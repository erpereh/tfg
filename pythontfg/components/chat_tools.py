import reflex as rx
from pythontfg import styles
from pythontfg.backend.database_conect import Usuario

def chatbar() -> rx.Component:
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
            rx.foreach(
                Usuario.filtered_sorted_items,
                lambda contacto: rx.box(
                    rx.text(
                        contacto.nombre,
                        font_size="1em",
                        font_weight=rx.cond(
                            Usuario.selected_contact_chat.email == contacto.email,
                            "bold",
                            "normal"
                        ),
                        color=rx.cond(
                            Usuario.selected_contact_chat.email == contacto.email,
                            styles.accent_text_color,
                            styles.text_color,
                        ),
                    ),
                    padding="0.5em",
                    border_bottom=styles.border,
                    cursor="pointer",
                    border_radius="md",
                    on_click=lambda contacto=contacto: Usuario.seleccionar_contacto_chat(contacto),
                )
            ),
            spacing="2",
        ),
        position="fixed",
        right="0",
        top="4em",  # ❗ Ajusta al alto real de tu header
        height="calc(100vh - 4em)",  # ❗ Así no pisa el header
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
            Usuario.selected_contact_chat,
            rx.vstack(
                rx.text(
                    f"Chat con {Usuario.selected_contact_chat.nombre}",
                    font_size="1.5em",
                    font_weight="bold"
                ),
                rx.hstack(
                    rx.text("Este es un prototipo del área de chat."),
                    spacing="2",
                    padding="1em",
                ),
                spacing="4",
                padding="2em",
                width="100%",
                height="100vh",
                overflow_y="auto",
            ),
            rx.box(
                rx.text("Selecciona un contacto para comenzar el chat."),
                width="100%",
                padding="2em",
                height="100vh"
            )
        ),
        margin_right=styles.sidebar_content_width,  # ❗ deja hueco para la barra fija
        width="100%",
    )
