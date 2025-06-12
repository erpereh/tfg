from pythontfg.backend.social_apis.discord import enviar_mensaje_discord, recargar_discord
from pythontfg.backend.social_apis.instagram import enviar_mensaje_instagram, recargar_instagram
from pythontfg.backend.social_apis.linkedin import LinkedInMessaging
from pythontfg.backend.social_apis.twitter import enviar_mensaje_twitter, recargar_twitter
import reflex as rx
from pythontfg.backend.social_apis.calendar_api import crear_evento_google_calendar
from pythontfg.backend.mensaje import Mensaje
from pythontfg.backend.database_conect import Contacto
from pythontfg.backend.database_conect import Usuario
from pythontfg.backend.usuario_ligero import UsuarioLigero  # si lo metes en archivo aparte
from pythontfg.backend.database_conect import supabase
from pythontfg.backend.config import KEY_OPEN_ROUTER, BASE_URL_OPEN_ROUTER, MODEL
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
    
    linkedin_chat_id = "qkVWRx4mXVKdgkXZXBAFQQ"
    linkedin_dsn = "IOKmnCf0Q-25BAabPas_fQ_MESSAGING"
    user: Optional[UsuarioLigero] = None


    selected_contact_chat: Optional[Contacto] = None
    selected_red_social: str = ""
    
    user_input: str = ""
    
    mensajes: List[Mensaje] = []

    is_generating_ia: bool = False
    
    is_chat: bool = False  # Para saber si es el chatbot o no
    
    mensajes_filtrados_list: List[Mensaje] = []
    

    @rx.event
    def set_is_chat(self, value: bool):
        self.is_chat = value

    
    def mensajes_filtrados(self) -> List[Mensaje]:
        return [m for m in self.mensajes if m.modo_chat == self.is_chat]
    
    @rx.event
    def actualizar_mensajes_filtrados(self):
        self.mensajes_filtrados_list = self.mensajes_filtrados()

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
            self.mensajes = [
                Mensaje(
                    mensaje=msg["mensaje"],
                    fecha_hora=msg["fecha_hora"],
                    hora_formato_chat=datetime.fromisoformat(msg["fecha_hora"]).strftime("%H:%M"),
                    enviado=msg["enviado"],
                    modo_chat=msg["modo_chat"] if msg["modo_chat"] is not None else False
                )
                for msg in response.data
            ]
            
            self.mensajes_filtrados_list = self.mensajes_filtrados()
            
            print(f"is_chat: {self.is_chat}")
            print(f"mensajes totales: {len(self.mensajes)}")
            print(f"mensajes filtrados: {len(self.mensajes_filtrados_list)}")

            print(f"{len(self.mensajes)} mensajes cargados")

            if self.is_chat:
                ult_mensaje_recibido = next((m for m in reversed(self.mensajes_filtrados_list) if not m.enviado), None)
                if ult_mensaje_recibido:
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
            self.mensajes = []
            self.mensajes_filtrados_list = self.mensajes_filtrados()
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
            enviado=True,
            modo_chat=self.is_chat
        )

        # Guardar en Supabase
        supabase.from_("mensajes").insert({
            "user_email": self.user.email,
            "nombre_contacto": self.selected_contact_chat.nombre,
            "mensaje": nuevo_mensaje.mensaje,
            "fecha_hora": nuevo_mensaje.fecha_hora,
            "enviado": True,
            "red_social": self.selected_red_social,
            "modo_chat": self.is_chat
        }).execute()

        # Enviar en background, pasándole el texto
        asyncio.create_task(self.send_message_to_red_social(texto))

        # Append y limpiar input
        self.mensajes.append(nuevo_mensaje)
        self.mensajes_filtrados_list = self.mensajes_filtrados()
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
                    self.user.instagram_pass,
                    texto,
                    self.selected_contact_chat.instagram
                )
            case "twitter":
                await enviar_mensaje_twitter(
                    self.user.twitter_usr,
                    self.user.email,
                    self.user.twitter_pass,
                    texto,
                    self.selected_contact_chat.twitter
                )
            case "linkedin":
                
                linkedin = LinkedInMessaging(self.linkedin_dsn)
                await asyncio.to_thread(
                    linkedin.enviar_mensajes_linkedin,
                    self.linkedin_chat_id,
                    texto
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
                nuevos_mensajes = await recargar_twitter(
                    self.user.twitter_usr,
                    self.user.email,
                    self.user.twitter_pass,
                    self.selected_contact_chat.twitter
                )
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
                    print(f"Recargados {len(nuevos_mensajes)} mensajes de Discord.")
                except Exception as e:
                    print("Error al recargar Discord:", e)
                    nuevos_mensajes = []
            case "linkedin":
                linkedin = LinkedInMessaging(self.linkedin_dsn)
                try:
                    nuevos_mensajes = await asyncio.to_thread(
                        linkedin.recargar_linkedin,
                        self.linkedin_chat_id
                    )
                    print(f"Recargados {len(nuevos_mensajes)} mensajes de LinkedIn.")
                except Exception as e:
                    print("Error al recargar LinkedIn:", e)
                    nuevos_mensajes = []
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
            if all(m.mensaje != m_g.mensaje for m_g in self.mensajes):
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
                "red_social": self.selected_red_social,
                "modo_chat": m.modo_chat
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
                f"Hoy es {hoy}. Tu única tarea es detectar si hay un evento futuro en el siguiente mensaje. "
                "Debes responder exclusivamente en este formato (sin comillas ni comentarios):\n"
                "evento:TÍTULO_DEL_EVENTO|fecha:AAAA-MM-DDTHH:MM:SS|duracion:HH\n"
                "En caso de que no se localice una hora concreta pero sí una fecha y evento, deberás poner: evento:título_evento|fecha:AAAA-MM-DDT00:00:00|duracion:24. "
                "En caso de que no se localice una duración concreta, se debe estimar según el tipo de evento en horas, siendo el mínimo 1 hora."
                "O si no detectas ningún evento:\n"
                "evento:null|fecha:null|duracion:null\n"
                "No respondas con ningún otro texto fuera de ese formato."
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
                    for i, m in enumerate(self.mensajes):
                        if m.mensaje == message.mensaje and not m.enviado:
                            self.mensajes[i] = message
                            break
                        
                    self.mensajes_filtrados_list = self.mensajes_filtrados()

                yield  # Notifica a Reflex el cambio de estado
            else:
                print("No se detectó ningún evento o fecha útil.")

        except Exception as e:
            print("Error procesando el evento:", e)

        yield  # Cierre del evento en Reflex (aunque no cambies estado, es buena práctica)


    @rx.event
    def confirmar_evento(self, index: int):
        mensaje = self.mensajes[index]
        if mensaje.evento_localizado:
            crear_evento_google_calendar(mensaje.evento, mensaje.fecha_dt, mensaje.duracion)

    
    #****************************************************************************************
    #************** TODO ESTO ES PARA GENERAR MENSAJE CON IA EN MODO NORMAL *****************
    #****************************************************************************************
    @rx.event(background=True)
    async def write_with_ia(self):
        async with self:
            self.is_generating_ia = True
        yield  # informa al cliente que hay un cambio de estado

        # 1) Selección y recorte del historial (últimos 3 mensajes)
        MAX_HISTORY = 3
        recent_msgs = self.mensajes_filtrados()[-MAX_HISTORY:]

        # 2) Construcción de 'history' con roles
        history = []
        for m in recent_msgs:
            role = "user" if m.enviado else "assistant"
            history.append({"role": role, "content": m.mensaje})
            
        print (f"Historial para IA: {history}")

        # 3) Prompt del sistema (simulación de usuario)
        system_prompt = {
            "role": "system",
            "content": (
                "Imita al usuario real en esta conversación de red social. "
                "Habla de forma natural, breve y con su estilo personal "
                "(por ejemplo, emojis, giros coloquiales). "
                "No menciones que eres una IA ni referencias a chats anteriores fuera de este contexto."
            ),
        }

        # 4) Ensamblaje de la lista de mensajes para la API
        api_messages = [system_prompt] + history

        # 5) Llamada a la API de OpenAI
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=api_messages,
            )
            ia_text = response.choices[0].message.content
            print(f"Modo chat (simulación usuario): {ia_text}")
        except Exception as e:
            # En caso de error, volcamos el último ia_text (o un valor por defecto) y salimos
            async with self:
                self.is_generating_ia = False
            yield
            return  # detenemos la función para no seguir procesando

        # 6) Volcar directamente la respuesta en el input del usuario
        async with self:
            self.user_input = ia_text
            self.is_generating_ia = False
        yield  # informa al cliente que hay un cambio de estado


    #****************************************************************************************
    #************* TODO ESTO ES PARA GENERAR MENSAJE CON IA EN MODO CHATBOT ***************** 
    #****************************************************************************************
    @rx.event(background=True)
    async def send_message_chatbot(self):
        async with self:
            self.is_generating_ia = True
        yield  # informa al cliente que hay un cambio de estado

        # 1) Selección y recorte del historial (últimos 10 mensajes)
        MAX_HISTORY = 5
        recent_msgs = (self.mensajes)[-MAX_HISTORY:]

        # 2) Construcción de 'history' con roles y etiquetas en el contenido
        history = []
        for m in recent_msgs:
            if m.enviado:
                # Tú escribiste esto (da igual si era al contacto o a la IA)
                role = "user"
                content = f"[{self.user.nombre}] {m.mensaje}"
            else:
                # Mensaje recibido (contacto o chatbot)
                role = "assistant"
                if m.modo_chat:
                    # Vino del contacto
                    content = f"[{self.selected_contact_chat.nombre}] {m.mensaje}"
                else:
                    # Vino de tu propio chatbot en iteraciones previas
                    content = f"[CHATBOT] {m.mensaje}"
            history.append({"role": role, "content": content})

        # 3) Prompt del sistema (chatbot empático)
        system_prompt = {
            "role": "system",
            "content": (
                f"Eres el asistente personal de {self.user.nombre}. "
                "Tu tarea es leer la conversación y ofrecer consejos prácticos de forma empática, "
                "como lo haría un amigo cercano en tercera persona. "
                f"Cuando respondas, comienza dirigiéndote a {self.user.nombre} por su nombre y da tu consejo con calidez. "
                f"Ten en cuenta que este contexto es un chat entre {self.user.nombre} y sus contactos, "
                "podrás saber que mensajes son del usuario y cuáles de sus contactos por el formato: "
                f"[NombreContacto] mensaje del contacto o [{self.user.nombre}] mensaje del usuario. "
                "No menciones que eres una IA ni hagas referencia a un chat o plataforma."
            ),
        }

        # 4) Ensamblaje de la lista de mensajes para la API
        api_messages = [system_prompt] + history

        # 5) Llamada a la API de OpenAI
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=api_messages,
            )
            ia_text = response.choices[0].message.content
            print(f"Modo chatbot: {ia_text}")
        except Exception as e:
            async with self:
                self.is_generating_ia = False
            yield
            return

        # 6) Guardar y persistir mensajes
        async with self:
            now_iso = datetime.now().isoformat()
            hora_formato = datetime.fromisoformat(now_iso).strftime("%H:%M")

            mensaje_usuario = Mensaje(
                mensaje=self.user_input,
                fecha_hora=now_iso,
                hora_formato_chat=hora_formato,
                enviado=True,
                modo_chat=False
            )
            respuesta_ia = Mensaje(
                mensaje=ia_text,
                fecha_hora=now_iso,
                hora_formato_chat=hora_formato,
                enviado=False,
                modo_chat=False
            )

            self.mensajes.extend([mensaje_usuario, respuesta_ia])
            self.mensajes_filtrados_list = self.mensajes_filtrados()
            self.user_input = ""

            supabase.from_("mensajes").insert([
                {
                    "user_email": self.user.email,
                    "nombre_contacto": self.selected_contact_chat.nombre if self.selected_contact_chat else "",
                    "mensaje": mensaje_usuario.mensaje,
                    "fecha_hora": mensaje_usuario.fecha_hora,
                    "enviado": True,
                    "red_social": self.selected_red_social,
                    "modo_chat": False
                },
                {
                    "user_email": self.user.email,
                    "nombre_contacto": self.selected_contact_chat.nombre if self.selected_contact_chat else "",
                    "mensaje": respuesta_ia.mensaje,
                    "fecha_hora": respuesta_ia.fecha_hora,
                    "enviado": False,
                    "red_social": self.selected_red_social,
                    "modo_chat": False
                }
            ]).execute()

            self.is_generating_ia = False
        yield  # informa al cliente que hay un cambio de estado
