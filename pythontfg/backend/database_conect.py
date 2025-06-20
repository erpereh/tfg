from supabase import create_client, Client
from typing import Optional
from pythontfg.backend import config

SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

import reflex as rx
import re
from typing import List
import csv
from pathlib import Path

class Contacto(rx.Base):
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    instagram: str = ""
    discord: str = ""
    twitter: str = ""
    linkedin: str = ""



class Usuario(rx.State):
    
    
    #****************************************************************************************
    #******************* TODO ESTO ES PARA EL LOGIN, REGISTRO Y PROFILE *********************
    #****************************************************************************************
    nombre: str = ""
    email: str = ""
    password: str = ""
    error: str = ""
    
    instagram_usr: str = ""
    instagram_pass: str = ""
    discord_usr: str = ""
    discord_pass: str = ""
    telefono: str = ""
    twitter_usr: str = ""
    twitter_pass: str = ""
    linkedin_usr: str = ""
    linkedin_pass: str = ""


    def on_telefono_change(self, value: str):
        self.telefono = value
        self.validar_telefono()
    
    def on_nombre_change(self, value: str):
        self.set_nombre(value)
        self.validar_nombre()
        
    def on_pass_change(self, value: str):
        self.set_password(value)
        self.validar_pass()

    def validar_pass(self):
        
        if len(self.password) < 6:
            self.error = "La contraseña debe tener al menos 6 caracteres."
            return

        self.error = ""  # limpia el error si todo está bien
    
    def validar_nombre(self):

        if len(self.nombre) < 3:
            self.error = "El nombre debe tener al menos 3 caracteres."
            return

        self.error = ""  # limpia el error si todo está bien
    
    def on_email_change(self, value: str):
        self.set_email(value)
        self.validar_email()
    
    def no_mod_email(self, _: str = ""):
        self.error = "No se puede cambiar el email."


    def validar_telefono(self):
        if not self.telefono:
            self.error = "El teléfono no puede estar vacío."
            return

        # Solo 9 dígitos
        pattern = r"^\d{9}$"
        if not re.match(pattern, self.telefono):
            self.error = "El teléfono debe tener exactamente 9 dígitos numéricos."
            return

        self.error = ""  # limpia el error si está bien

    
    def validar_email(self):
        if not self.email:
            self.error = "El correo no puede estar vacío."
            return

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.email):
            self.error = "El formato del correo no es válido."
            return
        self.error = ""  # limpia el error si está bien
        
    
            
    def validar_registro(self):
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("users").select("*").eq("email", self.email).execute()

        if res.data:
            # Usuario repetido, no se puede registrar
            self.error = "Usuario ya existe."
            return
        
        self.validar_nombre()
        if self.error != "":
            return
        self.validar_email()  
        if self.error != "":
            return
        self.validar_pass()
        if self.error != "":
            return
        
        supabase.table("users").insert({"email": self.email, "pass": self.password, "nombre": self.nombre}).execute()
        
        return rx.redirect("/inicio")
    
    def validar_login(self):
        #************************************
        #comentar, solo para desarrollo
        #self.set_email("1@gmail.com")
        #self.set_password("111111")
        #************************************
        
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("users").select("*").eq("email", self.email).eq("pass", self.password).execute()

        if res.data:
            # Usuario encontrado, redirigimos
            self.error = ""
            self.cargar_datos_usr(res)
            self.cargar_contactos()
            self.cargar_estadisticas()
            return rx.redirect("/inicio")
        else:
            # No coincide email/pass
            self.error = "Correo o contraseña incorrectos."
            
            
    def cargar_datos_usr(self, res):
        if not res.data:
            self.error = "No se encontraron datos del usuario."
            return

        datos = res.data[0]

        self.set_nombre(datos.get("nombre", ""))
        self.set_email(datos.get("email", ""))
        self.set_password(datos.get("pass", ""))

        self.instagram_usr = datos.get("instagram_usr", "")
        self.instagram_pass = datos.get("instagram_pass", "")
        self.discord_usr = datos.get("discord_urs", "")
        self.discord_pass = datos.get("discord_pass", "")
        self.telefono = datos.get("telefono", "0")
        self.twitter_usr = datos.get("twitter_usr", "")
        self.twitter_pass = datos.get("twitter_pass", "")
        self.linkedin_usr = datos.get("linkedin_usr", "")
        self.linkedin_pass = datos.get("linkedin_pass", "")
        
        # Imprimir todos los valores para verificar
        print("Usuario cargado:")
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
        print(f"Password: {self.password}")
        print(f"Instagram: {self.instagram_usr} / {self.instagram_pass}")
        print(f"Discord: {self.discord_usr} / {self.discord_pass}")
        print(f"Teléfono: {self.telefono}")
        print(f"Twitter: {self.twitter_usr} / {self.twitter_pass}")
        print(f"LinkedIn: {self.linkedin_usr} / {self.linkedin_pass}")
        
    def guardar_cambios(self, form_data: dict):
        """Valida y actualiza los datos del usuario en Supabase."""

        # Actualiza el estado interno
        self.nombre = form_data.get("nombre", self.nombre)
        # self.email NO se modifica
        self.telefono = form_data.get("telefono", self.telefono)
        self.password = form_data.get("pass", self.password)  # Asegúrate de usar el mismo name del input

        self.instagram_usr = form_data.get("instagram_usr", self.instagram_usr)
        self.instagram_pass = form_data.get("instagram_pass", self.instagram_pass)
        self.discord_usr = form_data.get("discord_usr", self.discord_usr)
        self.discord_pass = form_data.get("discord_pass", self.discord_pass)
        self.twitter_usr = form_data.get("twitter_usr", self.twitter_usr)
        self.twitter_pass = form_data.get("twitter_pass", self.twitter_pass)
        self.linkedin_usr = form_data.get("linkedin_usr", self.linkedin_usr)
        self.linkedin_pass = form_data.get("linkedin_pass", self.linkedin_pass)

        # VALIDACIONES
        self.validar_nombre()
        if self.error:
            return

        self.validar_telefono()
        if self.error:
            return

        self.validar_pass()
        if self.error:
            return

        # Actualiza en la base de datos
        supabase.table("users").update({
            "nombre": self.nombre,
            "pass": self.password,
            "telefono": self.telefono,
            "instagram_usr": self.instagram_usr,
            "instagram_pass": self.instagram_pass,
            "discord_usr": self.discord_usr,
            "discord_pass": self.discord_pass,
            "twitter_usr": self.twitter_usr,
            "twitter_pass": self.twitter_pass,
            "linkedin_usr": self.linkedin_usr,
            "linkedin_pass": self.linkedin_pass,
        }).eq("email", self.email).execute()

        return rx.toast.success("Cambios guardados correctamente", position="top-center")



    def cargar_contactos(self):
        """Carga los contactos del usuario desde Supabase."""
        self.contactos = []  # Limpiar lista previa

        res = supabase.table("contactos").select("*").eq("user_email", self.email).execute()

        if not res.data:
            print("No se encontraron contactos.")
            return

        for contacto_data in res.data:
            contacto = Contacto(
                nombre=contacto_data.get("nombre") or "",
                email=contacto_data.get("email") or "",
                telefono=contacto_data.get("telefono") or "",
                instagram=contacto_data.get("instagram") or "",
                discord=contacto_data.get("discord") or "",
                twitter=contacto_data.get("twitter") or "",
                linkedin=contacto_data.get("linkedin") or ""
            )

            
            self.contactos.append(contacto)
            
        if self.contactos and self.selected_contact is None:
            self.selected_contact = self.contactos[0]
        
        print(f"{len(self.contactos)} contacto(s) cargado(s) correctamente.")
        print(self.contactos)
        

    @rx.event
    def enviar_datos_chat(self):
        from pythontfg.backend.backend_chat import ChatState
        datos = {
            "nombre": self.nombre,
            "instagram_usr": self.instagram_usr,
            "instagram_pass": self.instagram_pass,
            "discord_usr": self.discord_usr,
            "discord_pass": self.discord_pass,
            "twitter_usr": self.twitter_usr,
            "twitter_pass": self.twitter_pass,
            "linkedin_usr": self.linkedin_usr,
            "linkedin_pass": self.linkedin_pass,
            "email": self.email
        }
        return ChatState.cargar_usuario(datos)
    

    def reset_password(self):
        self.error="Pongase en contacto con davidjuliotfg@gmail.com"

    
    #****************************************************************************************
    #******************* TODO ESTO ES PARA EL CREAR CONTACTOS *******************************
    #****************************************************************************************
        
        
    # Campos para añadir un nuevo contacto
    nuevo_nombre: str = ""
    nuevo_email: str = ""
    nuevo_telefono: str = ""
    nuevo_instagram: str = ""
    nuevo_discord: str = ""
    nuevo_twitter: str = ""
    nuevo_linkedin: str = ""
    
    contactos: List[Contacto] = []

    nuevo_error: str = ""

    def nuevo_on_telefono_change(self, value: str):
        self.nuevo_telefono = value
        self.nuevo_validar_telefono()

    def nuevo_on_nombre_change(self, value: str):
        self.nuevo_nombre = value
        self.nuevo_validar_nombre()

    def nuevo_on_email_change(self, value: str):
        self.nuevo_email = value
        self.nuevo_validar_email()
        
    def nuevo_validar_nombre(self):
        if len(self.nuevo_nombre) < 3:
            self.nuevo_error = "El nombre debe tener al menos 3 caracteres."
            return
        self.nuevo_error = ""  # limpia el error si todo está bien

    def nuevo_validar_telefono(self):
        if not self.nuevo_telefono:
            self.nuevo_error = "El teléfono no puede estar vacío."
            return
        # Solo 9 dígitos
        pattern = r"^\d{9}$"
        if not re.match(pattern, self.nuevo_telefono):
            self.nuevo_error = "El teléfono debe tener exactamente 9 dígitos numéricos."
            return
        self.nuevo_error = ""  # limpia el error si está bien

    def nuevo_validar_email(self):
        if not self.nuevo_email:
            self.nuevo_error = "El correo no puede estar vacío."
            return
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.nuevo_email):
            self.nuevo_error = "El formato del correo no es válido."
            return
        self.nuevo_error = ""  # limpia el error si está bien
        
    
    def add_new_user(self):
        print("Añadiendo...")
        self.nuevo_validar_nombre()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        self.nuevo_validar_email()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        self.nuevo_validar_telefono()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        
        # Verifica si ya existe antes de añadir nada
        existing_contact = supabase.table("contactos")\
                .select("nombre")\
                .eq("user_email", self.email)\
                .eq("nombre", self.nuevo_nombre)\
                .execute()

        if existing_contact.data and len(existing_contact.data) > 0:
            return rx.toast.error("El contacto ya existe", position="top-center")

        # Ahora sí puedes crear y añadir el nuevo contacto
        nuevo = Contacto(
            nombre=self.nuevo_nombre,
            email=self.nuevo_email,
            telefono=self.nuevo_telefono,
            instagram=self.nuevo_instagram,
            discord=self.nuevo_discord,
            twitter=self.nuevo_twitter,
            linkedin=self.nuevo_linkedin,
        )
        self.contactos.append(nuevo)

        # Inserta en Supabase
        supabase.table("contactos").insert({
            "nombre": self.nuevo_nombre,
            "email": self.nuevo_email,
            "telefono": self.nuevo_telefono,
            "instagram": self.nuevo_instagram,
            "discord": self.nuevo_discord,
            "twitter": self.nuevo_twitter,
            "linkedin": self.nuevo_linkedin,
            "user_email": self.email
        }).execute()

        self.load_entries()
        return rx.toast.success("Contacto creado correctamente", position="top-center")

    
    def modificar_contacto(self, nombre_contacto:str):
        print("modificando...")
        self.nuevo_validar_nombre()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        self.nuevo_validar_email()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        self.nuevo_validar_telefono()
        if self.nuevo_error:
            return rx.toast.error(self.nuevo_error, position="top-center")
        
        supabase.table("contactos")\
                .update({
                    "nombre": self.nuevo_nombre,
                    "email": self.nuevo_email,
                    "telefono": self.nuevo_telefono,
                    "instagram": self.nuevo_instagram,
                    "discord": self.nuevo_discord,
                    "twitter": self.nuevo_twitter,
                    "linkedin": self.nuevo_linkedin,
                })\
                .eq("user_email", self.email)\
                .eq("nombre", nombre_contacto)\
                .execute()
        
        #borra el anterior contacto de la lista y añade el nuevo
        self.contactos = [c for c in self.contactos if c.nombre != nombre_contacto]
        self.contactos.append(Contacto(
            nombre=self.nuevo_nombre,
            email=self.nuevo_email,
            telefono=self.nuevo_telefono,
            instagram=self.nuevo_instagram,
            discord=self.nuevo_discord,
            twitter=self.nuevo_twitter,
            linkedin=self.nuevo_linkedin,
        ))
        self.load_entries()
        return rx.toast.success("Contacto modificado correctamente", position="top-center")
    
    
    def resetear_campos_nuevos(self):
        # Resetea campos del formulario
        self.nuevo_nombre = ""
        self.nuevo_email = ""
        self.nuevo_telefono = ""
        self.nuevo_instagram = ""
        self.nuevo_discord = ""
        self.nuevo_twitter = ""
        self.nuevo_linkedin = ""

    selected_contact: Optional[Contacto] = None
    
    # Método para actualizar la selección de contacto.
    def seleccionar_contacto(self, contacto: Contacto):
        self.set_selected_contact(contacto)
        # Opcional: preparar el formulario con los datos del contacto.
        self.preparar_formulario(contacto)

    def preparar_formulario(self, contacto: Contacto):
        self.nuevo_nombre = contacto.nombre
        self.nuevo_email = contacto.email
        self.nuevo_telefono = contacto.telefono or ""
        self.nuevo_instagram = contacto.instagram or ""
        self.nuevo_discord = contacto.discord or ""
        self.nuevo_twitter = contacto.twitter or ""
        self.nuevo_linkedin = contacto.linkedin or ""


    # ESTO ES PARA ELIMINAR CONTACTOS
    def eliminar_contacto(self, nombre_contacto: str):
        """Elimina un contacto del usuario actual por nombre."""
        """if not nombre_contacto:
            print("Debe proporcionar el nombre del contacto a eliminar.")
            return"""

        # Elimina en la base de datos
        supabase.table("contactos")\
            .delete()\
            .eq("user_email", self.email)\
            .eq("nombre", nombre_contacto)\
            .execute()

        # También lo elimina de la lista local
        self.contactos = [c for c in self.contactos if c.nombre != nombre_contacto]
        #self.load_entries()
        print(f"Contacto '{nombre_contacto}' eliminado correctamente de {self.email}.")


    #****************************************************************************************
    #************************ TODO ESTO ES PARA LA TABLA DE CONTACTOS ***********************
    #****************************************************************************************
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    offset: int = 0
    limit: int = 10  # Número de filas por página

    @rx.event
    def load_entries(self):
        self.cargar_contactos()


    @rx.var
    def filtered_sorted_items(self) -> List[Contacto]:
        items = self.contactos

        # Ordenamiento
        sort_field = self.sort_value
        if sort_field == "teléfono":
            sort_field = "telefono"

        if sort_field:
            items = sorted(
                items,
                key=lambda item: str(getattr(item, sort_field)).lower(),
                reverse=self.sort_reverse,
            )

        # Búsqueda
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in ["nombre", "email", "telefono", "instagram", "discord", "twitter", "linkedin"]
                )
            ]

        return items

    @rx.var
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var
    def total_pages(self) -> int:
        total = len(self.filtered_sorted_items)
        return (total // self.limit) + (1 if total % self.limit else 0) or 1

    @rx.var(initial_value=[])
    def get_current_page(self) -> list[Contacto]:
        items = self.filtered_sorted_items
        start_index = self.offset
        end_index = self.offset + self.limit
        return items[start_index:end_index]


    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def set_search_value(self, value: str):
        self.search_value = value
        self.offset = 0  # Reiniciar página al buscar

    def set_sort_value(self, value: str):
        if value == "teléfono":
            value = "telefono"
        self.sort_value = value
        self.offset = 0  # Reiniciar página al ordenar

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.offset = 0  # Reiniciar al cambiar el orden

    def load_entries(self):
        self.cargar_contactos()

    def export_to_csv(self):
        """Genera un CSV actualizado con los contactos y lo pone disponible para descargar."""
        self.load_entries()  # <-- Asegúrate de que tienes los datos más recientes

        file_path = Path("assets/contactos.csv")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Email", "Teléfono", "Instagram", "Discord", "Twitter", "LinkedIn"])
            for contacto in self.contactos:
                writer.writerow([
                    contacto.nombre,
                    contacto.email,
                    contacto.telefono,
                    contacto.instagram,
                    contacto.discord,
                    contacto.twitter,
                    contacto.linkedin,
                ])

        return rx.download(url="/contactos.csv")



    #****************************************************************************************
    #******************* TODO ESTO ES PARA LAS ESTADÍSTICAS DEL OVERVIEW ********************
    #****************************************************************************************
    stat_num_mensajes=0
    stat_media_redes_sociales_disponibles_por_contacto = 0.0
    
    stat_cont_instagram=0
    stat_cont_discord=0
    stat_cont_twitter=0
    stat_cont_linkedin=0

    datos_formato_grafico_circular: List[dict] = []
    
    
    class Mensaje_stat(rx.Base):
        fecha: str = ""
        enviado: bool = False

    mensajes_stats: List[Mensaje_stat]
    tipo_diagrama: bool = True
    tipo_mensaje_seleccionado: str = "enviados"
    enviados_data = []
    recibidos_data = []
    todos_data = []


    def cargar_estadisticas(self):
        res = supabase.table("mensajes").select("*").eq("user_email", self.email).execute()

        if res.data is not None:
            self.stat_num_mensajes = len(res.data)
            #carga en mensajes_stats los mensajes de los últimos 30 días
            self.mensajes_stats = [
                self.Mensaje_stat(
                    fecha=msg["fecha_hora"],
                    enviado=msg["enviado"]
                )
                for msg in res.data
            ]
            self.generar_datos_estadisticos_por_fecha()
        else:
            self.stat_num_mensajes = 0

        for c in self.contactos:
            if c.instagram != "":
                self.stat_cont_instagram += 1
            if c.discord != "":
                self.stat_cont_discord += 1
            if c.twitter != "":
                self.stat_cont_twitter += 1
            if c.linkedin != "":
                self.stat_cont_linkedin += 1
                
                
        cont = self.stat_cont_instagram + self.stat_cont_discord + self.stat_cont_twitter + self.stat_cont_linkedin

        total_contactos = len(self.contactos)
        if total_contactos > 0:
            self.stat_media_redes_sociales_disponibles_por_contacto = cont / total_contactos
        else:
            self.stat_media_redes_sociales_disponibles_por_contacto = 0.0
            
        self.datos_formato_grafico_circular = [
            {"name": "Instagram", "value": self.stat_cont_instagram, "fill": "#E1306C"},  # rosa Instagram
            {"name": "Discord", "value": self.stat_cont_discord, "fill": "#843797"},      # azul oscuro Discord
            {"name": "Twitter", "value": self.stat_cont_twitter, "fill": "#A9DDFF"},      # azul Twitter
            {"name": "Linkedin", "value": self.stat_cont_linkedin, "fill": "#0077B5"},    # azul LinkedIn
        ]


    def generar_datos_estadisticos_por_fecha(self):
        
        from collections import defaultdict
        from datetime import datetime, timedelta
        # Diccionarios para acumular recuentos
        enviados_por_dia = defaultdict(int)
        recibidos_por_dia = defaultdict(int)
        todos_por_dia = defaultdict(int)

        # Rellenamos los diccionarios desde los mensajes_stats
        for msg in self.mensajes_stats:
            try:
                fecha = msg.fecha[:10]  # extrae YYYY-MM-DD
                fecha_clave = datetime.strptime(fecha, "%Y-%m-%d").strftime("%m-%d")

                if msg.enviado:
                    enviados_por_dia[fecha_clave] += 1
                else:
                    recibidos_por_dia[fecha_clave] += 1
                todos_por_dia[fecha_clave] += 1
            except Exception as e:
                print("Error procesando mensaje:", msg.fecha, e)

        # Limpiamos las listas antes de rellenarlas
        self.enviados_data.clear()
        self.recibidos_data.clear()
        self.todos_data.clear()

        # Para los últimos 30 días (incluyendo hoy)
        for i in range(30, -1, -1):
            fecha_actual = (datetime.now() - timedelta(days=i)).strftime("%m-%d")

            self.enviados_data.append({
                "Date": fecha_actual,
                "Enviados": enviados_por_dia[fecha_actual],
            })

            self.recibidos_data.append({
                "Date": fecha_actual,
                "Recibidos": recibidos_por_dia[fecha_actual],
            })

            self.todos_data.append({
                "Date": fecha_actual,
                "Todos": todos_por_dia[fecha_actual],
            })


    def set_tipo_mensaje(self, tab: str | list[str]):
        self.tipo_mensaje_seleccionado = tab if isinstance(tab, str) else tab[0]
    
    def cambio_tipo_diagrama(self):
        self.tipo_diagrama = not self.tipo_diagrama

