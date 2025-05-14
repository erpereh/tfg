
from instagrapi import Client

from pythontfg.backend.mensaje import Mensaje

#cliente login para instagram
cl = Client()

from instagrapi import Client
from pythontfg.backend.mensaje import Mensaje
from datetime import datetime

# Cliente login para Instagram
cl = Client()

def recargar_instagram(usr: str, contrasena: str, usuario_contacto: str, cantidad=2) -> list[Mensaje]:
    print(f"usuario instagram: {usr}, contraseña {contrasena}")
    cl.login(usr, contrasena)

    # ID del usuario con quien chateas
    target_id = cl.user_id_from_username(usuario_contacto)

    # Obtén el dict bruto del hilo
    raw = cl.direct_thread_by_participants([target_id])
    thread = raw["thread"]

    # Lista de items (mensajes) - últimos N
    items = thread["items"][-cantidad:]

    # Tu propio ID para distinguir enviados de recibidos
    mi_id = cl.user_id

    nuevos_mensajes: list[Mensaje] = []

    for msg in items:
        texto = msg.get("text", "<media/sin texto>")
        timestamp = msg.get("timestamp") or msg.get("created_at")  # depende del formato

        # Intentamos convertir la fecha a datetime
        try:
            if isinstance(timestamp, int):  # Unix timestamp en milisegundos
                fecha = datetime.fromtimestamp(timestamp / 1000)
            elif isinstance(timestamp, str):
                fecha = datetime.fromisoformat(timestamp)
            else:
                fecha = datetime.now()
        except Exception as e:
            print("Error parseando fecha:", e)
            fecha = datetime.now()

        # Construimos el mensaje
        mensaje = Mensaje(
            mensaje=texto,
            fecha_hora=fecha.strftime("%H:%M"),
            enviado=(msg["user_id"] == mi_id)
        )
        nuevos_mensajes.append(mensaje)

        autor = "Tú" if mensaje.enviado else usuario_contacto
        print(f"{autor}: {mensaje.mensaje} a las {mensaje.fecha_hora}")

    return nuevos_mensajes


def recargar_twitter(usr:str, contrasena:str, usuario_contacto:str) -> list:
    print("Recargando mensajes de Twitter...")
    return []

def recargar_facebook(usr:str, contrasena:str, usuario_contacto:str) -> list:
    print("Recargando mensajes de Facebook...")
    return []

def recargar_linkedin(usr:str, contrasena:str, usuario_contacto:str) -> list:
    print("Recargando mensajes de LinkedIn...")
    return []


def enviar_mensaje_instagram(usuario, mensaje):
    # Obtener el ID del usuario
    user_id = cl.user_id_from_username(usuario)
    
    # Enviar el mensaje
    cl.direct_send(mensaje, [user_id])
    print(f"Mensaje enviado a {usuario}: {mensaje}")
    
def ver():
    target_id = cl.user_id_from_username("d.pereezz_")
    thread = cl.direct_thread_by_participants([target_id])
    print(thread["thread"].keys())