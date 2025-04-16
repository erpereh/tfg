"""The profile page."""
from ..backend.database_conect import Usuario
from ..components.profile_input import profile_input
from ..templates import template
import reflex as rx


@template(route="/profile", title="Profile")
def profile() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("square-user-round"),
                    rx.heading("Información personal", size="5"),
                    align="center",
                ),
                rx.text("Visualiza los datos vinculados a tu cuenta.", size="3"),
                width="100%",
            ),
            rx.vstack(
                profile_input(
                    "Nombre",
                    "nombre",
                    Usuario.nombre,
                    "text",
                    "user",
                    Usuario.nombre,
                ),
                profile_input(
                    "Email",
                    "email",
                    Usuario.email,
                    "email",
                    "mail",
                    Usuario.email,
                ),
                profile_input(
                    "Teléfono",
                    "telefono",
                    str(Usuario.telefono),
                    "tel",
                    "phone",
                    str(Usuario.telefono),
                ),

                # Redes sociales agrupadas: usr y pass en una fila
                _social_group("Instagram", Usuario.instagram_usr, Usuario.instagram_pass, "instagram"),
                _social_group("Facebook", Usuario.facebook_usr, Usuario.facebook_pass, "facebook"),
                _social_group("Twitter", Usuario.twitter_usr, Usuario.twitter_pass, "twitter"),
                _social_group("LinkedIn", Usuario.linkedin_usr, Usuario.linkedin_pass, "linkedin"),

                width="100%",
                spacing="4",
            ),
            width="100%",
            spacing="4",
            flex_direction=["column", "column", "row"],
        ),
        rx.divider(),
        spacing="6",
        width="100%",
        max_width="800px",
    )


def _social_group(nombre: str, usr: str, pwd: str, icono: str) -> rx.Component:
    """Muestra usuario y contraseña de una red social en una misma fila."""
    return rx.vstack(
        rx.text(nombre, size="3", weight="medium"),
        rx.hstack(
            profile_input(f"{nombre} usuario", f"{icono}_usr", usr, "text", icono, usr),
            profile_input(f"{nombre} contraseña", f"{icono}_pass", pwd, "text", "lock", pwd),
            spacing="3",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )
