import reflex as rx
from pythontfg.backend.database_conect import Contacto
from pythontfg.backend.database_conect import supabase
from typing import Optional


class Mensaje(rx.Base):
    mensaje: str = ""
    fecha_hora: str = ""
    enviado: bool = False

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
        redes = {
            "instagram": self.selected_contact_chat.instagram,
            "facebook": self.selected_contact_chat.facebook,
            "twitter": self.selected_contact_chat.twitter,
            "linkedin": self.selected_contact_chat.linkedin,
        }
        # Si la actual está vacía o no existe, buscar la siguiente disponible
        if self.selected_red_social not in redes or redes[self.selected_red_social] == "":
            for red, valor in redes.items():
                if valor != "":
                    self.selected_red_social = red
                    break
            else:
                self.selected_red_social = ""
        


    
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


