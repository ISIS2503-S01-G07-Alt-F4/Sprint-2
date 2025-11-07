from django.shortcuts import render
from django.http import JsonResponse


# Healthcheck endpoint for Kong active checks
def health(request):
	"""
	Simple health endpoint that returns HTTP 200 and a small JSON body.
	Kong upstream healthchecks can be pointed to /health/.
	"""
	return JsonResponse({"status": "ok"})


from django.views.decorators.csrf import csrf_exempt
import json
from .logic import correos


@csrf_exempt
def server_down_notify(request):
	"""Webhook endpoint to notify that a server is down.

	Expects JSON POST with keys: 'server_name', 'email' and optional 'details'.
	"""
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=405)
	try:
		payload = json.loads(request.body)
	except Exception:
		return JsonResponse({'error': 'invalid json'}, status=400)

	server_name = payload.get('server_name')
	email = payload.get('email')
	details = payload.get('details')
	if not server_name or not email:
		return JsonResponse({'error': 'server_name and email required'}, status=400)

	sent = correos.notify_server_down(email, server_name, details)
	return JsonResponse({'sent': sent})


@csrf_exempt
def circuit_breaker_notify(request):
	"""Webhook endpoint to notify that a circuit-breaker was activated.

	Expects JSON POST with keys: 'circuit_name', 'email' and optional 'details'.
	"""
	if request.method != 'POST':
		return JsonResponse({'error': 'POST required'}, status=405)
	try:
		payload = json.loads(request.body)
	except Exception:
		return JsonResponse({'error': 'invalid json'}, status=400)

	circuit_name = payload.get('circuit_name')
	email = payload.get('email')
	details = payload.get('details')
	if not circuit_name or not email:
		return JsonResponse({'error': 'circuit_name and email required'}, status=400)

	sent = correos.notify_circuit_breaker_activated(email, circuit_name, details)
	return JsonResponse({'sent': sent})
