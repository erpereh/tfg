import streamlit as st
from ChatBot import chatbot
from Twitter import twitter
import inicio

# ⚠️ set_page_config SOLO AQUÍ (debe ser la primera línea después de imports)
st.set_page_config(page_title="Menú con Programas", layout="wide")

# Crear menú en la barra lateral
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una opción", ["Inicio", "Dashboard", "Explorar Tendencias", "Buscar Influencer", "Chatbot", "Histórico y Reportes", "Configuración"])

if opcion == "Inicio":
    inicio.inicio()
elif opcion == "Chatbot":
    chatbot.chatbot()
elif opcion == "Buscar Influencer":
    twitter.buscar_tweets()
