# Source streamlint
import streamlit as st
import os
import sys

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

## Set page configuration
st.set_page_config(
    page_title="¡Hola!",
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


# ---- Page functions ----

# Agregar modulos de backend
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend'))
from db import *
from user import *

# Inicializamos la conexión a la base de datos
conn = conexion_base_de_datos()

# Comprobar credenciales de un usuario
def login(username, password):
    return check_login(conn, username, password)

# Guardar usuario activo en archivo activo.txt
def save_active_user_to_file(conn, email):
    id = get_user_id(conn, email)

    with open('active.txt', 'w') as file:
        file.write(str(id))

# Obtener el id del usuario activo de un archivo activo.txt
def get_active_user_from_file() -> int:
    with open('active.txt', 'r') as file:
        if not file.read():
            return -1
        return int(file.read())

# ---- Page functions ----

pagina_actual = "pregunta_1"

def login_page():
    st.markdown("## Iniciar Sesión o Registrarse")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Button to handle login
    if st.button("Login"):
        if login(email, password):
            st.success("Entrando ... , bienvenido, " + email + "!")
            # Marcar como loggeado
            st.session_state['logged_in'] = True
            save_active_user_to_file(conn, email)

            # Redirigir a la página dashboard
            st.switch_page("pages/2_dashboard.py")
        else:
            st.error("El usuario no existe, creando ...")
            # Crear registro en la base de datos
            add_user(conn, "", email, password)

            st.session_state['logged_in'] = True
            save_active_user_to_file(conn, email)
            st.session_state['page'] = 'pregunta_1'

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
    st.session_state['page'] = 'login'

if st.session_state['page'] == 'login':
    login_page()
elif st.session_state['page'] == 'pregunta_1':
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