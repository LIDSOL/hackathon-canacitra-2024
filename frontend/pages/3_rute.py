import streamlit as st
import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend'))
from graph import *
from db import *
from ai import *

def get_estacion_destino() -> int:
    with open('estacion_destino.txt', 'r') as file:
        return int(file.read())

# Debe mostrar:
# 1. Mapa de donde se encuentra el usuario
# 2. Porcentaje de viaje
# 3. Tiempo estimado de llegada
# 6. Ruta completa resaltando la siguiente estación y la estación actual

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

conn = conexion_base_de_datos()
cursor = conn.cursor()
estaciones_info = obtener_estaciones_info(conn)
estacion_inicial_id = guess_near_station(conn, 'Estoy en una de las estaciones mas transitadas')
estacion_inicial_info = estaciones_info[estacion_inicial_id]

grafo_ideal = obtener_grafo_ideal(conn)
grafo_real = obtener_grafo(conn)
ruta_ideal = encontrar_rutas(estacion_inicial_id,get_estacion_destino(), grafo_ideal)
ruta_alterna = encontrar_rutas(estacion_inicial_id, get_estacion_destino(), grafo_real)

print(ruta_ideal, ruta_alterna)

if ruta_ideal[1] == ruta_alterna[1]:
    print("No hay contratiempos")
else:
    print("Hay contratiempos en la ruta usual") 


ubic_estacion_actual = random.randint(0, len(ruta_alterna[0]) - 1)
estacion_actual = estaciones_info[ruta_alterna[0][ubic_estacion_actual]]
estacion_siguiente = estaciones_info[ruta_alterna[0][ubic_estacion_actual+1]]
estacion_final = estaciones_info[ruta_alterna[0][-1]]

print(estacion_siguiente, estacion_final)

# Lineas que se encuentran mal, asumir que la linea 8 es la que se encuentra mal
st.markdown("# Jellyway")

# Mostrar dos columnas
col1, col2 = st.columns(2)

# Columna 2, tiempo estimado de llegada y ruta completa
ruta = [('**Estacion inicial:** ' +estacion_inicial_info[0], estacion_inicial_info[1]),('**Estacion actual:** '+estacion_actual[0], estacion_actual[1]), ('**Estacion siguiente:** '+estacion_siguiente[0], estacion_siguiente[1]), ('**Estacion final:** '+estacion_final[0], estacion_final[1])]
with col1:
    # Mostrar cada estación conectada a la ruta en orden como botones
    st.markdown("#### Ruta completa:")
    for estacion in ruta:
        st.button(f'{estacion[0]} ({estacion[1]})')



# Columna 1,  mapa de donde se encuentra el usuario y porcentaje de viaje
with col2:
    st.markdown("#### Vas en la estacion "+estacion_actual[0]+" de la "+estacion_actual[1]+" 🚇")
    # Mostrar el porcentaje de viaje
    st.markdown("Porcentaje de viaje:")

    progreso = int(100*(ubic_estacion_actual / len(ruta_alterna[0])))
    st.progress(progreso)
    map = '<iframe width="425" height="350" src="https://www.openstreetmap.org/export/embed.html?bbox=-99.17232871055603%2C19.359954577831356%2C-99.16868090629579%2C19.36282924864357&amp;layer=mapnik" style="border: 1px solid black"></iframe><br/><small><a href="https://www.openstreetmap.org/#map=18/19.361392/-99.170505">View Larger Map</a></small>'
    st.markdown(map, unsafe_allow_html=True)

if st.sidebar.button("Log out", key="logout_button_action"):
    if 'logged_in' in st.session_state:
        st.session_state['logged_in'] = False
        st.sidebar.success("You have successfully logged out")
        st.switch_page("About_us.py")
    else:
        st.sidebar.error("There is no session active now")
        st.switch_page("About_us.py")