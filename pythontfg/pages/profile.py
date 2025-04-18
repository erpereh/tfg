from ..backend.database_conect import Usuario
from ..components.profile_input import profile_input
from ..templates import template
import reflex as rx


@template(route="/profile", title="Profile")
def profile() -> rx.Component:
    return rx.vstack(
        # Encabezado superior
        rx.hstack(
            rx.icon("square-user-round"),
            rx.heading("Información personal", size="5"),
            align="center",
        ),
        rx.text("Visualiza los datos vinculados a tu cuenta.", size="3"),
        
        # Cuerpo principal dividido en dos columnas
        rx.flex(
            # Columna izquierda: datos personales
            rx.form.root(
                rx.vstack(
                    profile_input("Nombre", "nombre", Usuario.nombre, "text", "user", Usuario.nombre, Usuario.on_nombre_change),
                    profile_input("Email", "email", Usuario.email, "email", "mail", Usuario.email, Usuario.no_se_puede_cambiar_email),
                    profile_input("Teléfono", "telefono", Usuario.telefono, "tel", "phone", Usuario.telefono, Usuario.on_telefono_change),

                    rx.button(
                        rx.icon("save", size=20),
                        "Guardar cambios",
                        size="3",
                        variant="solid",
                        color_scheme="green",
                        type="submit",
                    ),
                    spacing="4",
                ),
                on_submit=Usuario.guardar_cambios,
                reset_on_submit=False,
                width="100%",
            ),
            # Columna derecha: redes sociales
            rx.vstack(
                _social_group("Instagram", Usuario.instagram_usr, Usuario.instagram_pass, "instagram"),
                _social_group("Facebook", Usuario.facebook_usr, Usuario.facebook_pass, "facebook"),
                _social_group("Twitter", Usuario.twitter_usr, Usuario.twitter_pass, "twitter"),
                _social_group("LinkedIn", Usuario.linkedin_usr, Usuario.linkedin_pass, "linkedin"),
                spacing="4",
                width="100%",
            ),
            spacing="8",
            width="100%",
            flex_direction=["column", "column", "row"],
        ),
        
        # Mensaje de error debajo
        rx.cond(
            Usuario.error != "",
            rx.text(Usuario.error, color="red", size="2"),
        ),
        spacing="6",
        align="start",
        width="100%",
    )


def _social_group(nombre: str, usr: str, pwd: str, icono: str) -> rx.Component:
    """Muestra usuario y contraseña de una red social en una misma fila."""
    return rx.vstack(
        rx.hstack(
            profile_input(f"User {nombre}", f"{icono}_usr", usr, "text", icono, usr, getattr(Usuario, f"on_{icono}_usr_change")),
            profile_input(f"Pass {nombre}", f"{icono}_pass", pwd, "text", "lock", pwd, getattr(Usuario, f"on_{icono}_pass_change")),
            spacing="3",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )
