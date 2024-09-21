# Source streamlint
import streamlit as st

# Debemos de preguntar:
# 1. Nombre
# 2. Es estudiante o trabajador?
# 3. Si lo es, ¿en qué escuela o empresa trabaja?
# 4. A que hora suele salir de su casa?
# 5. A que hora suele regresar a su casa?
# 6. De donde suele salir?
# Cada pregunta debe de ser respondida con un campo de texto.
# Se responde a las preguntas con un botón de "Siguiente" y cambia a la siguiente pregunta.
# Al finalizar se muestra un mensaje de "Gracias por registrarte"

## Set page configuration
st.set_page_config(
    page_title="Hola, nuevo usuario",
    page_icon="assets/mi_icono.jpg",
    # layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/LIDSOL/hackathon-canacitra-2024',
        'Report a bug': "https://github.com/LIDSOL/hackathon-canacitra-2024",
        'About': "Encuentra la mejor ruta para llegar a tu destino de manera segura y rápida."
    }
)

## Custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik+Spray+Paint&display=swap');

    h1 {
        text-align: center;
        color: #a822c9;
        font-family: "Rubik Spray Paint", system-ui;
        font-size: 60px;
        font-weight: 400;
        font-style: normal;
    }

    h2 {
        text-align: left;
        font_size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

pagina_actual = "pregunta_1"

def header_registro():
    st.markdown("# JELLYWAY")

def pregunta_1_page():
    header_registro()
    st.markdown("## ¡Hola usuario_nuevo@! 🌟")

    st.markdown("### ¿Cuál es tu nombre? 🤔")
    nombre = st.text_input("Nombre")

    if st.button("Siguiente"):
        st.session_state['page'] = 'pregunta_2'


def pregunta_2_page():
    header_registro()
    st.markdown("### Oye fer, estudias o trabajas? 🎓💼")
    estudiante = st.radio("Selecciona una opción", ("Estudiante 🎓", "Trabajador 💼", "Otros 🌟"))

    if st.button("Siguiente"):
        st.session_state['page'] = 'pregunta_3'

def pregunta_3_page():
    header_registro()

    st.markdown("### ¿En donde estudias? 🏫")
    lugar = st.text_input("Escuela")

    if st.button("Siguiente"):
        st.session_state['page'] = 'pregunta_4'

def pregunta_4_page():
    header_registro()

    st.markdown("### Y para ir a la UNAM, ¿a qué hora sueles salir de tu casa? ⏰")
    hora = st.time_input("Hora de salida")

    if st.button("Siguiente"):
        st.session_state['page'] = 'pregunta_5'

def pregunta_5_page():
    header_registro()

    st.markdown("### ¿Y a qué hora sueles regresar a tu casa? ⏰")
    hora = st.time_input("Hora")

    if st.button("Siguiente"):
        st.session_state['page'] = 'pregunta_6'

def pregunta_6_page():
    header_registro()

    st.markdown("### Para terminar, ¿de dónde sueles salir? 🏠")
    lugar = st.text_input("Lugar")

    if st.button("Siguiente"):
        st.session_state['page'] = 'gracias'

def gracias_page():
    header_registro()

    st.markdown("### ¡Excelente, fer! 🎉"
                "Gracias por registrarte. 🌟\n"
                "Te mantendremos informada de las mejores rutas para llegar a tu destino de manera segura y rápida.\n")
    st.balloons()

# Main logic to control page display, switch between pages
if 'page' not in st.session_state:
    st.session_state['page'] = 'pregunta_1'

if st.session_state['page'] == 'pregunta_1':
    pregunta_1_page()
elif st.session_state['page'] == 'pregunta_2':
    pregunta_2_page()
elif st.session_state['page'] == 'pregunta_3':
    pregunta_3_page()
elif st.session_state['page'] == 'pregunta_4':
    pregunta_4_page()
elif st.session_state['page'] == 'pregunta_5':
    pregunta_5_page()
elif st.session_state['page'] == 'pregunta_6':
    pregunta_6_page()
elif st.session_state['page'] == 'gracias':
    gracias_page()