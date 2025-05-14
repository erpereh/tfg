#clase para utilizar las credenciales del usuario
from dataclasses import dataclass
@dataclass
class UsuarioLigero:
    instagram_usr: str
    instagram_pass: str
    facebook_usr: str
    facebook_pass: str
    twitter_usr: str
    twitter_pass: str
    linkedin_usr: str
    linkedin_pass: str
    email: str