
from instagrapi import Client

from pythontfg.backend.mensaje import Mensaje
from datetime import datetime

# Cliente login para Instagram
cl = Client()
def recargar_instagram(usr: str, contrasena: str, usuario_contacto: str, cantidad=4) -> list[Mensaje]:
    print(f"usuario instagram: {usr}, contraseña {contrasena}")
    cl.login(usr, contrasena)

    target_id = cl.user_id_from_username(usuario_contacto)
    raw = cl.direct_thread_by_participants([target_id])

    thread = raw["thread"]
    # Paso 1: ordenar cronológicamente los mensajes (más antiguos primero)
    items = sorted(thread["items"], key=lambda m: int(m.get("timestamp") or m.get("created_at")))
    # Paso 2: coger los últimos `cantidad` mensajes reales
    items = items[-cantidad:]

    mi_id = cl.user_id
    nuevos_mensajes: list[Mensaje] = []

    for msg in items:
        texto = msg.get("text", "Audio / imagen sin texto")
        timestamp = msg.get("timestamp") or msg.get("created_at")
        # Parseo robusto
        try:
            if isinstance(timestamp, int):
                timestamp_int = timestamp
            elif isinstance(timestamp, str) and timestamp.isdigit():
                timestamp_int = int(timestamp)
            else:
                raise ValueError("Formato de timestamp no reconocido")

            if timestamp_int > 1e14:
                fecha = datetime.fromtimestamp(timestamp_int / 1_000_000)
            elif timestamp_int > 1e11:
                fecha = datetime.fromtimestamp(timestamp_int / 1000)
            else:
                fecha = datetime.fromtimestamp(timestamp_int)

        except Exception as e:
            print("Error parseando fecha:", e)
            fecha = datetime.now()

        mensaje = Mensaje(
            mensaje=texto,
            fecha_hora=fecha.isoformat(),
            hora_formato_chat=fecha.strftime("%H:%M"),
            enviado=(msg["user_id"] == mi_id)
        )

        nuevos_mensajes.append(mensaje)

        autor = "Tú" if mensaje.enviado else usuario_contacto
        print(f"{autor}: {mensaje.mensaje} a las {mensaje.fecha_hora}")

    return nuevos_mensajes



def enviar_mensaje_instagram(usr: str, contrasena: str, mensaje:str , usuario_contacto: str):
    # Obtener el ID del usuario
    cl.login(usr, contrasena)
    destinatario_id = cl.user_id_from_username(usuario_contacto)
    
    # Enviar el mensaje
    cl.direct_send(mensaje, [destinatario_id])
    print(f"Mensaje enviado a {usuario_contacto}: {mensaje}")
    