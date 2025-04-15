## Como rodar

Criar um ambiente virtual e ativa-lo

`python3 -m venv .venv && source .venv/bin/activate`

Instalar as dependencias

`pip install -r requirements.txt`

Executar API

`uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload`

## Anotações

Calendário

1. Para acessar os dados do calendário a agenda precisa de estar compartilhada com o e-mail da conta de serviço usado na autenticação da API com o Google;

TODO:

- Listar eventos por todas as páginas
- Restringir melhor o período da busca
- Melhorar filtro de busca