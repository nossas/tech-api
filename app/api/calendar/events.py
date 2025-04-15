import requests
from fastapi import APIRouter, Depends, Request
from .oauth import get_token


router = APIRouter(tags=["events"])

@router.get("/events")
async def get_events(request: Request, calendar_id: str, query: str = None):
    token = await get_token()

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    # Cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Parâmetros da consulta
    params = {
        "singleEvents": "true",
        "orderBy": "startTime",
        "timeMin": "2025-01-01T00:00:00Z",
        "maxResults": 50
    }

    # Fazendo a requisição
    response = requests.get(url, headers=headers, params=params)

    # Verificando resposta
    if response.status_code == 200:
        events = response.json().get("items", [])
        print(events)
        if query:
            events = list(filter(lambda x: query.lower() in x.get("summary", "").lower(), events))

        return { "events": events }
    else:
        print("Erro:", response.status_code, response.text)

    return {"message": token}