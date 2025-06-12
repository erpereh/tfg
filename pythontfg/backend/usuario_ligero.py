#clase para utilizar las credenciales del usuario
from dataclasses import dataclass
@dataclass
class UsuarioLigero:
    nombre: str
    instagram_usr: str
    instagram_pass: str
    discord_usr: str
    discord_pass: str
    twitter_usr: str
    twitter_pass: str
    linkedin_usr: str
    linkedin_pass: str
    email: str