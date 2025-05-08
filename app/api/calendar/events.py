import requests
from fastapi import APIRouter, Depends, Request
from .oauth import get_token
from datetime import datetime, timedelta, timezone


router = APIRouter(tags=["events"])

@router.get("/events")
async def get_events(
    request: Request, 
    calendar_id: str, 
    query: str = None, 
    time_min: str = None,
    time_max: str = None
):
    
    
    
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
        "timeMin": time_min,
        "timeMax": time_max,
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



@router.get("/next-week-events")
async def get_next_week_events(
    request: Request, 
    calendar_id: str, 
    query: str = None, 

):
    
    hoje = datetime.now(timezone.utc)  # Pega a data e hora atual em UTC
    
    # Calcula quantos dias faltam até a próxima segunda-feira
    dias_ate_segunda = (7 - hoje.weekday()) % 7
    proxima_segunda = hoje + timedelta(days=dias_ate_segunda)

    # Zera hora, minuto, segundo e microssegundo
    proxima_segunda = proxima_segunda.replace(hour=0, minute=0, second=0, microsecond=0)

    # Define o domingo da semana seguinte: 6 dias depois da próxima segunda
    domingo_seguinte = proxima_segunda + timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Converte para o formato exigido pela API (ISO 8601 com 'Z' indicando UTC)
    time_min = proxima_segunda.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_max = domingo_seguinte.strftime("%Y-%m-%dT%H:%M:%SZ")   
    
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
        "timeMin": time_min,
        "timeMax": time_max,
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

        events = list(map(lambda x: dict(event_name = x["summary"],event_date = x["start"].get("dateTime", None)),events))
        return { "events": events }
    else:
        print("Erro:", response.status_code, response.text)

    return {"message": token}