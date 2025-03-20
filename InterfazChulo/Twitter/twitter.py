import streamlit as st
import requests
from Twitter import config

def buscar_tweets():
    """Función que muestra la interfaz de búsqueda de tweets en Streamlit."""
    st.title("🔍 Buscador de Tweets")
    st.markdown("Introduce el nombre de usuario de X (antes Twitter) y consulta los tweets más recientes.")

    # Formulario de búsqueda
    with st.form(key="search_form"):
        username = st.text_input("Nombre de usuario (sin @):")
        max_results = st.slider("Número de tweets a buscar", min_value=5, max_value=50, value=10)
        search_button = st.form_submit_button("Buscar Tweets")

    # Lógica para ejecutar la búsqueda
    if search_button and username:
        try:
            with st.spinner("Buscando usuario..."):
                user_id = get_user_id(username)

            with st.spinner(f"Buscando los últimos {max_results} tweets..."):
                tweets = get_user_tweets(user_id, max_results)

            if not tweets:
                st.warning(f"No se encontraron tweets para @{username}.")
            else:
                st.success(f"Se encontraron {len(tweets)} tweets de @{username}:")
                for tweet in tweets:
                    tweet_text = tweet.get("text", "No disponible")
                    tweet_id = tweet.get("id", "N/A")
                    st.markdown(f"<div class='tweet-box'><strong>📝 Tweet {tweet_id}:</strong><br>{tweet_text}</div>", unsafe_allow_html=True)

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Error obteniendo datos: {e}")

# Funciones auxiliares
def get_user_id(username: str) -> str:
    """Obtiene el ID de usuario a partir del nombre de usuario de X."""
    url = f"https://api.x.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {config.bearer_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["id"]

def get_user_tweets(user_id: str, max_results: int = 10) -> list:
    """Obtiene los tweets de un usuario a partir de su ID."""
    url = f"https://api.x.com/2/users/{user_id}/tweets?max_results={max_results}"
    headers = {"Authorization": f"Bearer {config.bearer_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("data", [])
