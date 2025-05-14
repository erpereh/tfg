import reflex as rx

from pythontfg.backend.backend_chat import ChatState
from pythontfg.backend.database_conect import Usuario
from pythontfg.backend.usuario_ligero import UsuarioLigero
from ..templates import template
from pythontfg.components.chat_tools import chatbar
from pythontfg.components.chat_tools import area_chat

@template(
    route="/chat",
    title="Chat",
    on_load=Usuario.enviar_datos_chat  # ← este nuevo método lo crearás ahora
)
def chat() -> rx.Component:
    return rx.hstack(
        chatbar(),
        area_chat(),
        spacing="0",
        width="100%",
    )
