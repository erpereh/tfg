import config
from rich import print
from instagrapi import Client

def main():
    cl = Client()
    cl.login("mispruebas_tfg", "David2004")

    # Utilizamos el endpoint privado para obtener la información del usuario
    user = cl.user_info_by_username("ibaillanos")
    user_id = user.pk
    medias = cl.user_medias(user_id, 20)
    print(medias)

if __name__ == "__main__":
    main()
