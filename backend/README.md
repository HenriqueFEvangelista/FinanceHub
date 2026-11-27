# FinanceHub API — Atividades 3 e 4

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

## Histórico de pesquisas (Atividade 4)

A migração inicial de integracao está versionada. Execute `python manage.py migrate` para criar a tabela SQLite. Para conferir alterações no modelo, use `python manage.py makemigrations --check`.

Cada consulta GET bem-sucedida grava um registro no modelo HistoricoPesquisa, incluindo símbolo, data do pregão, preços decimais, volume e data/hora da consulta. Consultas repetidas geram novos registros; falhas não são gravadas. A data da consulta é diferente da data do pregão.

Crie um administrador antes de iniciar o servidor:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Consulte http://127.0.0.1:8000/api/acoes/AAPL/ e, se desejar, outro símbolo. Acesse http://127.0.0.1:8000/admin/ e entre com o superusuário. Abra Histórico de pesquisas para consultar os registros. É possível pesquisar pelo símbolo e filtrar por data.

Para a entrega, capture a resposta HTTP 200 na Browsable API e a tabela preenchida no admin, sem revelar senhas ou chaves.

## Testes

```powershell
python manage.py check
python manage.py test
```

Os testes simulam a resposta externa e não exigem uma chave real. O teste manual depende da disponibilidade e dos limites da Alpha Vantage.

## Escopo

Configuração local para a atividade escolar, não adequada a produção (DEBUG ativo, sem autenticação de usuários ou controle de quota local). A persistência é um histórico de consultas, não um serviço de atualização automática de preços. O GET tem efeito de gravação por exigência didática; em produção, revise a semântica HTTP, autenticação e limites.
