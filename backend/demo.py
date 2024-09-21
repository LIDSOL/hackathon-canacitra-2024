from user import *
from db import *

# Valores del demo
conn = conexion_base_de_datos()

# Crear usuario
add_user(conn, "fer", "ordfer@gmail.com", "password")
# Agregar ruta
agregar_ruta(conn, "ordfer@gmail.com", "6:32", "Lunes", "Coyuya")
