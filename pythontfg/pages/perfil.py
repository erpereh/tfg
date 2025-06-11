from ..backend.database_conect import Usuario
from ..templates import template
import reflex as rx


@template(route="/perfil", title="Perfil")
def perfil() -> rx.Component:
    return rx.vstack(
        # Encabezado superior
        rx.hstack(
            rx.icon("square-user-round"),
            rx.heading("Información personal", size="8"),
            align="center",
        ),
        rx.text("Visualiza los datos vinculados a tu cuenta.", size="3"),
        
        # Cuerpo principal dividido en dos columnas
        rx.flex(
            # Columna izquierda: datos personales
            rx.form.root(
                rx.vstack(
                    profile_input("Nombre", "nombre", Usuario.nombre, "text", "user", Usuario.nombre, Usuario.on_nombre_change),
                    profile_input_clickable_email(label="Email", name="email", value=Usuario.email, icon="mail", on_click=Usuario.no_mod_email),
                    profile_input("Contraseña", "pass", Usuario.password, "pass", "lock", Usuario.password, Usuario.on_pass_change),
                    profile_input("Teléfono", "telefono", Usuario.telefono, "tel", "phone", Usuario.telefono, Usuario.on_telefono_change),
                    rx.button(
                        rx.icon("save", size=20),
                        "Guardar cambios",
                        size="3",
                        variant="solid",
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
                _social_group("Discord", Usuario.discord_usr, Usuario.discord_pass, "discord"),
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
            profile_input(f"User {nombre}", f"{icono}_usr", usr, "text", icono, usr, getattr(Usuario, f"set_{icono}_usr")),
            profile_input(f"Pass {nombre}", f"{icono}_pass", pwd, "text", "lock", pwd, getattr(Usuario, f"set_{icono}_pass")),
            spacing="3",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )

def profile_input(
    label: str,
    name: str,
    placeholder: str,
    type: str,
    icon: str,
    default_value: str = "",
    on_change=None,
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
            on_change=on_change,
        ),
        direction="column",
        spacing="1",
        width="100%",
    )

def profile_input_clickable_email(
    label: str,
    name: str,
    value: str,
    icon: str,
    on_click=None,
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            align="center",
            spacing="2",
            width="100%",
        ),
        rx.input(
            value=value,
            name=name,
            width="100%",
            is_read_only=True,  # No editable pero permite interacción
            on_click=on_click,
            cursor="pointer",
        ),
        spacing="1",
        width="100%",
    )
