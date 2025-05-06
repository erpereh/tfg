import reflex as rx
from pythontfg.backend.database_conect import Contacto
from pythontfg.backend.database_conect import supabase
from pythontfg.backend.database_conect import Usuario
from typing import List, Optional
from datetime import datetime


class Mensaje(rx.Base):
    mensaje: str = ""
    fecha_hora: str = ""
    enviado: bool = False

class ChatState(rx.State):
    
    user_email: str =""
    selected_contact_chat: Optional[Contacto] = None
    selected_red_social: str = ""
    
    user_input: str = ""
    
    messages: List[Mensaje] = []

    def seleccionar_contacto_chat(self, contacto: Contacto, user_email: str):
        self.user_email = user_email
        self.selected_contact_chat = contacto
        print(f"Contacto seleccionado: {self.selected_contact_chat.nombre}")
        
        self.seleccionar_red_social_disponible()
            
            
    def cargar_mensajes_contacto(self):
        response = (
            supabase
            .from_("mensajes")
            .select("*")
            .eq("user_email", self.user_email)
            .eq("nombre_contacto", self.selected_contact_chat.nombre)
            .eq("red_social", self.selected_red_social)
            .order("fecha_hora", desc=False)
            .execute()
        )

        if response.data:
            self.messages = [
                Mensaje(
                    mensaje=msg["mensaje"],
                    fecha_hora=datetime.fromisoformat(msg["fecha_hora"]).strftime("%H:%M"),
                    enviado=msg["enviado"]
                )
                for msg in response.data
            ]
            print(f"{len(self.messages)} mensajes cargados")  # <-- Confirmación
        else:
            print("No se encontraron mensajes.")

      
        
    
    def seleccionar_red_social_disponible(self):
        redes = {
            "instagram": self.selected_contact_chat.instagram,
            "facebook": self.selected_contact_chat.facebook,
            "twitter": self.selected_contact_chat.twitter,
            "linkedin": self.selected_contact_chat.linkedin,
        }
        for red, valor in redes.items():
            if valor != "":
                self.set_red_social(red)
                break
        else:
            self.selected_red_social = ""


    
    def set_red_social(self, red_social: str):
        self.selected_red_social = red_social
        print(f"Red social cambiada:{self.selected_red_social}")
        if self.selected_red_social != "":
            self.messages = []
            self.cargar_mensajes_contacto()

    def is_all_selected(self) -> bool:
        return self.selected_contact_chat is not None and self.selected_red_social != ""

    def send_message(self):
        if self.user_input.strip():
            now = datetime.utcnow().isoformat()

            nuevo_mensaje = Mensaje(
                mensaje=self.user_input,
                fecha_hora=now,
                enviado=True
            )

            # Guardar en Supabase
            supabase.from_("mensajes").insert({
                "user_email": self.user_email,
                "nombre_contacto": self.selected_contact_chat.nombre,
                "mensaje": nuevo_mensaje.mensaje,
                "fecha_hora": nuevo_mensaje.fecha_hora,
                "enviado": nuevo_mensaje.enviado,
                "red_social": self.selected_red_social
            }).execute()

            nuevo_mensaje.fecha_hora = datetime.fromisoformat(nuevo_mensaje.fecha_hora).strftime("%H:%M")
            # Actualizar en el frontend
            self.messages.append(nuevo_mensaje)
            self.user_input = ""
    



