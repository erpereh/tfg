import reflex as rx

from ..templates.template import ThemeState


def radius_picker() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("radius"),
                rx.heading("Radio", size="6"),
                align="center",
            ),
            rx.select(
                [
                    "no",
                    "pequeño",
                    "mediano",
                    "grande",
                    "completo",
                ],
                size="3",
                value=ThemeState.radius_visual,  # <-- Usa valor visual en español
                on_change=ThemeState.set_radius,
            ),
            width="100%",
        ),
    )
