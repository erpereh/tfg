"""The overview page of the app."""

import datetime

import reflex as rx

from pythontfg.backend.database_conect import Usuario

from .. import styles
from ..components.card import card
from ..components.notification import notification
from ..templates import template
from ..views.acquisition_view import acquisition
from ..views.charts import (
    StatsState,
    area_toggle,
    orders_chart,
    pie_chart,
    revenue_chart,
    timeframe_select,
    users_chart,
)


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/overview", title="Overview", on_load=StatsState.randomize_data)
def index() -> rx.Component:
    """The overview page.
    Returns:
        The UI for the overview page.

    """
    num_contactos = Usuario.contactos.length()
    return rx.vstack(
        rx.flex(
            rx.heading(
                f"Hola, {Usuario.nombre}",
                size="8",
                white_space="nowrap",
            ),
            rx.flex(
                rx.link(
                    notification("message-square-text", "plum", num_contactos),
                    href="/chat",
                    style={"cursor": "pointer"},
                ),
                spacing="4",
                wrap="nowrap",
                justify="end",
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.grid(
            rx.card(
                rx.hstack(
                    rx.icon("users", size=36),
                    rx.vstack(
                        rx.text("Contactos", size="4", weight="medium"),
                        rx.text(Usuario.contactos.length(), size="6", weight="bold"),
                        spacing="1",
                        align_items="start",
                    ),
                    align="center",
                    spacing="4",
                ),
                size="3",
                width="100%",
            ),
            rx.card(
                rx.hstack(
                    rx.icon("message-circle", size=36),
                    rx.vstack(
                        rx.text("Mensajes totales", size="4", weight="medium"),
                        rx.text(Usuario.stat_num_mensajes, size="6", weight="bold"),
                        spacing="1",
                        align_items="start",
                    ),
                    align="center",
                    spacing="4",
                ),
                size="3",
                width="100%",
            ),
            rx.card(
                rx.hstack(
                    rx.icon("at-sign", size=36),
                    rx.vstack(
                        rx.text("Media redes sociales por contacto", size="4", weight="medium"),
                        rx.text(f"{Usuario.stat_media_redes_sociales_disponibles_por_contacto:.2f}", size="6", weight="bold"),
                        spacing="1",
                        align_items="start",
                    ),
                    align="center",
                    spacing="4",
                ),
                size="3",
                width="100%",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
                "repeat(3, 1fr)",
            ],
            width="100%",
        ),
        card(
            rx.hstack(
                tab_content_header(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Users", value="users"),
                    rx.segmented_control.item("Revenue", value="revenue"),
                    rx.segmented_control.item("Orders", value="orders"),
                    margin_bottom="1.5em",
                    default_value="users",
                    on_change=StatsState.set_selected_tab,
                ),
                width="100%",
                justify="between",
            ),
            rx.match(
                StatsState.selected_tab,
                ("users", users_chart()),
                ("revenue", revenue_chart()),
                ("orders", orders_chart()),
            ),
        ),
        rx.grid(
            card(
                rx.hstack(
                    rx.hstack(
                        rx.icon("user-round-search", size=20),
                        rx.text("Visitors Analytics", size="4", weight="medium"),
                        align="center",
                        spacing="2",
                    ),
                    timeframe_select(),
                    align="center",
                    width="100%",
                    justify="between",
                ),
                pie_chart(),
            ),
            card(
                rx.hstack(
                    rx.icon("globe", size=20),
                    rx.text("Acquisition Overview", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="2.5em",
                ),
                rx.vstack(
                    acquisition(),
                ),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
