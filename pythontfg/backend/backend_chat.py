from pythontfg.backend.social_apis.discord import enviar_mensaje_discord, recargar_discord
from pythontfg.backend.social_apis.instagram import enviar_mensaje_instagram, recargar_instagram
from pythontfg.backend.social_apis.linkedin import enviar_mensaje_linkedin, recargar_linkedin
from pythontfg.backend.social_apis.twitter import enviar_mensaje_twitter, recargar_twitter
import reflex as rx
from pythontfg.backend.social_apis.calendar import crear_evento_google_calendar
from pythontfg.backend.mensaje import Mensaje
from pythontfg.backend.database_conect import Contacto
from pythontfg.backend.usuario_ligero import UsuarioLigero  # si lo metes en archivo aparte
from pythontfg.backend.database_conect import supabase
from pythontfg.backend.config import KEY_OPEN_ROUTER, BASE_URL_OPEN_ROUTER
from typing import List, Optional
from datetime import datetime
from openai import OpenAI
from pythontfg.backend.config import DS_TOKEN

import asyncio

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
            .eq("user_email", self.user.email)
            .eq("nombre_contacto", self.selected_contact_chat.nombre)
            .eq("red_social", self.selected_red_social)
            .order("fecha_hora", desc=False)
            .execute()
        )

        if response.data:
            self.messages = [
                Mensaje(
                    mensaje=msg["mensaje"],
                    fecha_hora=msg["fecha_hora"],
                    hora_formato_chat=datetime.fromisoformat(msg["fecha_hora"]).strftime("%H:%M"),
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
            "discord": self.selected_contact_chat.discord,
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
        
    @rx.event
    def send_message(self):
        if not self.user_input.strip():
            return

        texto = self.user_input  # capturamos el texto
        now_iso = datetime.now().isoformat()
        hora_formato = datetime.fromisoformat(now_iso).strftime("%H:%M")
        nuevo_mensaje = Mensaje(
            mensaje=texto,
            fecha_hora=now_iso,
            hora_formato_chat=hora_formato,
            enviado=True
        )

        # Guardar en Supabase
        supabase.from_("mensajes").insert({
            "user_email": self.user.email,
            "nombre_contacto": self.selected_contact_chat.nombre,
            "mensaje": nuevo_mensaje.mensaje,
            "fecha_hora": nuevo_mensaje.fecha_hora,
            "enviado": True,
            "red_social": self.selected_red_social
        }).execute()

        # Enviar en background, pasándole el texto
        asyncio.create_task(self.send_message_to_red_social(texto))

        # Append y limpiar input
        self.messages.append(nuevo_mensaje)
        self.user_input = ""

    async def send_message_to_red_social(self, texto: str):
        print(f"Enviando mensaje a {self.selected_red_social}: {texto!r}")
        match self.selected_red_social:
            case "discord":
                usuario_id = 460702684094136320  # ID del usuario de Discord
                # Ejecuta el wrapper síncrono en un thread con el texto correcto
                await asyncio.to_thread(
                    enviar_mensaje_discord,
                    self.user.discord_pass,
                    usuario_id,
                    texto,
                )
            case "instagram":
                await asyncio.to_thread(
                    enviar_mensaje_instagram,
                    self.user.instagram_usr,
                    texto,
                    self.selected_contact_chat.instagram
                )
            case "twitter":
                await asyncio.to_thread(
                    enviar_mensaje_twitter,
                    self.user.twitter_usr,
                    texto,
                    self.selected_contact_chat.twitter
                )
            case "linkedin":
                await asyncio.to_thread(
                    enviar_mensaje_linkedin,
                    self.user.linkedin_usr,
                    texto,
                    self.selected_contact_chat.linkedin
                )
            case _:
                print("Red social no reconocida.")
    
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
            case "discord":
                #ESTO HAY Q CAMBIARLO
                usuario_id = 460702684094136320
                
                try:
                    # Función síncrona, pero corre su event loop interno
                    nuevos_mensajes = await asyncio.to_thread(
                        recargar_discord,
                        self.user.discord_pass,
                        usuario_id,
                        20
                    )
                except Exception as e:
                    print("Error al recargar Discord:", e)
                    nuevos_mensajes = []
            case "linkedin":
                nuevos_mensajes = recargar_linkedin(self.selected_contact_chat.linkedin)
            case _:
                print("Red social no reconocida.")
                nuevos_mensajes = []

        mensajes_comprobados = self.comprobarRepetidos(nuevos_mensajes)
        self.add_mensajes_comprobados_to_supabase(mensajes_comprobados)
        # Aquí se cargan los mensajes actualizados desde Supabase
        return type(self).cargar_mensajes_contacto()

        
    def comprobarRepetidos(self, mensajes: list[Mensaje]) -> list[Mensaje]:
        mensajes_filtrados = []

        for m in mensajes:
            if all(m.mensaje != m_g.mensaje for m_g in self.messages):
                mensajes_filtrados.append(m)

        return mensajes_filtrados


    def add_mensajes_comprobados_to_supabase(self, mensajes: list[Mensaje]):
        for m in mensajes:
            print(f"subiendo a supabase {m.mensaje}")
            supabase.from_("mensajes").insert({
                "user_email": self.user.email,
                "nombre_contacto": self.selected_contact_chat.nombre,
                "mensaje": m.mensaje,
                "fecha_hora": m.fecha_hora,
                "enviado": m.enviado,
                "red_social": self.selected_red_social
            }).execute()




    
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