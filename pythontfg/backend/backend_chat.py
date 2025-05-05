import reflex as rx
from pythontfg.backend.database_conect import Usuario

def click_red_social(nombre_red: str) -> rx.EventHandler:
    def handler():
        print(f"Botón pulsado: {nombre_red}")

        if nombre_red == "instagram":
            Usuario.set_red_social("instagram")
        elif nombre_red == "facebook":
           Usuario.set_red_social("facebook")
        elif nombre_red == "twitter":
            Usuario.set_red_social("twitter")
        elif nombre_red == "linkedin":
            Usuario.set_red_social("linkedin")
        else:
            return rx.event(handler)
    #return rx.redirect("/nuevo_chat/")



