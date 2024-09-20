import sqlite3
import os
from graph import crear_archivo_de_base_de_datos, imprimir_grafo, encontrar_rutas, obtener_estaciones_id, obtener_estaciones_info

def conexion_base_de_datos() -> sqlite3.Connection:
    # Si la base de datos no existe, llamar al método crear_base_de_datos
    if not os.path.exists('metro.db'):
        # Crear tablas con datos del metro
        crear_archivo_de_base_de_datos()

    # Conectar a la base de datos
    conn = sqlite3.connect('metro.db')
    conn.enable_load_extension(True)
    conn.execute("SELECT load_extension('mod_spatialite')")
    conn.commit()

    return conn

def actualizar_conexion(conn, origen, destino, tiempo_evento) -> None:
    cursor = conn.cursor()

    # Obtener id de la conexión
    cursor.execute("""
        SELECT id
        FROM conexiones
        WHERE estacion_origen = ? AND estacion_destino = ?
    """, (origen, destino))
    resultado = cursor.fetchone()

    # Si la conexión no existe, retornar
    if not resultado:
        return

    # Si la conexión existe, actualizar el tiempo estimado
    conexion_id = resultado[0]
    cursor.execute("""
        UPDATE conexiones
        SET tiempo_estimado_evento = ?
        WHERE id = ?
    """, (tiempo_evento, conexion_id))
    cursor.execute("""
        UPDATE conexiones
        SET tiempo_estimado = tiempo_estimado_normal + tiempo_estimado_evento
        WHERE id = ?
    """, (conexion_id,))

    conn.commit()

def imprimir_tiempo_estimado(conn, conexion_id) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT tiempo_estimado FROM conexiones WHERE id = ?", (conexion_id,))
    tiempo_estimado = cursor.fetchone()[0]
    print(f"Tiempo estimado: {tiempo_estimado} minutos")

def verificar_conexiones(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conexiones")
    conexiones = cursor.fetchall()
    for conexion in conexiones:
        print(conexion)

# Ejemplo de uso
conn = conexion_base_de_datos()
#imprimir_grafo(conn)

# Calcular ruta
estaciones_id = obtener_estaciones_id(conn)
estaciones_info = obtener_estaciones_info(conn)

ruta,tiempo = encontrar_rutas(conn, estaciones_id[("Garibaldi", "ML8")], estaciones_id[("Barranca del Muerto", "ML7")])

print(f"Tiempos: {tiempo}")
for estacion in ruta:
    print(estaciones_info[estacion], end=" -> ")
print()
