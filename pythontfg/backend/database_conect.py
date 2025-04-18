from supabase import create_client, Client

SUPABASE_URL = "https://kpwbkzdjqgginzpfcpsd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtwd2JremRqcWdnaW56cGZjcHNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2NTYxMzUsImV4cCI6MjA2MDIzMjEzNX0.pBbx1E1vxNa1FunK0rXau--7SoA9934S7ISWixm-i2M"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Insertar un usuario
#supabase.table("borrame").insert({"email": "prueba4@correo.com", "pass": "123456"}).execute()

# Leer usuarios
#res = supabase.table("borrame").select("*").execute()
#print(res.data)


import reflex as rx
import re
class Usuario(rx.State):
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
    
    def on_instagram_usr_change(self, value: str):
        self.instagram_usr = value

    def on_instagram_pass_change(self, value: str):
        self.instagram_pass = value

    def on_facebook_usr_change(self, value: str):
        self.facebook_usr = value

    def on_facebook_pass_change(self, value: str):
        self.facebook_pass = value

    def on_telefono_change(self, value: str):
        self.telefono = value
        self.validar_telefono()

    def on_twitter_usr_change(self, value: str):
        self.twitter_usr = value

    def on_twitter_pass_change(self, value: str):
        self.twitter_pass = value

    def on_linkedin_usr_change(self, value: str):
        self.linkedin_usr = value

    def on_linkedin_pass_change(self, value: str):
        self.linkedin_pass = value

    
    
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
        
        
        #****************************************************************************************
        #comentar, solo para desarrollo
        self.set_email("1@gmail.com")
        self.set_password("1")
        #****************************************************************************************
        
        
        
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("users").select("*").eq("email", self.email).eq("pass", self.password).execute()

        if res.data:
            # Usuario encontrado, redirigimos
            self.error = ""
            self.cargar_datos_usr(res)
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
        #self.email = form_data.get("email", self.email)
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
            "telefono": self.telefono,
            "instagram_usr": self.instagram_usr,
            "instagram_pass": "otra vez",
            "facebook_usr": self.facebook_usr,
            "facebook_pass": self.facebook_pass,
            "twitter_usr": self.twitter_usr,
            "twitter_pass": self.twitter_pass,
            "linkedin_usr": self.linkedin_usr,
            "linkedin_pass": self.linkedin_pass,
        }).eq("email", self.email).execute()

        return rx.toast.success("Cambios guardados correctamente", position="top-center")

