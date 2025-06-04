import requests
from pythontfg.backend.mensaje import Mensaje
from datetime import datetime

class LinkedInMessaging:
    API_KEY = 'hNmjgk/A.O3YWeB/a/x2cndxIn9ypRNlmaq5uavlNMZ67ipZOOKY='
    BASE_URL = 'https://api12.unipile.com:14287/api/v1'

    headers = {
        'X-API-KEY': API_KEY,
        'accept': 'application/json'
    }

    def __init__(self, dsn):
        self.dsn = dsn
        self.sync_account()
        
        self.mi_id = self.obtener_mi_id()
        print(f"Mi ID de LinkedIn: {self.mi_id}")

    def sync_account(self):
        url = f"{self.BASE_URL}/accounts/{self.dsn}/sync"
        response = requests.get(url, headers=self.headers)
        if response.ok:
            print("Sincronización iniciada correctamente.")
        else:
            print(f"Error al sincronizar cuenta: {response.status_code} - {response.text}")

    def enviar_mensajes_linkedin(self, chat_id: str, mensaje: str) -> bool:
        url = f"{self.BASE_URL}/chats/{chat_id}/messages"
        payload = {'text': mensaje}
        response = requests.post(url, headers={**self.headers, 'content-type': 'application/json'}, json=payload)
        if response.ok:
            print("Mensaje enviado correctamente.")
            return True
        else:
            print(f"Error enviando mensaje: {response.status_code} - {response.text}")
            return False

    def recargar_linkedin(self, chat_id: str, cantidad=10) -> list[Mensaje]:
        url = f"{self.BASE_URL}/chats/{chat_id}/messages"
        response = requests.get(url, headers=self.headers)
        if not response.ok:
            print(f"Error al obtener mensajes: {response.status_code} - {response.text}")
            return []

        items = response.json().get('items', [])

        def parsear_fecha_iso(fecha_str):
            if not fecha_str:
                return datetime.min
            try:
                if isinstance(fecha_str, int):
                    # Si la fecha viene como timestamp numérico (milisegundos o microsegundos)
                    if fecha_str > 1e14:
                        return datetime.fromtimestamp(fecha_str / 1_000_000)
                    elif fecha_str > 1e11:
                        return datetime.fromtimestamp(fecha_str / 1000)
                    else:
                        return datetime.fromtimestamp(fecha_str)
                elif isinstance(fecha_str, str):
                    if fecha_str.endswith('Z'):
                        fecha_str = fecha_str[:-1] + '+00:00'
                    return datetime.fromisoformat(fecha_str)
            except Exception:
                return datetime.min

        # Ordenar usando la función que parsea fecha ISO
        items = sorted(items, key=lambda m: parsear_fecha_iso(m.get('createdAt') or m.get('timestamp')))
        items = items[-cantidad:]

        # Asegúrate de tener el ID una sola vez
        mi_id = "ACoAAEuCDxIBsAHzghy2sjIyMj_-svPKoafs5Lw"
        if not mi_id:
            print("No se pudo obtener tu sender_id de LinkedIn. Todos los mensajes aparecerán como 'Contacto'.")
        nuevos_mensajes = []
        for msg in items:
            texto = msg.get('text', 'Mensaje sin texto')
            fecha = parsear_fecha_iso(msg.get('createdAt') or msg.get('timestamp'))
            enviado = (msg.get("sender_id") != mi_id)

            mensaje = Mensaje(
                mensaje=texto,
                fecha_hora=fecha.isoformat(),
                hora_formato_chat=fecha.strftime("%H:%M"),
                enviado=enviado,
                modo_chat=True
            )
            nuevos_mensajes.append(mensaje)
            print(f"Comparando: sender_id={msg.get('sender_id')} vs mi_id={mi_id}")
            autor = "Tú" if enviado else "Contacto"
            print(f"{autor}: {texto} a las {fecha.isoformat()}")
            #print("Mensaje completo:", msg)

        return nuevos_mensajes

    def obtener_mi_id(self):
        url = f"{self.BASE_URL}/accounts/{self.dsn}"
        response = requests.get(url, headers=self.headers)
        if response.ok:
            data = response.json()
            print("Respuesta completa de la cuenta:", data)
            # Extrae el sender_id de connection_params.im.id
            mi_id = (
                data.get("connection_params", {})
                    .get("im", {})
                    .get("id")
            )
            if mi_id:
                self.mi_id = mi_id
                print(f"Mi sender_id obtenido: {self.mi_id}")
                return mi_id
            else:
                print("No se encontró el sender_id en la respuesta de la cuenta.")
                self.mi_id = None
                return None
        else:
            print(f"Error al obtener ID de cuenta: {response.status_code} - {response.text}")
            self.mi_id = None
            return None
