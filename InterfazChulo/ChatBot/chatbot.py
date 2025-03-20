import streamlit as st
from openai import OpenAI
from ChatBot import config

def chatbot():
    st.markdown(
        """
        <style>
        .stButton>button {
            background: #ff4b4b;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: #ff2020;
            transform: scale(1.05);
        }
        .chat-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializar cliente de OpenAI
    client = OpenAI(
        base_url=config.base_url,
        api_key=config.api_key
    )

    # Inicializar el historial de mensajes en session_state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "system", "content": "Eres un asistente muy útil."}]

    st.title("🤖💅 Chatbot Guapisimo Precioso Perfecto")
    st.markdown("Escribe `new` para iniciar una nueva conversación.")

    # Mostrar el historial de la conversación
    for message in st.session_state['messages']:
        if message['role'] == "user":
            st.markdown(f"<div class='chat-box'><strong>Tú:</strong> {message['content']}</div>", unsafe_allow_html=True)
        elif message['role'] == "assistant":
            st.markdown(f"<div class='chat-box'><strong>Asistente:</strong> {message['content']}</div>", unsafe_allow_html=True)

    # Formulario para enviar nuevos mensajes
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("¿Sobre qué quieres hablar?")
        submit_button = st.form_submit_button("Enviar")

    if submit_button and user_input:
        if user_input.lower() == "new":
            st.session_state['messages'] = [{"role": "system", "content": "Eres un asistente muy útil."}]
            st.success("🆕 Nueva conversación creada")
            st.rerun()
        elif user_input.lower() == "pene":
            st.session_state['messages'].append({"role": "user", "content": user_input})
            respuesta_content = "El pene de David no tiene sentido lo grande que es, no lo dice él, lo dice la IA."
            st.session_state['messages'].append({"role": "assistant", "content": respuesta_content})
            st.rerun()
        else:
            # Añadir mensaje del usuario
            st.session_state['messages'].append({"role": "user", "content": user_input})
            with st.spinner("Obteniendo respuesta..."):
                respuesta = client.chat.completions.create(
                    model="deepseek/deepseek-r1:free",
                    messages=st.session_state['messages']
                )
                respuesta_content = respuesta.choices[0].message.content
            # Añadir respuesta del asistente
            st.session_state['messages'].append({"role": "assistant", "content": respuesta_content})
            st.rerun()
