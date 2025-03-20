import streamlit as st

def inicio():
    # ===============================
    # Estilos personalizados con CSS
    # ===============================
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }

        .title {
            font-size: 4em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 2em;
            text-align: center;
            margin-bottom: 2rem;
        }
        .info {
            font-size: 1.3em;
            line-height: 1.8;
            margin: 1rem 0;
            text-align: justify;
        }
        .features {
            margin-top: 2rem;
        }
        .features ul {
            list-style: none;
            padding: 0;
        }
        .features li {
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            font-size: 1.2em;
        }
        .features li::before {
            content: "\\2714";
            color: #3ddc97;
            font-size: 1.5em;
            margin-right: 0.8rem;
        }
        .cta-button {
            background-color: #3ddc97;
            color: white;
            padding: 1rem 2rem;
            font-size: 1.2em;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .cta-button:hover {
            background-color: #35c488;
        }
        .footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.9em;
            color: #cccccc;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # ===============================
    # Contenido de la página de inicio
    # ===============================

    st.markdown('<div class="title">Social Trends Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Explora y analiza tendencias en redes sociales en tiempo real</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info">
            Bienvenido a la plataforma que transforma la forma en que descubres y analizas el pulso de las redes sociales. 
            Nuestro sistema te permite acceder a datos en tiempo real, descubrir tendencias emergentes y generar reportes visuales que facilitan la toma de decisiones.
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="features">
            <ul>
                <li>Identifica hashtags y temas virales en segundos.fuytrytrf</li>
                <li>Analiza el sentimiento y la interacción de tus publicaciones.</li>
                <li>Genera reportes detallados y visualizaciones interactivas.</li>
                <li>Accede a datos en tiempo real desde múltiples redes sociales.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown('<div style="text-align:center; margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown('<button class="cta-button" onclick="window.location.href=\'#\'">Descubre Más</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.image("https://via.placeholder.com/1200x500.png?text=Visualiza+Tendencias", use_container_width=True)

    st.markdown('<div class="footer">© 2025 Social Trends Analyzer. Todos los derechos reservados.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    inicio()
