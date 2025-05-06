import reflex as rx
from pythontfg.backend.backend_chat import ChatState



def chat_bubble(sender, text):
    return rx.box(
        rx.text(text, color="white"),
        bg=rx.cond(sender == "user", "#333", "#8265d4"),
        border_radius="lg",
        max_width="80%",
        padding="10px",
        align_self=rx.cond(sender == "user", "end", "start"),
        margin_y="5px",
    )


def chat_ui():
    return rx.vstack(
        rx.box(
            rx.foreach(ChatState.messages, lambda msg: chat_bubble(msg[0], msg[1])),
            overflow_y="auto",
            height="400px",
            width="100%",
            padding="10px",
            border="1px solid #444",
            border_radius="lg",
            bg="#1a1a1a"
        ),
        rx.hstack(
            rx.input(
                value=ChatState.user_input,
                placeholder="Ask a question",
                on_change=ChatState.set_user_input,
                bg="#111",
                color="white",
                border="1px solid #555",
                flex="1",
            ),
            rx.button("Ask", on_click=ChatState.send_message, bg="#8265d4", color="white"),
            width="100%",
        ),
        width="100%",        
        margin="auto",
        spacing="4",
    )
