from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def _send(subject: str, body: str, to: list, html: str | None = None):
    """Send an email using Django's email backend.

    - subject: subject text
    - body: plain text body
    - to: list of recipient emails
    - html: optional HTML body
    """
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
        if html:
            msg = EmailMessage(subject=subject, body=body, from_email=from_email, to=to)
            msg.content_subtype = 'html'
            msg.send(fail_silently=False)
        else:
            send_mail(subject, body, from_email, to, fail_silently=False)
        logger.info("Sent email '%s' to %s", subject, to)
        return True
    except Exception as e:
        logger.exception("Failed to send email '%s' to %s: %s", subject, to, e)
        return False


def notify_server_down(to_email: str, server_name: str, details: str | None = None):
    """Notify a single recipient that a monitored server is down."""
    subject = f"[ALERTA] Servidor caído: {server_name}"
    body = f"El servidor '{server_name}' ha sido reportado como caído.\n"
    if details:
        body += f"Detalles: {details}\n"
    body += "Por favor revise el servicio."
    return _send(subject, body, [to_email])


def notify_circuit_breaker_activated(to_email: str, circuit_name: str, details: str | None = None):
    """Notify that a circuit-breaker was activated."""
    subject = f"[ALERTA] Circuit-breaker activado: {circuit_name}"
    body = f"Se ha activado el circuit-breaker '{circuit_name}'.\n"
    if details:
        body += f"Detalles: {details}\n"
    body += "Revise las métricas y logs asociados para diagnosticar el problema."
    return _send(subject, body, [to_email])
