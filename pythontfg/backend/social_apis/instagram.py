
from instagrapi import Client

from pythontfg.backend.mensaje import Mensaje
from datetime import datetime

# Cliente login para Instagram
cl = Client()

def recargar_instagram(usr: str, contrasena: str, usuario_contacto: str, cantidad=3) -> list[Mensaje]:
    print(f"usuario instagram: {usr}, contraseña {contrasena}")
    cl.login(usr, contrasena)

    target_id = cl.user_id_from_username(usuario_contacto)
    raw = cl.direct_thread_by_participants([target_id])
    thread = raw["thread"]
    items = thread["items"][-cantidad:]
    mi_id = cl.user_id
    nuevos_mensajes: list[Mensaje] = []

    for msg in items:
        texto = msg.get("text", "<media/sin texto>")
        timestamp = msg.get("timestamp") or msg.get("created_at")
        print(f"cargando: {texto} con hora {timestamp}")

        # Parseo robusto
        try:
            if isinstance(timestamp, int):
                # Detecta si es en microsegundos (más de 13 dígitos)
                timestamp_int = timestamp
            elif isinstance(timestamp, str) and timestamp.isdigit():
                timestamp_int = int(timestamp)
            else:
                raise ValueError("Formato de timestamp no reconocido")

            # Decodifica según la magnitud
            if timestamp_int > 1e14:  # más de 14 dígitos = microsegundos
                fecha = datetime.fromtimestamp(timestamp_int / 1_000_000)
            elif timestamp_int > 1e11:  # 13 dígitos = milisegundos
                fecha = datetime.fromtimestamp(timestamp_int / 1000)
            else:  # segundos
                fecha = datetime.fromtimestamp(timestamp_int)

        except Exception as e:
            print("Error parseando fecha:", e)
            fecha = datetime.now()


        mensaje = Mensaje(
            mensaje=texto,
            fecha_hora=fecha.isoformat(),
            enviado=(msg["user_id"] == mi_id)
        )

        nuevos_mensajes.append(mensaje)

        autor = "Tú" if mensaje.enviado else usuario_contacto
        print(f"{autor}: {mensaje.mensaje} a las {mensaje.fecha_hora}")

    return nuevos_mensajes



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