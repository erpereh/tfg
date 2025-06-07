"""The overview page of the app."""

import datetime

import reflex as rx

from pythontfg.backend.database_conect import Usuario

from .. import styles
from ..components.card import card
from ..components.notification import notification
from ..templates import template
from ..views.acquisition_view import acquisition
from reflex.components.radix.themes.base import LiteralAccentColor


@template(route="/inicio", title="Inicio")
def inicio() -> rx.Component:
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

        # AQUI VAN LAS ESTADÍSTICAS DE ARRIBA
        primeras_stats(),

        # AQUI VA EL DIAGRAMA DE MENSAJES EN EL TIEMPO
        diagrama_mensajes_temporalmente(),

        rx.grid(
            # AQUI VA EL DIAGRAMA EN CÍRCULO
            diagrama_circular(),

            # AQUI VA EL DIAGRAMA DE MENSAJES EN EL TIEMPO
            diagrama_abajo_derercha(),            
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



# ***************************************************************************
# *********** TODO ESTO ES PARA EL DIAGRAMA MENSAJES TEMPORALMENTE***********
# ***************************************************************************
def diagrama_mensajes_temporalmente() -> rx.Component:
    return card(
        rx.hstack(
            tab_content_header(),
            rx.segmented_control.root(
                rx.segmented_control.item("Enviados", value="enviados"),
                rx.segmented_control.item("Recibidos", value="recibidos"),
                rx.segmented_control.item("Todos", value="todos"),
                margin_bottom="1.5em",
                default_value="enviados",
                on_change=Usuario.set_tipo_mensaje,
            ),
            width="100%",
            justify="between",
        ),
        rx.match(
            Usuario.tipo_mensaje_seleccionado,
            ("enviados", diagrama_enviados()),
            ("recibidos", diagrama_recibidos()),
            ("todos", diagrama_todos()),
        ),
    )


def diagrama_enviados() -> rx.Component:
    return rx.cond(
        Usuario.tipo_diagrama,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Enviados",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.enviados_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="Enviados",
                stroke=rx.color("blue", 9),
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.enviados_data,
            height=425,
        ),
    )


def diagrama_recibidos() -> rx.Component:
    return rx.cond(
        Usuario.tipo_diagrama,
        rx.recharts.area_chart(
            _create_gradient("green", "colorGreen"),
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Recibidos",
                stroke=rx.color("green", 9),
                fill="url(#colorGreen)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.recibidos_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Recibidos",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.recibidos_data,
            height=425,
        ),
    )


def diagrama_todos() -> rx.Component:
    return rx.cond(
        Usuario.tipo_diagrama,
        rx.recharts.area_chart(
            _create_gradient("purple", "colorPurple"),
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Todos",
                stroke=rx.color("purple", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.todos_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Todos",
                stroke=rx.color("purple", 9),
                fill=rx.color("purple", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=Usuario.todos_data,
            height=425,
        ),
    )


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="95%", stop_opacity=0
                ),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )

def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        boton_tipo_diagrama(),
        align="center",
        width="100%",
        spacing="4",
    )
def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Historial de mensajes últimos 30 días", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )
def boton_tipo_diagrama() -> rx.Component:
    return rx.cond(
        Usuario.tipo_diagrama,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=Usuario.cambio_tipo_diagrama,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=Usuario.cambio_tipo_diagrama,
        ),
    )
# ***************************************************************************



def diagrama_abajo_derercha() -> rx.Component:
    return card(
        rx.hstack(
            rx.icon("globe", size=20),
            rx.text("Usuarios Chatly AI", size="4", weight="medium"),
            align="center",
            spacing="2",
            margin_bottom="2.5em",
        ),
        rx.vstack(
            acquisition(),
        ),
    )


def diagrama_circular() -> rx.Component:
    return card(
        rx.hstack(
            rx.hstack(
                rx.icon("user-round-search", size=20),
                rx.text("Contactos por redes sociales", size="4", weight="medium"),
                align="center",
                spacing="2",
            ),
            align="center",
            width="100%",
            justify="between",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=Usuario.datos_formato_grafico_circular,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
    )



def primeras_stats() -> rx.Component:
    return rx.grid(
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
    )