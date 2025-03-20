import config
import requests
from rich import print
from rich.table import Table

def get_user_id(username: str) -> str:
    """
    Obtiene el ID de usuario a partir del nombre de usuario usando el endpoint:
    GET https://api.x.com/2/users/by/username/{username}
    """
    url = f"https://api.x.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {config.bearer_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza error si la respuesta no es 2xx
    data = response.json()
    return data["data"]["id"]

def get_user_tweets(user_id: str, max_results: int = 10) -> list:
    """
    Obtiene el timeline de tweets de un usuario a partir de su ID usando el endpoint:
    GET https://api.x.com/2/users/USER_ID/tweets
    """
    url = f"https://api.x.com/2/users/{user_id}/tweets?max_results={max_results}"
    headers = {
        "Authorization": f"Bearer {config.bearer_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Si no hay tweets, la clave "data" puede no existir
    return data.get("data", [])

def main():
    # Solicitamos al usuario el nombre de usuario y el número de tweets deseados
    username = input("Ingresa el nombre de usuario de Twitter: ")
    max_results_input = input("¿Cuántos tweets deseas obtener? (Por defecto 10): ")
    max_results = int(max_results_input) if max_results_input else 10
    
    # Obtener el ID del usuario a partir del username
    try:
        user_id = get_user_id(username)
    except requests.exceptions.HTTPError as e:
        print(f"[red]Error obteniendo el ID de usuario: {e}[/red]")
        return

    # Obtener los tweets del usuario
    try:
        tweets = get_user_tweets(user_id, max_results)
    except requests.exceptions.HTTPError as e:
        print(f"[red]Error obteniendo tweets: {e}[/red]")
        return
    
    if not tweets:
        print(f"[yellow]No se encontraron tweets para el usuario {username}.[/yellow]")
        return

    # Crear una tabla para mostrar los tweets
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID Tweet", style="dim", width=12)
    table.add_column("Tweet", width=60)

    for tweet in tweets:
        tweet_id = tweet.get("id", "N/A")
        text = tweet.get("text", "")
        table.add_row(tweet_id, text)

    print(table)

if __name__ == "__main__":
    main()
