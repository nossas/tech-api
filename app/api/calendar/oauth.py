from google.oauth2 import service_account
from google.auth.transport.requests import Request
import google.auth


async def get_token():
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    SERVICE_ACCOUNT_FILE = "/Users/developer/Repositories/nossas/bonde/tech-api/app/api/calendar/google.json"  # Substitua pelo seu arquivo JSON

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Se precisar impersonar o usuário (delegação), descomente abaixo:
    # credentials = credentials.with_subject("barbara@nossas.org")

    # Gera o token
    credentials.refresh(Request())
    return credentials.token