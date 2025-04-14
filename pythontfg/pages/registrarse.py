
import reflex as rx

from pythontfg.backend.database_conect import Usuario

@rx.page(route="/registrarse", title="Registrarse")
def registrarse() -> rx.Component:
    return rx.center(
        registrarse_default_icons(),
        height="100vh",
        padding="2em",
    )


def registrarse_default_icons() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/preicono.png",
                    width="2.5em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Registrarse",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Nombre",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Julio David",
                    type="email",
                    size="3",
                    width="100%",
                    on_change=Usuario.on_nombre_change
                ),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="juliodavid@gmail.com",
                    type="email",
                    size="3",
                    width="100%",
                    on_change=Usuario.on_email_change
                ),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Password",
                        size="3",
                        weight="medium",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=Usuario.on_pass_change
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Sign Up",
                size="3",
                width="100%",
                on_click=Usuario.validar_registro,
            ),
            rx.cond(
                Usuario.error != "",
                rx.text(Usuario.error, color="red", size="2"),
            ),
            rx.center(
                rx.text("Ya tienes cuenta?", size="3"),
                rx.link("Login", href="/", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        max_width="28em",
        size="4",
        width="100%",
    )
    