
from twikit import Client
from twikit.errors import Forbidden, NotFound


def recargar_twitter(usr:str, contrasena:str, usuario_contacto:str) -> list:
    print("Recargando mensajes de Twitter...")
    return []



async def enviar_mensaje_twitter(usr: str, mail_usr: str, contrasena: str, mensaje: str, usuario_contacto: str):
    client = Client('en-US')
    await client.login(
        auth_info_1=usr,
        auth_info_2=mail_usr,
        password=contrasena
    )
    try:
        print(f"Buscando usuario: {usuario_contacto}")
        user = await client.get_user_by_screen_name(usuario_contacto)
        user_id = user.id
        message = await client.send_dm(user_id, mensaje)
        print("Mensaje enviado:", message)
        return True
    except NotFound as e:
        print(f"❌ Usuario no encontrado o página no existe: {e}")
    except Forbidden as e:
        print(f"❌ No autorizado a enviar mensaje: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    return False
