import reflex as rx
from ..templates import template
from pythontfg.components.chat_tools import chatbar
from pythontfg.components.chat_tools import area_chat

@template(route="/chat", title="Chat")
def chat() -> rx.Component:
    return rx.hstack(
        # Chatbar lateral
        chatbar(),
        area_chat(),  # Área de chat
        spacing="0",
        width="100%",
    )
