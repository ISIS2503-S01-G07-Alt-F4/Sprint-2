import os
import time
import logging
import requests
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings
from Alarmas.logic import correos

logger = logging.getLogger(__name__)

# Valores por defecto configurables mediante variables de entorno.
# Estos parámetros se pueden sobreescribir al ejecutar el comando.
DEFAULT_KONG_ADMIN = os.environ.get('KONG_ADMIN_URL', 'http://localhost:8001')
DEFAULT_UPSTREAM = os.environ.get('KONG_UPSTREAM', 'provesi_upstream')
DEFAULT_INTERVAL = int(os.environ.get('KONG_POLL_INTERVAL', '30'))
DEFAULT_ALERT_EMAIL = os.environ.get('ALERT_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'ops@example.com'))
DEFAULT_CB_THRESHOLD = int(os.environ.get('CIRCUIT_BREAKER_THRESHOLD', '2'))


def get_kong_targets(kong_admin_url: str, upstream: str):
    """
    Obtiene la lista de targets (hosts:puerto) desde la Admin API de Kong.

    Comentarios en español:
    - Consulta: GET /upstreams/{upstream}/targets
    - El formato JSON devuelto puede variar entre versiones de Kong. Aquí
      intentamos soportar las claves más comunes ('data' o 'targets').
    - Devuelve una lista de cadenas como '10.0.0.1:8080'.
    """
    url = f"{kong_admin_url.rstrip('/')}/upstreams/{upstream}/targets"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Kong puede devolver 'data' o 'targets' dependiendo de la versión
        targets = []
        if isinstance(data, dict):
            if 'data' in data:
                items = data['data']
            elif 'targets' in data:
                items = data['targets']
            else:
                items = []
            for it in items:
                # cada elemento suele contener 'target' con formato 'ip:puerto'
                t = it.get('target') or it.get('address') or it.get('ip')
                if t:
                    targets.append(t)
        elif isinstance(data, list):
            for it in data:
                if isinstance(it, dict) and 'target' in it:
                    targets.append(it['target'])
        return targets
    except Exception as e:
        logger.exception('Failed to fetch targets from Kong Admin %s: %s', url, e)
        # En caso de error devolvemos lista vacía para no romper el bucle
        return []


def check_target_health(target: str, path: str = '/health/', timeout: int = 5) -> bool:
    """
    Llama directamente al endpoint de health del target.

    Comentarios en español:
    - target puede venir como 'host:puerto' o solo 'host'. Se construye
      la URL con http por defecto.
    - Devuelve True si obtiene HTTP 200, False en cualquier otro caso.
    """
    if ':' in target:
        host, port = target.split(':', 1)
        url = f'http://{host}:{port}{path}'
    else:
        url = f'http://{target}{path}'
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except Exception:
        # Si falla la conexión o hay timeout, consideramos el target unhealthy
        return False


class Command(BaseCommand):
    help = 'Poll Kong upstream targets and send notifications when servers go down or circuit-breaker activates.'

    def add_arguments(self, parser):
        # Argumentos CLI para sobreescribir los valores por defecto
        parser.add_argument('--kong-admin', dest='kong_admin', default=DEFAULT_KONG_ADMIN,
                            help='Kong Admin URL, e.g. http://kong:8001')
        parser.add_argument('--upstream', dest='upstream', default=DEFAULT_UPSTREAM,
                            help='Name of the Kong upstream to monitor')
        parser.add_argument('--interval', dest='interval', type=int, default=DEFAULT_INTERVAL,
                            help='Polling interval in seconds')
        parser.add_argument('--email', dest='email', default=DEFAULT_ALERT_EMAIL,
                            help='Alert recipient email')
        parser.add_argument('--circuit-threshold', dest='circuit_threshold', type=int, default=DEFAULT_CB_THRESHOLD,
                            help='Number of unhealthy targets to consider circuit-breaker activated')
        parser.add_argument('--once', dest='once', action='store_true', help='Run only one poll and exit')

    def handle(self, *args, **options):
        # Valores usados en esta ejecución
        kong_admin = options['kong_admin']
        upstream = options['upstream']
        interval = options['interval']
        alert_email = options['email']
        circuit_threshold = options['circuit_threshold']
        once = options['once']

        logger.info('Starting Kong monitor for upstream %s against admin %s', upstream, kong_admin)

        # Llaves de cache para almacenar el estado previo y si ya se envió alerta CB
        cache_key = f'kong_monitor_status:{upstream}'
        cb_flag_key = f'kong_monitor_cb_sent:{upstream}'

        while True:
            # 1) Obtener targets desde Kong Admin
            targets = get_kong_targets(kong_admin, upstream)
            if not targets:
                logger.warning('No targets found for upstream %s', upstream)
            current_status = {}
            unhealthy_count = 0
            # 2) Comprobar cada target llamando su /health/
            for t in targets:
                ok = check_target_health(t)
                current_status[t] = ok
                if not ok:
                    unhealthy_count += 1

            # 3) Leer el estado previo desde cache (si existe)
            prev_status = cache.get(cache_key, {})

            # 4) Detectar transiciones healthy -> unhealthy y enviar email por target
            for t, ok in current_status.items():
                prev_ok = prev_status.get(t, True)
                if prev_ok and not ok:
                    logger.info('Target %s transitioned healthy->unhealthy', t)
                    # Enviar correo indicando que el servidor específico cayó
                    try:
                        correos.notify_server_down(alert_email, t, details=f'Observed by monitor for upstream {upstream}')
                    except Exception:
                        logger.exception('Failed to send server down email for %s', t)

            # 5) Lógica de circuito: si hay suficientes targets unhealthy, avisar
            cb_sent = cache.get(cb_flag_key, False)
            if unhealthy_count >= circuit_threshold and not cb_sent:
                logger.info('Circuit-breaker condition met: %d unhealthy (threshold=%d)', unhealthy_count, circuit_threshold)
                try:
                    # Enviar correo informando que se activó el circuit-breaker
                    correos.notify_circuit_breaker_activated(alert_email, upstream,
                                                            details=f'{unhealthy_count} unhealthy targets (threshold {circuit_threshold})')
                    # Marcar en cache que ya enviamos la alerta para no repetir
                    cache.set(cb_flag_key, True, None)
                except Exception:
                    logger.exception('Failed to send circuit-breaker email for upstream %s', upstream)

            # 6) Si el número de unhealthy baja del umbral y ya habíamos enviado la alerta,
            #    limpiamos la marca para permitir futuras alertas si vuelve a ocurrir.
            if unhealthy_count < circuit_threshold and cb_sent:
                logger.info('Circuit-breaker cleared for upstream %s', upstream)
                cache.set(cb_flag_key, False, None)

            # 7) Persistir estado actual en cache para la siguiente iteración
            cache.set(cache_key, current_status, None)

            if once:
                break
            time.sleep(interval)
