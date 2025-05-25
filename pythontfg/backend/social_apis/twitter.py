from datetime import datetime
from twikit.errors import Forbidden, NotFound
from pythontfg.backend.mensaje import Mensaje
from twikit import Client

async def recargar_twitter(usr: str, mail_usr: str, contrasena: str, usuario_contacto: str, cantidad=4) -> list[Mensaje]:
    client = Client('en-US')
    await client.login(
        auth_info_1=usr,
        auth_info_2=mail_usr,
        password=contrasena
    )

    user = await client.get_user_by_screen_name(usuario_contacto)
    user_id = user.id

    mensajes_raw = await client.get_dm_history(user_id)
    mi_id = await client.user_id()

    nuevos_mensajes: list[Mensaje] = []

    # Tomamos los últimos `cantidad` mensajes
    ultimos_mensajes = list(mensajes_raw)[-cantidad:]

    for msg in ultimos_mensajes:
        texto = getattr(msg, 'text', '<Sin texto>')
        fecha = getattr(msg, 'created_at', datetime.now())
        enviado = (msg.sender_id == mi_id)

        mensaje = Mensaje(
            mensaje=texto,
            fecha_hora=fecha.isoformat(),
            hora_formato_chat=fecha.strftime("%H:%M"),
            enviado=enviado
        )

        nuevos_mensajes.append(mensaje)

        autor = "Tú" if enviado else usuario_contacto
        print(f"{autor}: {texto} a las {fecha.isoformat()}")

    return nuevos_mensajes





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
