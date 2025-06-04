import reflex as rx
from datetime import datetime
from pythontfg.backend.social_apis.calendar_api import crear_evento_google_calendar

class Mensaje(rx.Base):
    mensaje: str = ""
    fecha_hora: str = ""
    hora_formato_chat: str = ""
    enviado: bool = False
    modo_chat: bool = False
    
    
    # creación eventos en Calendar
    evento_localizado: bool = False
    evento: str = ""
    fecha_dt: datetime = datetime.now()
    duracion: float = 1.0

    def crear_evento_mensaje(self):
        crear_evento_google_calendar(self.evento, self.fecha_dt, self.duracion)
