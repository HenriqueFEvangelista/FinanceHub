from unittest.mock import patch
import requests
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIClient


@override_settings(ALPHA_VANTAGE_API_KEY="chave-de-teste")
class BuscarAcaoTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/acoes/aapl/"

    @patch("integracao.views.requests.get")
    def test_filtra_ultimo_pregao(self, get):
        dia = {"1. open": "100.00", "2. high": "110.00", "3. low": "90.00",
               "4. close": "105.00", "5. volume": "1000"}
        get.return_value.json.return_value = {
            "Meta Data": {"ignored": True},
            "Time Series (Daily)": {"2026-11-24": dia, "2026-11-25": dia},
        }
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data["data"], "2026-11-25")
        self.assertEqual(resposta.data["simbolo"], "AAPL")
        self.assertEqual(resposta.data["volume"], 1000)
        self.assertNotIn("Meta Data", resposta.data)
        self.assertEqual(get.call_args.kwargs["params"]["symbol"], "AAPL")

    @patch("integracao.views.requests.get")
    def test_limite_externo(self, get):
        get.return_value.json.return_value = {"Note": "limite"}
        self.assertEqual(self.client.get(self.url).status_code, 503)

    @patch("integracao.views.requests.get")
    def test_falha_externa(self, get):
        get.side_effect = requests.Timeout()
        self.assertEqual(self.client.get(self.url).status_code, 502)

    @patch("integracao.views.requests.get")
    def test_simbolo_invalido_externo(self, get):
        get.return_value.json.return_value = {"Error Message": "invalid"}
        self.assertEqual(self.client.get(self.url).status_code, 400)

    @override_settings(ALPHA_VANTAGE_API_KEY="")
    @patch("integracao.views.requests.get")
    def test_sem_chave(self, get):
        self.assertEqual(self.client.get(self.url).status_code, 500)
        get.assert_not_called()
