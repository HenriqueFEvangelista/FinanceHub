import re
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def buscar_acao(request, simbolo):
    simbolo = simbolo.upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9.:-]{0,19}", simbolo):
        return Response({"erro": "Símbolo inválido."}, status=400)

    if not settings.ALPHA_VANTAGE_API_KEY:
        return Response({"erro": "Chave da API não configurada."}, status=500)

    try:
        resposta = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "TIME_SERIES_DAILY",
                "symbol": simbolo,
                "apikey": settings.ALPHA_VANTAGE_API_KEY,
            },
            timeout=10,
        )
        resposta.raise_for_status()
        dados = resposta.json()
    except (requests.RequestException, ValueError):
        return Response({"erro": "Falha ao consultar a API externa."}, status=502)

    if not isinstance(dados, dict):
        return Response({"erro": "Resposta externa inválida."}, status=502)
    if "Error Message" in dados:
        return Response({"erro": "Símbolo não encontrado ou consulta inválida."}, status=400)
    if "Note" in dados or "Information" in dados:
        return Response({"erro": "Consulta indisponível. Verifique a chave e os limites da Alpha Vantage."}, status=503)

    historico = dados.get("Time Series (Daily)")
    if not isinstance(historico, dict) or not historico:
        return Response({"erro": "Dados indisponíveis na API externa."}, status=502)

    try:
        data = max(historico)
        acao = historico[data]
        resultado = {
            "mensagem": "Dados consumidos com sucesso!",
            "simbolo": simbolo,
            "data": data,
            "abertura": acao["1. open"],
            "maxima": acao["2. high"],
            "minima": acao["3. low"],
            "fechamento": acao["4. close"],
            "volume": int(acao["5. volume"]),
        }
    except (KeyError, TypeError, ValueError):
        return Response({"erro": "Dados financeiros externos inválidos."}, status=502)

    return Response(resultado)
