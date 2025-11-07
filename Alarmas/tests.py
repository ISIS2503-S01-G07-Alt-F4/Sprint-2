from django.test import TestCase, Client


class HealthEndpointTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_health_returns_200(self):
		resp = self.client.get('/health/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json().get('status'), 'ok')
