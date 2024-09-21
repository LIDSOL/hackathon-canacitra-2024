import streamlit as st
import sys
import os

# Agregar el directorio backend al sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend'))

# Ahora puedes intentar importar los módulos
from  db import *  # o from backend.db import *
from user import *  # o from backend.user import *

conn = conexion_base_de_datos()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'


def create_route_page():
    st.markdown("## Create Route")
    st.write("Please enter your route information.")
    
    if 'email' not in st.session_state:
        st.session_state.email = ""
    if 'hora' not in st.session_state:
        st.session_state.hora = ""
    if 'dia_semana' not in st.session_state:
        st.session_state.dia_semana = ""
    if 'nombre_estacion' not in st.session_state:
        st.session_state.nombre_estacion = ""
    
    st.session_state.email = st.text_input("Email", st.session_state.email)
    st.session_state.hora = st.text_input("Hora", st.session_state.hora)
    st.session_state.dia_semana = st.text_input("Dia de la semana", st.session_state.dia_semana)
    st.session_state.nombre_estacion = st.text_input("Nombre de la estacion destino", st.session_state.nombre_estacion)
    
    # Create route button
    if st.button("Add Route"):
        if st.session_state.email and st.session_state.hora and st.session_state.dia_semana and st.session_state.nombre_estacion:
            agregar_ruta(conn, st.session_state.email, st.session_state.hora, st.session_state.dia_semana, st.session_state.nombre_estacion)
            st.success(f"Route created for {st.session_state.email}.")
            # Reset fields if needed
            st.session_state.email = ""
            st.session_state.hora = ""
            st.session_state.dia_semana = ""
            st.session_state.nombre_estacion = ""
        else:
            st.error("Please enter valid information.")
    
    # Button to go back to the main page
    if st.button("Back to Route"):
        st.session_state['page'] = 'route_page'     
        
def not_logged_in_page():
    st.markdown("### You are not logged in.")
    
if st.session_state['logged_in']:
    create_route_page()
else:
    if st.session_state['page'] == 'login':
        not_logged_in_page()