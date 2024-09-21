import streamlit as st
import os
import sys

# Debe mostrar:
# 1. Las lineas que se encuentran mal
# 2. Una entrada de texto para que el usuario pueda decir a donde se dirige
# 3. Una sugerencia de listas de lugares a donde se puede dirigir
# 4. Un mapa de la ubicación actual

# Agregar modulos de backend
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend'))
from db import *
from user import *
from ai import *

# Obtener el id del usuario activo de un archivo activo.txt
def get_active_user_from_file() -> str:
    with open('active.txt', 'r') as file:
        return file.read()

def set_estacion_destino(estacion_id) -> int:
    with open('estacion_destino.txt', 'w') as file:
        file.write(str(estacion_id))

conn = conexion_base_de_datos()
user_id = get_active_user_from_file()
user_name = get_user_name(conn, user_id)

## Set page configuration
st.set_page_config(
    page_title="Jellyway",
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

# Lineas que se encuentran mal, asumir que la linea 8 es la que se encuentra mal
st.markdown("# Jellyway")

# Mostrar dos columnas
col1, col2 = st.columns(2)

# Columna 1
with col1:
    st.markdown("## ¡Hola "+user_name+"! 🌟")

    lugar = st.text_input("#### ¡Buenos días!, dónde te diriges hoy? 🤔")

    # Mostrar los lugares en cuadros tipo botones
    st.markdown("#### Te sugerimos los siguientes lugares de tus lugares frecuentes:")

    estaciones_info = obtener_estaciones_info(conn)
    destinos = set(obtener_destinos_ruta_usuario(conn, user_id))

    for destino in destinos:
        if st.button(estaciones_info[destino[0]][0]):
            set_estacion_destino(destino[0])
            st.switch_page("pages/3_rute.py")

with col2:
    st.markdown("#### Te encuentras en:")

    # Mostrar el mapa de la ubicación actual
    mapa = '<iframe width="425" height="350" src="https://www.openstreetmap.org/export/embed.html?bbox=-99.1234803199768%2C19.392590361364118%2C-99.1088891029358%2C19.404086436656293&amp;layer=mapnik" style="border: 1px solid black"></iframe><br/><small><a href="https://www.openstreetmap.org/#map=16/19.39834/-99.11618">View Larger Map</a></small>'
    st.markdown(mapa, unsafe_allow_html=True)

if st.sidebar.button("Log out", key="logout_button_action"):
    if 'logged_in' in st.session_state:
        st.session_state['logged_in'] = False
        st.sidebar.success("You have successfully logged out")
        st.switch_page("About_us.py")
    else:
        st.sidebar.error("There is no session active now")
        st.switch_page("About_us.py")