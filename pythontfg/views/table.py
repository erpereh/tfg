#table.py

import reflex as rx

from pythontfg.backend.database_conect import Contacto, Usuario

def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: Contacto, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.nombre),
        rx.table.cell(item.email),
        rx.table.cell(item.telefono),
        rx.table.cell(item.instagram),
        rx.table.cell(item.discord),
        rx.table.cell(item.twitter),
        rx.table.cell(item.linkedin),
        rx.table.cell(
            rx.hstack(
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.icon_button(
                            rx.icon("pencil"),
                            variant="ghost",
                            color_scheme="blue",
                            on_click=lambda: Usuario.preparar_formulario(item),
                            size="2",
                        )
                    ),
                    rx.dialog.content(
                        rx.dialog.title("Modificar usuario"),
                        rx.dialog.description("Rellena los campos para modificar un usuario"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Nombre",
                                    value=item.nombre,
                                    on_change=Usuario.set_nuevo_nombre,
                                    required=True,
                                ),
                                rx.input(
                                    placeholder="Email",
                                    value=item.email,
                                    on_change=Usuario.set_nuevo_email,
                                    required=True,
                                ),
                                rx.input(
                                    placeholder="Teléfono",
                                    value=item.telefono,
                                    on_change=Usuario.set_nuevo_telefono,
                                ),
                                rx.input(
                                    placeholder="Instagram",
                                    value=item.instagram,
                                    on_change=Usuario.set_nuevo_instagram,
                                ),
                                rx.input(
                                    placeholder="Discord",
                                    value=item.discord,
                                    on_change=Usuario.set_nuevo_discord,
                                ),
                                rx.input(
                                    placeholder="Twitter",
                                    value=item.twitter,
                                    on_change=Usuario.set_nuevo_twitter,
                                ),
                                rx.input(
                                    placeholder="LinkedIn",
                                    value=item.linkedin,
                                    on_change=Usuario.set_nuevo_linkedin,
                                ),
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button("Cancelar", variant="soft", color_scheme="gray")
                                    ),
                                    rx.dialog.close(
                                        rx.button(
                                            "Guardar",
                                            on_click=lambda: Usuario.modificar_contacto(item.nombre),
                                        )
                                    ),  
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                        ),
                        max_width="450px",
                    ),
                ),
                rx.icon_button(
                    rx.icon("trash"),
                    variant="ghost",
                    color_scheme="red",
                    on_click=lambda: Usuario.eliminar_contacto(item.nombre),
                    size="2",
                ),
            )
        ),

        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(Usuario.page_number),
                f" of {Usuario.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=Usuario.first_page,
                    opacity=rx.cond(Usuario.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(Usuario.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=Usuario.prev_page,
                    opacity=rx.cond(Usuario.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(Usuario.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=Usuario.next_page,
                    opacity=rx.cond(
                        Usuario.page_number == Usuario.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        Usuario.page_number == Usuario.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=Usuario.last_page,
                    opacity=rx.cond(
                        Usuario.page_number == Usuario.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        Usuario.page_number == Usuario.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )


def main_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                # icono de orden, flecha hacia arriba o hacia abajo de la a-z o z-a
                rx.cond(
                    Usuario.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=Usuario.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=Usuario.toggle_sort,
                    ),
                ),
                # combobox de ordenamiento, por nombre, pago, fecha o estado
                rx.select(
                    [
                        "nombre",
                        "email",
                        "teléfono",
                        "instagram",
                        "discord",
                        "twitter",
                        "linkedin",
                    ],
                    placeholder="Ordenar por:",
                    size="3",
                    on_change=Usuario.set_sort_value,
                ),
                # label de búsqueda, se pone una cruz para borrar el texto
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=Usuario.setvar("search_value", ""),
                        display=rx.cond(Usuario.search_value, "flex", "none"),
                    ),
                    value=Usuario.search_value,
                    placeholder="Buscar contacto...",
                    size="3",
                    width="100%",
                    max_width=["300px", "350px", "400px", "500px"],  # más largo
                    variant="surface",
                    color_scheme="gray",
                    on_change=Usuario.set_search_value,
                    min_width="230px",
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            # botón de añadir nuevo usuario, que abre un modal con un formulario
            rx.hstack(
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            rx.icon("plus", size=20),
                            "Añadir",
                            size="3",
                            variant="surface",
                            display=["none", "none", "none", "flex"],
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title("Añadir nuevo usuario"),
                        rx.dialog.description("Rellena los campos para añadir un nuevo usuario"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Nombre",
                                    value=Usuario.nuevo_nombre,
                                    on_change=Usuario.set_nuevo_nombre,
                                    required=True,
                                ),
                                rx.input(
                                    placeholder="Email",
                                    value=Usuario.nuevo_email,
                                    on_change=Usuario.set_nuevo_email,
                                    required=True,
                                ),
                                rx.input(
                                    placeholder="Teléfono",
                                    value=Usuario.nuevo_telefono,
                                    on_change=Usuario.set_nuevo_telefono,
                                ),
                                rx.input(
                                    placeholder="Instagram",
                                    value=Usuario.nuevo_instagram,
                                    on_change=Usuario.set_nuevo_instagram,
                                ),
                                rx.input(
                                    placeholder="Discord",
                                    value=Usuario.nuevo_discord,
                                    on_change=Usuario.set_nuevo_discord,
                                ),
                                rx.input(
                                    placeholder="Twitter",
                                    value=Usuario.nuevo_twitter,
                                    on_change=Usuario.set_nuevo_twitter,
                                ),
                                rx.input(
                                    placeholder="LinkedIn",
                                    value=Usuario.nuevo_linkedin,
                                    on_change=Usuario.set_nuevo_linkedin,
                                ),
                                rx.flex(
                                    rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                                    rx.dialog.close(rx.button("Guardar", type="submit")),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=Usuario.add_new_user,
                            reset_on_submit=False,
                        ),
                        max_width="450px",
                    ),
                ),
                # botón de exportar a csv, que llama a la función export_to_csv
                rx.button(
                    rx.icon("arrow-down-to-line", size=20),
                    "Export",
                    size="3",
                    variant="surface",
                    display=["none", "none", "none", "flex"],
                    on_click=Usuario.export_to_csv,
                ),
                spacing="3",
                justify="end",
                wrap="wrap",
                width="100%",
                padding_bottom="1em",
            ),
        ),
        # contenido de la tabla
        rx.table.root(
            # cabezera de la tabla
            rx.table.header(
                rx.table.row(
                    _header_cell("Nombre", "user"),
                    _header_cell("Email", "mail"),
                    _header_cell("Teléfono", "phone"),
                    _header_cell("Instagram", "instagram"),
                    _header_cell("Discord", "message-circle-heart"),
                    _header_cell("Twitter", "twitter"),
                    _header_cell("Linkedin", "linkedin"),
                    _header_cell("Modificar", "chart-candlestick"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    Usuario.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )
