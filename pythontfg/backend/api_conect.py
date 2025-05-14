
from instagrapi import Client

from pythontfg.backend.mensaje import Mensaje

#cliente login para instagram
cl = Client()

def recargar_instagram(usr:str, contrasena:str, usuario_contacto:str, cantidad=2) -> list:
    print(f"usuario instagram: {usr}, contraseña {contrasena}")
    cl.login(usr, contrasena)

    # 1) ID del usuario con quien chateas
    target_id = cl.user_id_from_username(usuario_contacto)
    
    # 2) Obtén el dict bruto del hilo
    raw = cl.direct_thread_by_participants([target_id])
    thread = raw["thread"]
    
    # 3) Toma la lista de items (mensajes) y coge sólo los últimos `cantidad`
    items = thread["items"][-cantidad:]
    
    # 4) Tu propio ID para diferenciar
    mi_id = cl.user_id
    
    # 5) Recorre e imprime
    for msg in items:
        text = msg.get("text") or "<media/sin texto>"
        if msg["user_id"] == mi_id:
            print(f"Tú: {text}")
        else:
            print(f"{usuario_contacto}: {text}")
    return []

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