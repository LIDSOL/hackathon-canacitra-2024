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
