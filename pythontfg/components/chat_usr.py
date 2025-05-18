import reflex as rx
from pythontfg.backend.backend_chat import ChatState
from pythontfg.backend.backend_chat import Mensaje



def chat_bubble(msg: Mensaje, index: int) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(msg.mensaje, color="white", flex="1",word_break="break-word"),
                    rx.text(msg.hora_formato_chat, font_size="0.8em", color="white", margin_left="10px"),
                    justify="between",
                    width="100%",
                ),
                rx.cond(
                    msg.evento_localizado,
                    rx.button(
                        rx.icon("calendar", color="white"),  # icono blanco
                        title=f"Crear evento: {msg.evento}",
                        on_click=lambda: ChatState.confirmar_evento(index),
                        size="2",
                        variant="ghost",  # mejor que outline para que no tenga borde
                        margin_top="5px",
                    ),
                    rx.fragment()
                ),
            ),
            bg=rx.cond(msg.enviado, "#333", "#8265d4"),
            border_radius="lg",
            max_width="80%",
            padding="10px",
            max_height="200px",
            overflow_y="auto",
        ),
        justify=rx.cond(msg.enviado, "end", "start"),
        width="100%",
        margin_bottom="0.5em",
    )




def chat_ui():
    return rx.vstack(
        rx.cond(
            ChatState.is_generating_ia,
            rx.box(
                rx.spinner(size="3"),
                rx.text("Generando mensaje con IA...", color="white"),
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                bg="rgba(0, 0, 0, 0.5)",
                display="flex",
                align_items="center",
                justify_content="center",
                z_index="100",
            )
        ),
        # Botón justo encima de la caja de mensajes
        rx.hstack(
            rx.spacer(),  # empuja el botón a la derecha
            rx.icon_button(
                rx.icon("refresh-cw"),
                on_click=ChatState.reload_messages,
                color_scheme="blue",
                variant="soft",
                size="2",
            ),
            width="100%",
        ),
        rx.box(
            rx.foreach(
                ChatState.messages,
                lambda msg, i: chat_bubble(msg, i)
            ),
            overflow_y="auto",
            height="70vh",
            width="100%",
            padding="10px",
            border="1px solid #444",
            border_radius="lg",
            bg="#1a1a1a",
        ),
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon(tag="lightbulb", size=24, margin_right="1"), 
                    align_items="center",
                ),
                on_click=ChatState.write_with_ia,
                variant="solid",
                disabled=ChatState.is_generating_ia,
            ),
            rx.text_area(
                value=ChatState.user_input,
                placeholder="Escribe un mensaje...",
                on_change=ChatState.set_user_input,
                bg="#111",
                color="white",
                border="1px solid #555",
                flex="1",
                min_rows=1,
                max_rows=6,
                resize="none",
            ),
            rx.button("Enviar", on_click=ChatState.send_message, bg="#8265d4", color="white"),
            width="100%",
        ),
        width="100%",
        margin="auto",
        spacing="4",
        height="100%",
    )
