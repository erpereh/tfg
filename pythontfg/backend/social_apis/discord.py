
#discord
import discord
from datetime import datetime
from discord.errors import Forbidden
from discord.http import Route
from pythontfg.backend.mensaje import Mensaje
import asyncio


def recargar_discord(token: str, usuario_id: int, cantidad: int = 20) -> list[Mensaje]:
    print(f"🔄 Recargando mensajes de Discord de usuario {usuario_id}…")
    bot = DiscordSelfBot(token, target_id=usuario_id, limit=cantidad)
    mensajes = bot.run_and_fetch()
    print(f"✅ Se obtuvieron {len(mensajes)} mensajes de Discord.")
    mensajes.reverse()
    return mensajes


def enviar_mensaje_discord(usuario_id: int, mensaje: str, token: str):
    """
    Envía un mensaje a un usuario específico en Discord.
    """
    bot = DiscordSelfBot(token, target_id=usuario_id)
    bot.run_and_fetch()
    channel = bot._get_dm_channel(usuario_id)
    
    # Enviar el mensaje
    channel.send(mensaje)
    print(f"Mensaje enviado a {usuario_id}: {mensaje}")


    


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
            fecha = msg.created_at.isoformat()
            hora = msg.created_at.strftime("%H:%M")
            enviado = (msg.author.id == self.user.id)
            # instantiate with keywords
            historial.append(
                Mensaje(mensaje=texto, fecha_hora=fecha, hora_formato_chat=hora, enviado=enviado, modo_chat=True)
            )
        return historial

    async def main(self):
        await self.wait_until_ready()
        self.history = await self.read_conversation()
        await self.close()

    def run_and_fetch(self) -> list[Mensaje]:
        super().run(self.token)
        return self.history



class DiscordSelfBotSender(discord.Client):
    def __init__(self, token: str, target_id: int, message: str):
        super().__init__(self_bot=True)
        self.token = token
        self._target_id = target_id
        self._message = message
        self._ready = asyncio.Event()

    async def setup_hook(self):
        # Lanza la tarea de envío justo antes de conectar
        self.loop.create_task(self._send_and_close())

    async def on_ready(self):
        # Señalamos que ya estamos listos
        self._ready.set()

    async def _get_dm_channel(self, user_id: int):
        # Intentamos por API “public” primero
        try:
            user = await self.fetch_user(user_id)
            return user.dm_channel or await user.create_dm()
        except Forbidden:
            # Fallback HTTP a /users/@me/channels
            payload = {"recipient_id": str(user_id)}
            data = await self.http.request(
                Route("POST", "/users/@me/channels"),
                json=payload
            )
            channel = await self.fetch_channel(int(data["id"]))
            return channel

    async def _send_and_close(self):
        # 1) Esperamos a on_ready
        await self._ready.wait()
        # 2) Conseguimos (o creamos) el canal DM
        dm = await self._get_dm_channel(self._target_id)
        # 3) Enviamos el mensaje
        await dm.send(self._message)
        print(f"✅ Discord: mensaje enviado a {self._target_id}: {self._message}")
        # 4) Cerramos el bot
        await self.close()

    def run_and_send(self):
        # Arranca el cliente y bloquea hasta que _send_and_close haga close()
        super().run(self.token)


def enviar_mensaje_discord(token: str, usuario_id: int, mensaje: str):
    """
    Envía un mensaje a un usuario específico en Discord usando self-bot.
    :param token: Tu token de usuario de Discord.
    :param usuario_id: ID del destinatario.
    :param mensaje: Texto a enviar.
    """
    print(f"✉️ Enviando mensaje de Discord a {usuario_id}: {mensaje!r}")
    bot = DiscordSelfBotSender(token, usuario_id, mensaje)
    bot.run_and_send()

