import reflex as rx
from pythontfg import styles
from pythontfg.backend.database_conect import Usuario
from pythontfg.components.button_redes_chat import button_redes
from pythontfg.backend.backend_chat import ChatState
from pythontfg.components.chat_usr import chat_ui

def social_buttons() -> rx.Component:
    return rx.cond(
        ChatState.selected_contact_chat,
        rx.flex(
            rx.cond(
                ChatState.selected_contact_chat.instagram,
                button_redes(
                    "instagram", "instagram", "#E1306C", "#C13584",
                    on_click=ChatState.set_red_social("instagram")
                ),
                rx.fragment()
            ),
            rx.cond(
                ChatState.selected_contact_chat.discord,
                button_redes(
                    "message-circle-heart", "message-circle-heart", "#3b5998", "#8b9dc3",
                    on_click=ChatState.set_red_social("discord")
                ),
                rx.fragment()
            ),
            rx.cond(
                ChatState.selected_contact_chat.twitter,
                button_redes(
                    "twitter", "twitter", "#1DA1F2", "#1991DB",
                    on_click=ChatState.set_red_social("twitter")
                ),
                rx.fragment()
            ),
            rx.cond(
                ChatState.selected_contact_chat.linkedin,
                button_redes(
                    "linkedin", "linkedin", "#0077B5", "#005983",
                    on_click=ChatState.set_red_social("linkedin")
                ),
                rx.fragment()
            ),
            spacing="2",
            justify="center",
            display="flex",
            align_items="center",
            width="100%",
        ),
        rx.box()  # Si no hay contacto seleccionado, no muestra nada
    )


def chatbar() -> rx.Component:
    """ ESTE ES EL DE CHAT """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="search", name="search", color=styles.accent_text_color),
                rx.input(
                    placeholder="Buscar contacto...",
                    value=Usuario.search_value,
                    on_change=Usuario.set_search_value,
                ),
                spacing="2",
                align_items="center",
                margin_bottom="1em",
            ),
            social_buttons(),
            rx.foreach(
                Usuario.filtered_sorted_items,
                lambda contacto: rx.box(
                    rx.text(
                        contacto.nombre,
                        font_size="1em",
                        font_weight=rx.cond(
                            ChatState.selected_contact_chat.email == contacto.email,
                            "bold",
                            "normal"
                        ),
                        color=rx.cond(
                            ChatState.selected_contact_chat.email == contacto.email,
                            styles.accent_text_color,
                            styles.text_color,
                        ),
                    ),
                    padding="0.5em",
                    border_bottom=styles.border,
                    cursor="pointer",
                    border_radius="md",
                    on_click=lambda contacto=contacto: ChatState.seleccionar_contacto_chat(contacto),
                )
            ),
            spacing="2",
        ),
        position="fixed",
        right="0",
        top="4em",  # Ajusta según el alto real de tu header
        height="calc(100vh - 4em)",  # Así no pisa el header
        width=styles.sidebar_content_width,
        background_color=styles.gray_bg_color,
        padding="1em",
        border_left=styles.border,
        overflow_y="auto",
        z_index="10",
    )


def area_chat() -> rx.Component:
    return rx.box(
        rx.cond(
            ChatState.selected_contact_chat,
            rx.vstack(
                # Agrupa ambas cards en un hstack para que estén una al lado de la otra
                rx.hstack(
                    rx.card(
                        rx.hstack(
                            rx.cond(
                                ChatState.selected_red_social == "instagram",
                                rx.icon(tag="instagram", color="#E1306C", size=32),
                                rx.cond(
                                    ChatState.selected_red_social == "discord",
                                    rx.icon(tag="message-circle-heart", color="#3b5998", size=32),
                                    rx.cond(
                                        ChatState.selected_red_social == "twitter",
                                        rx.icon(tag="twitter", color="#1DA1F2", size=32),
                                        rx.cond(
                                            ChatState.selected_red_social == "linkedin",
                                            rx.icon(tag="linkedin", color="#0077B5", size=32),
                                            rx.fragment()
                                        )
                                    )
                                )
                            ),
                            rx.text(
                                f"{ChatState.selected_contact_chat.nombre}",
                                font_size="1.5em",
                                font_weight="bold",
                                margin_left="0.5em"
                            ),
                            spacing="2",
                            align_items="center",
                        ),
                        padding="1em",
                        border_radius="md",
                        box_shadow="md",
                        background_color=styles.gray_bg_color,
                        margin_bottom="0em",  # Más pegado al chat
                        min_width="250px",
                    ),
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="mail", color="#0077B5", size=32),
                            rx.text(
                                f"{ChatState.mensajes_filtrados_list.length()}",
                                font_size="1.5em",
                                font_weight="bold",
                                margin_left="0.5em"
                            ),
                            spacing="2",
                            align_items="center",
                        ),
                        padding="1em",
                        border_radius="md",
                        box_shadow="md",
                        background_color=styles.gray_bg_color,
                        margin_bottom="0em",  # Más pegado al chat
                        width="auto",
                    ),
                    spacing="4",  # Más espacio entre las dos cards
                    align_items="center",
                    width="100%",
                ),
                rx.cond(
                    ChatState.is_all_selected(),
                    chat_ui(),
                    rx.text("Selecciona todos los elementos primero.", color="gray"),
                ),
                spacing="2",  # Menos espacio vertical entre las cards y el chat
                padding="2em",
                width="100%",
                flex="1",
                min_height="100vh",
                overflow_y="auto",
            ),
            rx.box(
                rx.text("Selecciona un contacto para comenzar el chat."),
                width="100%",
                padding="2em",
                height="100vh"
            ),
        ),
        margin_right=styles.sidebar_content_width,
        width="100%",
        height="100%",
    )
