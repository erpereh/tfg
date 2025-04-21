"""The table page."""

import reflex as rx

from pythontfg.backend.database_conect import Usuario

from ..templates import template
from ..views.table import main_table


@template(route="/contactos", title="Contactos", on_load=Usuario.load_entries)
def table() -> rx.Component:
    """The table page.

    Returns:
        The UI for the table page.

    """
    return rx.vstack(
        rx.heading("Contactos", size="5"),
        main_table(),
        spacing="8",
        width="100%",
    )

""" ESTA SI QUE FUNCIONA YA QUE NO CUENTA CON LAS CLASES TABLE, TABLESTATE ....


@template(route="/contactos", title="Contactos", on_load=TableState.load_entries)
def table() -> rx.Component:
    The table page.

    Returns:
        The UI for the table page.

    return rx.vstack(
        rx.heading("Contactos guardados", size="5"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Teléfono"),
                    rx.table.column_header_cell("Instagram"),
                    rx.table.column_header_cell("Facebook"),
                    rx.table.column_header_cell("Twitter"),
                    rx.table.column_header_cell("LinkedIn"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    Usuario.contactos,
                    lambda contacto: rx.table.row(
                        rx.table.cell(contacto.nombre),
                        rx.table.cell(contacto.email),
                        rx.table.cell(contacto.telefono),
                        rx.table.cell(contacto.instagram),
                        rx.table.cell(contacto.facebook),
                        rx.table.cell(contacto.twitter),
                        rx.table.cell(contacto.linkedin),
                    )
                )
            ),
            width="100%",
            variant="surface",
        ),
        spacing="4",
        align="start",
        width="100%",
        padding="4",
    )
"""