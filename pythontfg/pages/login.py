#login.py
import reflex as rx

from pythontfg.backend.database_conect import Usuario

@rx.page(route="/", title="Login")
def login_page() -> rx.Component:
    return rx.center(
        login_default_icons(),
        height="100vh",
        padding="2em",
    )


def login_default_icons() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/chatly_cuadrado.jpg",
                    width="2.5em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Accede con tu cuenta",
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
                    "Email",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="juliodavidtfg@gmail.com",
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
                        "Contraseña",
                        size="3",
                        weight="medium",
                    ),
                    rx.link(
                        "¿Olvidaste tu contraseña?",
                        href="#",
                        on_click=Usuario.reset_password,
                        size="3",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Introduce tu contraseña",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=Usuario.on_pass_change
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Iniciar sesión",
                size="3",
                width="100%",
                # Comentar, solo para desarrollar
                on_click=Usuario.validar_login,
            ),
            rx.cond(
                Usuario.error != "",
                rx.text(Usuario.error, color="red", size="2"),
            ),
            rx.center(
                rx.text("No tienes cuenta?", size="3"),
                rx.link("Registrarse", href="/registrarse", size="3"),
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
    
