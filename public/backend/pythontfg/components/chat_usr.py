import reflex as rx
from pythontfg.backend.backend_chat import ChatState
from pythontfg.backend.backend_chat import Mensaje



def chat_bubble(msg: Mensaje) -> rx.Component:
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
            max_height="200px",
            overflow_y="auto",
        ),
        justify=rx.cond(msg.enviado, "end", "start"),  # <- aquí decides si va a la derecha o a la izquierda
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
        rx.box(
            rx.foreach(ChatState.messages, chat_bubble),
            overflow_y="auto",   # aparece scroll solo si excede la altura
            height="70vh",       # fija al 70 % del viewport
            width="100%",
            padding="10px",
            border="1px solid #444",
            border_radius="lg",
            bg="#1a1a1a",
        ),
        rx.hstack(
            # Botón de IA
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
                min_rows=1,  # número mínimo de filas
                max_rows=6,  # límite para que no crezca infinito
                resize="none",  # evita que el usuario redimensione manualmente
            ),
            rx.button("Enviar", on_click=ChatState.send_message, bg="#8265d4", color="white"),
            width="100%",
        ),
        width="100%",
        margin="auto",
        spacing="4",
        height="100%",               # <- asegura que el vstack crezca
    )

