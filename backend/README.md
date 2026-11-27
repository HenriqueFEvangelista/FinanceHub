# FinanceHub API — Atividade 3

Backend didático Django REST Framework com SQLite e integração Alpha Vantage (TIME_SERIES_DAILY).

## Executar no Windows (PowerShell)

A partir da raiz do repositório:

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite o arquivo `.env` e preencha ALPHA_VANTAGE_API_KEY com sua chave pessoal. Não faça commit desse arquivo.

```powershell
python manage.py migrate
python manage.py runserver
```

Abra http://127.0.0.1:8000/api/acoes/AAPL/ para visualizar a Browsable API. A resposta retorna o último pregão disponível: símbolo, data, abertura, máxima, mínima, fechamento e volume. O histórico original e metadados externos são omitidos. Preços são preservados como strings decimais na moeda original do ativo.

## Testes

```powershell
python manage.py check
python manage.py test
```

Os testes simulam a resposta externa e não exigem uma chave real. O teste manual depende da disponibilidade e dos limites da Alpha Vantage.

## Escopo

Configuração local para a atividade escolar, não adequada a produção (DEBUG ativo, sem autenticação de usuários ou controle de quota local). Não há persistência de cotações nesta etapa.
