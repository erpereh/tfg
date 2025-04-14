
import reflex as rx

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
                    on_change=RegistroState.set_nombre,
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
                    on_change=RegistroState.set_email,
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
                    on_change=RegistroState.set_password,
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Sign Up",
                size="3",
                width="100%",
                on_click=RegistroState.validar_usr_pass,
            ),
            rx.cond(
                RegistroState.intentado_login & (RegistroState.error != ""),
                rx.text(RegistroState.error, color="red", size="2"),
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
    
import re
class RegistroState(rx.State):
    nombre: str = ""
    email: str = ""
    password: str = ""
    error: str = ""  # mensaje de error
    intentado_login: bool = False  # nueva bandera

    def validar_usr_pass(self):
        self.intentado_login = True
        
        print(f"Nombre: {self.nombre}, Email: {self.email}, Contraseña: {self.password}")

        if not self.email:
            self.error = "El correo no puede estar vacío."
            return

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.email):
            self.error = "El formato del correo no es válido."
            return

        if len(self.password) < 6:
            self.error = "La contraseña debe tener al menos 6 caracteres."
            return

        self.error = ""  # limpia el error si todo está bien
        return rx.redirect("/overview")
