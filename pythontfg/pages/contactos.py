"""The table page."""

import reflex as rx

from pythontfg.backend.database_conect import Usuario

from ..templates import template
from ..views.table import main_table


@template(route="/contactos", title="Contactos", on_load=Usuario.load_entries)
def table() -> rx.Component:
    return rx.vstack(
        rx.heading("Contactos", size="5"),
        main_table(),
        spacing="8",
        width="100%",
    )
