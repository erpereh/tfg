import reflex as rx
from pythontfg import styles

button_style = {
    "width": "300px",              # Ancho fijo
    "height": "300px",             # Alto fijo (para que sean cuadrados)
    "border_radius": "4",          # Esquinas cuadradas
    "padding": "1em",
    "display": "flex",             # Se usa flex para centrar el contenido
    "flex_direction": "column",    # Los elementos se apilan verticalmente
    "justify_content": "center",
    "align_items": "center",
    "justify": "center",
}

def button_redes(icon_tag:str, icon_name:str, text:str, bg_color:str, hover:str, on_click=None) -> rx.Component:
    return rx.button(
        rx.vstack(
            rx.icon(tag=icon_tag, name=icon_name, color="white", size=45),
            rx.text(text, color="white", margin_top="0.5em", font_size="45px"),
            width="100%",
            align="center",
        ),
        background_color=bg_color,
        _hover=hover,
        on_click=on_click,
        **button_style,
    )