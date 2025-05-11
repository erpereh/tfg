import reflex as rx


def profile_input(
    label: str,
    name: str,
    placeholder: str,
    type: str,
    icon: str,
    default_value: str = "",
    on_change=None,  # nuevo parámetro
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            width="100%",
            align="center",
            spacing="2",
        ),
        rx.input(
            placeholder=placeholder,
            type=type,
            default_value=default_value,
            name=name,
            width="100%",
            on_change=on_change,  # nuevo
        ),
        direction="column",
        spacing="1",
        width="100%",
    )
