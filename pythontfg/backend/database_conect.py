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
    error: str = ""  # mensaje de error
    
    
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

    
    def validar_email(self):
        if not self.email:
            self.error = "El correo no puede estar vacío."
            return

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.email):
            self.error = "El formato del correo no es válido."
            return
        self.error = ""  # limpia el error si está bien
        
    def validar_login(self):
        #comentar, solo para desarrollo
        self.set_email("2@g.com")
        self.set_password("123456")
        
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("borrame").select("*").eq("email", self.email).eq("pass", self.password).execute()

        if res.data:
            # Usuario encontrado, redirigimos
            self.error = ""
            return rx.redirect("/overview")
        else:
            # No coincide email/pass
            self.error = "Correo o contraseña incorrectos."
            
    def validar_registro(self):
        # Consultamos la tabla 'borrame' buscando coincidencia exacta de email y pass
        res = supabase.table("borrame").select("*").eq("email", self.email).execute()

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
        
        supabase.table("borrame").insert({"email": self.email, "pass": self.password}).execute()
        
        return rx.redirect("/overview")