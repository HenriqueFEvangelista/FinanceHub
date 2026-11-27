from unittest.mock import patch
import requests
from datetime import date
from decimal import Decimal
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from .models import HistoricoPesquisa


@override_settings(ALPHA_VANTAGE_API_KEY="chave-de-teste")
class BuscarAcaoTests(TestCase):
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

        registro = HistoricoPesquisa.objects.get()
        self.assertEqual(registro.simbolo, "AAPL")
        self.assertEqual(registro.data_pregao, date(2026, 11, 25))
        self.assertEqual(registro.abertura, Decimal("100.00"))
        self.assertEqual(registro.fechamento, Decimal("105.00"))
        self.assertEqual(registro.volume, 1000)
        self.assertIsNotNone(registro.data_pesquisa)

    @patch("integracao.views.requests.get")
    def test_consultas_repetidas_criam_historico(self, get):
        dia = {"1. open": "100.0000", "2. high": "110.0000", "3. low": "90.0000",
               "4. close": "105.0000", "5. volume": "1000"}
        get.return_value.json.return_value = {"Time Series (Daily)": {"2026-11-25": dia}}
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertEqual(HistoricoPesquisa.objects.count(), 2)

    @patch("integracao.views.requests.get")
    def test_limite_externo(self, get):
        get.return_value.json.return_value = {"Note": "limite"}
        self.assertEqual(self.client.get(self.url).status_code, 503)
        self.assertFalse(HistoricoPesquisa.objects.exists())

    @patch("integracao.views.requests.get")
    def test_falha_externa(self, get):
        get.side_effect = requests.Timeout()
        self.assertEqual(self.client.get(self.url).status_code, 502)
        self.assertFalse(HistoricoPesquisa.objects.exists())

    @patch("integracao.views.requests.get")
    def test_simbolo_invalido_externo(self, get):
        get.return_value.json.return_value = {"Error Message": "invalid"}
        self.assertEqual(self.client.get(self.url).status_code, 400)
        self.assertFalse(HistoricoPesquisa.objects.exists())

    @override_settings(ALPHA_VANTAGE_API_KEY="")
    @patch("integracao.views.requests.get")
    def test_sem_chave(self, get):
        self.assertEqual(self.client.get(self.url).status_code, 500)
        self.assertFalse(HistoricoPesquisa.objects.exists())
        get.assert_not_called()

    @patch("integracao.views.requests.get")
    def test_preco_invalido_nao_salva(self, get):
        dia = {"1. open": "invalido", "2. high": "110.00", "3. low": "90.00",
               "4. close": "105.00", "5. volume": "1000"}
        get.return_value.json.return_value = {"Time Series (Daily)": {"2026-11-25": dia}}
        self.assertEqual(self.client.get(self.url).status_code, 502)
        self.assertFalse(HistoricoPesquisa.objects.exists())
