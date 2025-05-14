
from instagrapi import Client

from pythontfg.backend.mensaje import Mensaje
import discord

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

def recargar_discord(usr:str, contrasena:str, usuario_contacto:str) -> list:
    print("Recargando mensajes de Discord...")
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
    

import discord
import asyncio
from datetime import datetime
from discord.errors import Forbidden
from discord.http import Route
from pythontfg.backend.mensaje import Mensaje

class DiscordSelfBot(discord.Client):
    def __init__(self, token: str, target_id: int, limit: int = 50):
        super().__init__(self_bot=True)
        self.token = token
        self.target_id = target_id
        self.limit = limit
        self.history: list[Mensaje] = []

    async def setup_hook(self):
        self.loop.create_task(self.main())

    async def on_ready(self):
        print(f"[✓] Conectado como {self.user} (ID: {self.user.id})")

    async def _get_dm_channel(self, user_id: int):
        try:
            user = await self.fetch_user(user_id)
            return user.dm_channel or await user.create_dm()
        except Forbidden:
            payload = {"recipient_id": str(user_id)}
            data = await self.http.request(Route("POST", "/users/@me/channels"), json=payload)
            channel_id = int(data["id"])
            return await self.fetch_channel(channel_id)

    async def read_conversation(self) -> list[Mensaje]:
        dm = await self._get_dm_channel(self.target_id)
        historial: list[Mensaje] = []
        async for msg in dm.history(limit=self.limit):
            texto = msg.content or "<media/sin texto>"
            hora = msg.created_at.strftime("%H:%M")
            enviado = (msg.author.id == self.user.id)
            # instantiate with keywords
            historial.append(
                Mensaje(mensaje=texto, fecha_hora=hora, enviado=enviado)
            )
        return historial

    async def main(self):
        await self.wait_until_ready()
        self.history = await self.read_conversation()
        await self.close()

    def run_and_fetch(self) -> list[Mensaje]:
        super().run(self.token)
        return self.history

def recargar_discord(token: str, usuario_id: int, cantidad: int = 20) -> list[Mensaje]:
    print(f"🔄 Recargando mensajes de Discord de usuario {usuario_id}…")
    bot = DiscordSelfBot(token, target_id=usuario_id, limit=cantidad)
    mensajes = bot.run_and_fetch()
    print(f"✅ Se obtuvieron {len(mensajes)} mensajes de Discord.")
    return mensajes