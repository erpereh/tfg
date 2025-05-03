import reflex as rx

from ..templates import template

from pythontfg.components.chatbar import chatbar

@template(route="/chat", title="Chat")
def chat() -> rx.Component:
    return rx.vstack(
        chatbar()
    )
