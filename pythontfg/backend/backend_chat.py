import reflex as rx
from pythontfg.backend.api_conect import recargar_facebook, recargar_instagram, recargar_linkedin, recargar_twitter
from pythontfg.backend.calendar import crear_evento_google_calendar
from pythontfg.backend.mensaje import Mensaje
from pythontfg.backend.database_conect import Contacto
from pythontfg.backend.usuario_ligero import UsuarioLigero  # si lo metes en archivo aparte
from pythontfg.backend.database_conect import supabase
from pythontfg.backend.config import KEY_OPEN_ROUTER, BASE_URL_OPEN_ROUTER
from typing import List, Optional
from datetime import datetime
from openai import OpenAI

client = OpenAI(
  base_url=BASE_URL_OPEN_ROUTER,
  api_key=KEY_OPEN_ROUTER,
)


class ChatState(rx.State):
    
    user: Optional[UsuarioLigero] = None


    selected_contact_chat: Optional[Contacto] = None
    selected_red_social: str = ""
    
    user_input: str = ""
    
    messages: List[Mensaje] = []

    is_generating_ia: bool = False

    @rx.event
    def cargar_usuario(self, datos: dict):
        self.user = UsuarioLigero(**datos)
        print(f"Usuario cargado en ChatState: {self.user.email}")

    
    @rx.event
    async def seleccionar_contacto_chat(self, contacto: Contacto):
        self.selected_contact_chat = contacto
        print(f"Contacto seleccionado: {self.selected_contact_chat.nombre}")
        return type(self).seleccionar_red_social_disponible()

            
    @rx.event
    async def cargar_mensajes_contacto(self):
        response = (
            supabase
            .from_("mensajes")
            .select("*")
            .eq("user_email", self.user)
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

            print(f"{len(self.messages)} mensajes cargados")

            ult_mensaje_recibido = next((m for m in reversed(self.messages) if not m.enviado), None)
            if ult_mensaje_recibido:
                print(f"+++++++++++++ Mensaje: {ult_mensaje_recibido.mensaje}")
                return type(self).search_event(ult_mensaje_recibido)
        else:
            print("No se encontraron mensajes.")


    
    @rx.event
    async def seleccionar_red_social_disponible(self):
        redes = {
            "instagram": self.selected_contact_chat.instagram,
            "facebook": self.selected_contact_chat.facebook,
            "twitter": self.selected_contact_chat.twitter,
            "linkedin": self.selected_contact_chat.linkedin,
        }
        for red, valor in redes.items():
            if valor != "":
                return type(self).set_red_social(red)
        self.selected_red_social = ""




    
    @rx.event
    async def set_red_social(self, red_social: str):
        self.selected_red_social = red_social
        print(f"Red social cambiada:{self.selected_red_social}")
        if self.selected_red_social != "":
            self.messages = []
            return type(self).cargar_mensajes_contacto()



    def is_all_selected(self) -> bool:
        return self.selected_contact_chat is not None and self.selected_red_social != ""

    def send_message(self):
        if self.user_input.strip():
            now = datetime.now().isoformat()

            nuevo_mensaje = Mensaje(
                mensaje=self.user_input,
                fecha_hora=now,
                enviado=True
            )

            # Guardar en Supabase
            supabase.from_("mensajes").insert({
                "user_email": self.user.email,
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
            
    @rx.event
    async def reload_messages(self):
        print(f"Recargando mensajes de {self.selected_red_social}...")


        match self.selected_red_social:
            case "instagram":
                nuevos_mensajes = recargar_instagram(
                    self.user.instagram_usr,
                    self.user.instagram_pass,
                    self.selected_contact_chat.instagram
                )
            case "twitter":
                nuevos_mensajes = recargar_twitter(self.selected_contact_chat.twitter)
            case "facebook":
                nuevos_mensajes = recargar_facebook(self.selected_contact_chat.facebook)
            case "linkedin":
                nuevos_mensajes = recargar_linkedin(self.selected_contact_chat.linkedin)
            case _:
                print("Red social no reconocida.")
                nuevos_mensajes = []

        self.messages.extend(nuevos_mensajes)





    
    #****************************************************************************************
    #******************* TODO ESTO ES DETECTAR EVENTO CON IA ********************************
    #****************************************************************************************
    
    @rx.event(background=True)
    async def search_event(self, message: Mensaje):
        async with self:
            pass  # Aquí podrías poner un flag como self.is_generating_event = True si lo necesitas
        yield  # Para notificar al cliente que hay un cambio (aunque no lo uses visualmente aún)

        history = [
            {"role": "user", "content": message.mensaje}
        ]

        hoy = datetime.now().strftime("%Y-%m-%d")

        system_prompt = {
            "role": "system",
            "content": (
                f"Hoy es {hoy}. Debes coger el contenido del mensaje, en caso de que sea un futuro evento, "
                "localizarás el título, su fecha y hora y su duración. "
                "El formato que debes poner será el siguiente: evento:título_evento|fecha:AAAA-MM-DDTHH:MM:SS|duracion:HH. "
                "En caso de que no se localice un evento o una fecha, debes devolver evento:null|fecha:null|duracion:null. "
                "En caso de que no se localice una hora concreta pero sí una fecha y evento, deberás poner: evento:título_evento|fecha:AAAA-MM-DDT00:00:00|duracion:24. "
                "En caso de que no se localice una duración concreta, se debe estimar según el tipo de evento en horas, siendo el mínimo 1 hora."
                "El formato de tu respuesta debe ser claro, sin añadir comentarios ni otros formatos, un ejemplo sería: evento:Reunión con Juan y Luis|fecha:2025-05-15T17:00:00|duracion:01"
            )
        }

        api_messages = [system_prompt] + history

        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=api_messages,
            )

            if not response or not response.choices:
                print("La respuesta de la IA es nula o vacía")
                return

            ia_text = response.choices[0].message.content.strip()
            print("Respuesta IA:", ia_text)


            # Parsear la respuesta tipo: "evento:Reunión|fecha:2025-05-11T15:00:00|duracion:1"
            partes = ia_text.split("|")
            evento = partes[0].split("evento:")[1].strip()
            fecha_str = partes[1].split("fecha:")[1].strip()
            duracion_str = partes[2].split("duracion:")[1].strip()

            if evento != "null" and fecha_str != "null":
                fecha_dt = datetime.fromisoformat(fecha_str)
                try:
                    duracion = float(duracion_str)
                except ValueError:
                    duracion = 1.0  # Valor por defecto si la IA se equivoca
                print(f"Evento registrado: {evento}, hora evento {fecha_str}, duración: {duracion}h")
                async with self:
                    message.evento = evento
                    message.fecha_dt = fecha_dt
                    message.duracion = duracion
                    message.evento_localizado = True

                    # Reemplaza el mensaje dentro del array para que Reflex detecte el cambio
                    for i, m in enumerate(self.messages):
                        if m.mensaje == message.mensaje and not m.enviado:
                            self.messages[i] = message
                            break
                yield  # Notifica a Reflex el cambio de estado
            else:
                print("No se detectó ningún evento o fecha útil.")

        except Exception as e:
            print("Error procesando el evento:", e)

        yield  # Cierre del evento en Reflex (aunque no cambies estado, es buena práctica)


    @rx.event
    def confirmar_evento(self, index: int):
        mensaje = self.messages[index]
        if mensaje.evento_localizado:
            crear_evento_google_calendar(mensaje.evento, mensaje.fecha_dt, mensaje.duracion)

    
    #****************************************************************************************
    #******************* TODO ESTO ES PARA GENERAR MENSAJE CON IA ***************************
    #****************************************************************************************

    @rx.event(background=True)
    async def write_with_ia(self):
        async with self:
            self.is_generating_ia = True
        yield  # <- informa al cliente que hay un cambio de estado

        history = [
            {"role": "user" if m.enviado else "assistant", "content": m.mensaje}
            for m in self.messages
        ]

        system_prompt = {
            "role": "system",
            "content": "Eres una persona muy maja que se hace pasar por la persona original respondiendo mensajes de redes sociales, debes comportarte como tal y no hacer preguntas como, ¿tienes mas dudas?. Responde de forma amigable. Respondes con mesajes cortos, propios de un chat."
        }

        api_messages = [system_prompt] + history

        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=api_messages,
        )

        ia_text = response.choices[0].message.content
        
        async with self:
            self.user_input = ia_text
            self.is_generating_ia = False
        yield  # <- informa al cliente que hay un cambio de estado

        """
        EN CASO DE QUIERER GUARDAR EN LA BASE DE DATOS
        now = datetime.now().isoformat()
        async with self:
            mensaje_ia = Mensaje(mensaje=ia_text, fecha_hora=now, enviado=False)
            self.messages.append(mensaje_ia)
            self.user_input = ia_text
            self.is_generating_ia = False
        yield  # <- para que Reflex actualice la UI
    
        """