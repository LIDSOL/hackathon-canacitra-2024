from user import *
from db import *

# Valores del demo
conn = conexion_base_de_datos()

# Crear usuario
add_user(conn, "fer", "ordfer@gmail.com", "password")
# Agregar ruta a la unam
agregar_ruta(conn, "ordfer@gmail.com", "6:32", "Lunes", "Universidad")
# Agregar ruta a polanco
agregar_ruta(conn, "ordfer@gmail.com", "7:00", "Martes", "Polanco")

# Agregar retraso en linea 3
actualizar_linea(conn, "ML3", 5)
# Agregar retraso en linea 7
actualizar_linea(conn, "ML7", 10)

grafo = obtener_grafo(conn)
estaciones_id = obtener_estaciones_id(conn)

ruta, tiempo = encontrar_rutas(estaciones_id["Coyuya", "ML8"], estaciones_id["Universidad", "ML3"], grafo)

s = stringificar_ruta(conn, ruta)
print(s)

