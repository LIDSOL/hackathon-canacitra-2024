import streamlit as st
import sys
import os

# Agregar el directorio backend al sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend'))

# Ahora puedes intentar importar los módulos
from  db import *
from user import *
from ai import *

conn = conexion_base_de_datos()

# Obtener el id del usuario activo de un archivo activo.txt
def get_active_user_from_file() -> str:
    with open('active.txt', 'r') as file:
        return file.read()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

def create_route_page():
    with st.form("my_form", clear_on_submit=True):
        st.markdown("### ¿Cuál es la información de la ruta nueva? 🚂")

        origen = st.text_input("Origen:")
        destino = st.text_input("Destino:")

        hora_salida = st.time_input("Hora de salida:")
        hora_llegada = st.time_input("Hora de regreso:")

        st.write("¿Qué días de la semana realizas esta ruta?")
        entre = st.checkbox("Lunes a Viernes")
        fin = st.checkbox("Sábados y Domingos")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Mandar nueva ruta del usuario a la base
            estacion_origen = guess_near_station(conn, origen)
            estacion_destino = guess_near_station(conn, destino)

            # Convertir hora a formato timestamp sqlite
            hora_salida = hora_salida.strftime("%H:%M:%S")
            hora_llegada = hora_llegada.strftime("%H:%M:%S")

            if entre and fin:
                dias = 1
            elif entre:
                dias = 2
            elif fin:
                dias = 3

            agregar_ruta(conn, get_active_user_from_file(), hora_salida, dias, estacion_destino)
            agregar_ruta(conn, get_active_user_from_file(), hora_llegada, dias, estacion_origen)


def not_logged_in_page():
    st.markdown("### You are not logged in.")

if st.session_state['logged_in']:
    create_route_page()
else:
    if st.session_state['page'] == 'login':
        not_logged_in_page()

if st.sidebar.button("Log out", key="logout_button_action"):
    if 'logged_in' in st.session_state:
        st.session_state['logged_in'] = False
        st.sidebar.success("You have successfully logged out")
        st.switch_page("About_us.py")
    else:
        st.sidebar.error("There is no session active now")
        st.switch_page("About_us.py")