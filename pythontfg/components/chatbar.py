import reflex as rx
from pythontfg import styles
from pythontfg.backend.database_conect import Usuario  # Ajusta la importación según tu estructura

def chatbar() -> rx.Component:
    return rx.hstack(
        rx.box(
            # Barra de búsqueda con ícono de lupa.
            rx.hstack(
                rx.icon(tag="search", name="search", color=styles.accent_text_color),
                rx.input(
                    placeholder="Buscar contacto...",
                    value=Usuario.search_value,
                    on_change=Usuario.set_search_value,
                ),
                margin_bottom="1em",
                align_items="center",
            ),
            # Listado de contactos filtrados.
            rx.foreach(
                Usuario.filtered_sorted_items,
                lambda contacto: rx.box(
                    rx.text(contacto.nombre, font_size="1em"),
                    padding="0.5em",
                    border_bottom=styles.border,
                    cursor="pointer",
                    background_color=rx.cond(
                        contacto == Usuario.selected_contact,
                        styles.accent_bg_color,
                        styles.gray_bg_color,
                    ),
                    color=rx.cond(
                        contacto == Usuario.selected_contact,
                        styles.accent_text_color,
                        styles.text_color,
                    ),
                    # Al hacer clic, actualiza la selección y prepara el formulario.
                    on_click=lambda contacto=contacto: Usuario.seleccionar_contacto(contacto),
                )
            ),
            width=styles.sidebar_content_width,
            background_color=styles.gray_bg_color,
            padding="1em",
            border_left=styles.border,
            height="100vh",
            position="fixed",
            right="0",
            top="0",
            overflow_y="auto",
        ),
        justify="end",
        width="100%",
    )
    