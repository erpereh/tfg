import reflex as rx
from pythontfg.backend.backend_chat import ChatState



def chat_bubble(msg):
    return rx.hstack(
        rx.box(
            rx.hstack(
                rx.text(msg.mensaje, color="white", flex="1"),
                rx.text(msg.fecha_hora, font_size="0.8em", color="white", margin_left="10px"),
                justify="between",
                width="100%",
            ),
            bg=rx.cond(msg.enviado, "#333", "#8265d4"),
            border_radius="lg",
            max_width="80%",
            padding="10px",
        ),
        justify=rx.cond(msg.enviado, "end", "start"),  # <- aquí decides si va a la derecha o a la izquierda
        width="100%",
        margin_bottom="0.5em",
    )




def chat_ui():
    return rx.vstack(
        rx.box(
            rx.foreach(ChatState.messages, chat_bubble),
            overflow_y="auto",
            height="100%",            # <- ocupará todo el alto disponible
            width="100%",
            padding="10px",
            border="1px solid #444",
            border_radius="lg",
            bg="#1a1a1a",
            flex="1"                  # <- permite que esta caja crezca
        ),
        rx.hstack(
            rx.input(
                value=ChatState.user_input,
                placeholder="Escribe un mensaje...",
                on_change=ChatState.set_user_input,
                bg="#111",
                color="white",
                border="1px solid #555",
                flex="1",
            ),
            rx.button("Enviar", on_click=ChatState.send_message, bg="#8265d4", color="white"),
            width="100%",
        ),
        width="100%",
        margin="auto",
        spacing="4",
        height="100%",               # <- asegura que el vstack crezca
    )

