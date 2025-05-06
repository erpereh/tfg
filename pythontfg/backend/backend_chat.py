import reflex as rx
from pythontfg.backend.database_conect import Contacto
from typing import Optional

class ChatState(rx.State):
    
    selected_contact_chat: Optional[Contacto] = None

    selected_red_social: str = ""
    
    user_input: str = ""
    
    messages: list[tuple[str, str]] = [  # (remitente, mensaje)
        ("user", "Hola bb"),
        ("bot", "Q pasa mi loco"),
    ]


    def seleccionar_contacto_chat(self, contacto: Contacto):
        self.selected_contact_chat = contacto
        print(f"Contacto seleccionado: {self.selected_contact_chat.nombre}")
        if(self.selected_red_social=="instagram" and self.selected_contact_chat.instagram==""):
            self.selected_red_social=""
        elif(self.selected_red_social=="facebook" and self.selected_contact_chat.facebook==""):
            self.selected_red_social=""
        elif(self.selected_red_social=="twitter" and self.selected_contact_chat.twitter==""):
            self.selected_red_social=""
        elif(self.selected_red_social=="linkedin" and self.selected_contact_chat.linkedin==""):
            self.selected_red_social=""
    
    def set_red_social(self, red_social: str):
        self.selected_red_social = red_social
        print(f"Red social cambiada:{self.selected_red_social}")

    def is_all_selected(self) -> bool:
        return self.selected_contact_chat is not None and self.selected_red_social != ""

    def send_message(self):
        if self.user_input.strip():
            # Agrega el mensaje del usuario
            self.messages.append(("user", self.user_input.strip()))
            # Respuesta fija del bot por ahora
            self.messages.append(("bot", "Calla putita"))
            self.user_input = ""

"""
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
"""

