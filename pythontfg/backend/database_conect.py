from supabase import create_client, Client
from typing import Optional


SUPABASE_URL = "https://kpwbkzdjqgginzpfcpsd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtwd2JremRqcWdnaW56cGZjcHNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2NTYxMzUsImV4cCI6MjA2MDIzMjEzNX0.pBbx1E1vxNa1FunK0rXau--7SoA9934S7ISWixm-i2M"

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
    facebook: str = ""
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
    facebook_usr: str = ""
    facebook_pass: str = ""
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
    
    def no_se_puede_cambiar_email(self, value: str):
        self.error = "No se puede cambiar el email."
        return

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
        
        return rx.redirect("/overview")
    
    def validar_login(self):
        #************************************
        #comentar, solo para desarrollo
        self.set_email("1@gmail.com")
        self.set_password("1")
        #************************************
        
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("users").select("*").eq("email", self.email).eq("pass", self.password).execute()

        if res.data:
            # Usuario encontrado, redirigimos
            self.error = ""
            self.cargar_datos_usr(res)
            self.cargar_contactos()
            return rx.redirect("/overview")
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
        self.facebook_usr = datos.get("facebook_usr", "")
        self.facebook_pass = datos.get("facebook_pass", "")
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
        print(f"Facebook: {self.facebook_usr} / {self.facebook_pass}")
        print(f"Teléfono: {self.telefono}")
        print(f"Twitter: {self.twitter_usr} / {self.twitter_pass}")
        print(f"LinkedIn: {self.linkedin_usr} / {self.linkedin_pass}")
        
        
    def guardar_cambios(self, form_data: dict):
        """Actualiza los datos del usuario en Supabase."""

        # Actualiza el estado interno
        self.nombre = form_data.get("nombre", self.nombre)
        #self.email = form_data.get("email", self.email) el mail no porque sino podría cambiar contraseñas de otra gente
        self.telefono = form_data.get("telefono", self.telefono)
        self.instagram_usr = form_data.get("instagram_usr", self.instagram_usr)
        self.instagram_pass = form_data.get("instagram_pass", self.instagram_pass)
        self.facebook_usr = form_data.get("facebook_usr", self.facebook_usr)
        self.facebook_pass = form_data.get("facebook_pass", self.facebook_pass)
        self.twitter_usr = form_data.get("twitter_usr", self.twitter_usr)
        self.twitter_pass = form_data.get("twitter_pass", self.twitter_pass)
        self.linkedin_usr = form_data.get("linkedin_usr", self.linkedin_usr)
        self.linkedin_pass = form_data.get("linkedin_pass", self.linkedin_pass)

        # Actualiza en la base de datos (según email como identificador)
        supabase.table("users").update({
            "nombre": self.nombre,
            "pass": self.password,
            "telefono": self.telefono,
            "instagram_usr": self.instagram_usr,
            "instagram_pass": self.instagram_pass,
            "facebook_usr": self.facebook_usr,
            "facebook_pass": self.facebook_pass,
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
                nombre=contacto_data.get("nombre", ""),
                email=contacto_data.get("email", ""),
                telefono=contacto_data.get("telefono", ""),
                instagram=contacto_data.get("instagram", ""),
                facebook=contacto_data.get("facebook", ""),
                twitter=contacto_data.get("twitter", ""),
                linkedin=contacto_data.get("linkedin", "")
            )
            self.contactos.append(contacto)
            
        if self.contactos and self.selected_contact is None:
            self.selected_contact = self.contactos[0]
        
        print(f"{len(self.contactos)} contacto(s) cargado(s) correctamente.")
        print(self.contactos)
        
        
        
    
    #****************************************************************************************
    #******************* TODO ESTO ES PARA EL CREAR CONTACTOS *******************************
    #****************************************************************************************
        
        
    # Campos para añadir un nuevo contacto
    nuevo_nombre: str = ""
    nuevo_email: str = ""
    nuevo_telefono: str = ""
    nuevo_instagram: str = ""
    nuevo_facebook: str = ""
    nuevo_twitter: str = ""
    nuevo_linkedin: str = ""
    
    contactos: List[Contacto] = []

    def add_new_user(self):
        
        if not self.nuevo_nombre or not self.nuevo_telefono or not self.nuevo_email:
            # Aqui deberíamos poner para que salga este mensaje de error en la interfaz de añadir contacto
            #self.error = "Nombre, Teléfono y Email del contacto son obligatorios."
            print("Nombre, Teléfono y Email del contacto son obligatorios.")
            return
        
        nuevo = Contacto(
            nombre=self.nuevo_nombre,
            email=self.nuevo_email,
            telefono=self.nuevo_telefono,
            instagram=self.nuevo_instagram,
            facebook=self.nuevo_facebook,
            twitter=self.nuevo_twitter,
            linkedin=self.nuevo_linkedin,
        )
        self.contactos.append(nuevo)
        
        
        
        existing_contact = supabase.table("contactos")\
                .select("nombre")\
                .eq("user_email", self.email)\
                .eq("nombre", self.nuevo_nombre)\
                .execute()

        if existing_contact.data and len(existing_contact.data) > 0:
            self.error = "El contacto ya existe."
            print("El contacto ya existe.")
            return

        # Insertar nuevo contacto asociado al usuario actual
        supabase.table("contactos").insert({
            "nombre": self.nuevo_nombre,
            "email": self.nuevo_email,  # Email del contacto
            "telefono": self.nuevo_telefono,
            "instagram": self.nuevo_instagram,
            "facebook": self.nuevo_facebook,
            "twitter": self.nuevo_twitter,
            "linkedin": self.nuevo_linkedin,
            "user_email": self.email  # Email del usuario autenticado
        }).execute()
        
        # Resetea campos del formulario
        self.nuevo_nombre = ""
        self.nuevo_email = ""
        self.nuevo_telefono = ""
        self.nuevo_instagram = ""
        self.nuevo_facebook = ""
        self.nuevo_twitter = ""
        self.nuevo_linkedin = ""
        
        self.load_entries()
        
        
    def modificar_contacto(self, nombre_contacto:str):
        print("modificando...")
        
        supabase.table("contactos")\
                .update({
                    "nombre": self.nuevo_nombre,
                    "email": self.nuevo_email,
                    "telefono": self.nuevo_telefono,
                    "instagram": self.nuevo_instagram,
                    "facebook": self.nuevo_facebook,
                    "twitter": self.nuevo_twitter,
                    "linkedin": self.nuevo_linkedin,
                })\
                .eq("user_email", self.email)\
                .eq("nombre", nombre_contacto)\
                .execute()
                
        # Resetea campos del formulario
        self.nuevo_nombre = ""
        self.nuevo_email = ""
        self.nuevo_telefono = ""
        self.nuevo_instagram = ""
        self.nuevo_facebook = ""
        self.nuevo_twitter = ""
        self.nuevo_linkedin = ""
        
        #borra el anterior contacto de la lista y añade el nuevo
        self.contactos = [c for c in self.contactos if c.nombre != nombre_contacto]
        self.contactos.append(Contacto(
            nombre=self.nuevo_nombre,
            email=self.nuevo_email,
            telefono=self.nuevo_telefono,
            instagram=self.nuevo_instagram,
            facebook=self.nuevo_facebook,
            twitter=self.nuevo_twitter,
            linkedin=self.nuevo_linkedin,
        ))
        self.load_entries()
        print(f"Contacto '{nombre_contacto}' modificado correctamente.")

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
        self.nuevo_facebook = contacto.facebook or ""
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
        self.load_entries()
        print(f"Contacto '{nombre_contacto}' eliminado correctamente.")


    #****************************************************************************************
    #************************ TODO ESTO ES PARA LA TABLA DE CONTACTOS ***********************
    #****************************************************************************************
    
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page
    
    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Contacto]:
        items = self.contactos

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["nombre"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in ["nombre", "email", "telefono", "instagram", "facebook", "twitter", "linkedin"]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 1
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Contacto]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

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

    def load_entries(self):
        self.cargar_contactos()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()
        

    def export_to_csv(self):
        """Genera un CSV con los contactos y lo pone disponible para descargar."""
        file_path = Path("assets/contactos.csv")

        # Crear carpeta 'assets' si no existe
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Cabecera
            writer.writerow(["Nombre", "Email", "Teléfono", "Instagram", "Facebook", "Twitter", "LinkedIn"])
            # Filas de contactos
            for contacto in self.contactos:
                writer.writerow([
                    contacto.nombre,
                    contacto.email,
                    contacto.telefono,
                    contacto.instagram,
                    contacto.facebook,
                    contacto.twitter,
                    contacto.linkedin,
                ])

        return rx.download(url="/contactos.csv")


    #****************************************************************************************
    #************************ TODO ESTO ES PARA LA PAG DEL CHAT *****************************
    #****************************************************************************************

    selected_contact_chat: Optional[Contacto] = None

    selected_red_social: str = ""

    def seleccionar_contacto_chat(self, contacto: Contacto):
        self.selected_contact_chat = contacto
    
    def set_red_social(self, red_social: str):
        self.selected_red_social = red_social
        print(f"Red social cambiada:{self.selected_red_social}")