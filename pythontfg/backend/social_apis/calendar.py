from datetime import datetime
from datetime import timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def crear_evento_google_calendar(evento: str, fecha: datetime, duracion: float):
    if not evento or not fecha:
        print("No se pudo extraer la información correctamente.")
        return

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    # Autenticación local del usuario
    flow = InstalledAppFlow.from_client_secrets_file("assets/credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("calendar", "v3", credentials=creds)

    # Formato de la fecha para Google Calendar
    fecha_google = fecha.strftime("%Y-%m-%dT%H:%M:%S")
    fecha_fin = (fecha + timedelta(hours=duracion)).strftime("%Y-%m-%dT%H:%M:%S")

    event = {
        "summary": evento,
        "start": {"dateTime": fecha_google, "timeZone": "Europe/Madrid"},
        "end": {"dateTime": fecha_fin, "timeZone": "Europe/Madrid"},
    }
    
    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Evento creado en Google Calendar: {event.get('htmlLink')}")
