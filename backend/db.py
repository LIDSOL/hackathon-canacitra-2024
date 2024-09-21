import sqlite3
import os
from graph import *

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

def actualizar_conexion(conn, conexion_id, tiempo_evento) -> None:
    cursor = conn.cursor()

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

def actualizar_linea(conn, linea, tiempo_evento) -> None:
    cursor = conn.cursor()

    # Obtener estaciones de la linea
    estaciones_dict = obtener_estaciones_de_linea(conn)

    conexiones = set()

    # Por cada estacion de la linea, agregar a las conexiones
    for estacion in estaciones_dict[linea]:
        tmp = obtener_conexiones_contienen_estacion(conn, estacion)
        for conexion in tmp:
            conexiones.add(conexion[0])

    # Por cada conexión, actualizar el tiempo estimado
    for conexion in conexiones:
        actualizar_conexion(conn, conexion, tiempo_evento)

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

def test(conn):
    # Actualizar tiempo de conexión de linea 1
    #actualizar_linea(conn, "ML1", 0)

    #print(obtener_estaciones_de_linea(conn))
    #print(obtener_conexiones_contienen_estacion(conn, 1))

    # Calcular ruta
    estaciones_id = obtener_estaciones_id(conn)
    estaciones_info = obtener_estaciones_info(conn)

    ruta,tiempo = encontrar_rutas(conn, estaciones_id[("Garibaldi", "ML8")], estaciones_id[("Barranca del Muerto", "ML7")])

    print(f"Tiempos: {tiempo}")
    for estacion in ruta:
        print(estaciones_info[estacion], end=" -> ")
    print()

    actualizar_linea(conn, "ML2", 20)

    ruta,tiempo = encontrar_rutas(conn, estaciones_id[("Garibaldi", "ML8")], estaciones_id[("Barranca del Muerto", "ML7")])

    actualizar_linea(conn, "ML1", 0)

    print(f"Tiempos: {tiempo}")
    for estacion in ruta:
        print(estaciones_info[estacion], end=" -> ")
    print()


#funcion para añadir un usuraio nuevo a la base de datos
#input email, nombre, contraseña
#output
def guardar_usuario(conn, email, nombre, contraseña):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios(email, nombre, contraseña) VALUES (?,?,?)", (email, nombre, contraseña))
    conn.commit()
#input email, destino, horario, dias
#output 
#funcion para almacenar en la tabla rutas una ruta comun de un usuario recibe -> id del usuairo, destino, horario de salida,dias de la semana
def guardar_ruta(conn, id_usuario, destino, horario, dias):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rutas(id_usuario, destino, horario, dias) VALUES (?,?,?,?)", (id_usuario, destino, horario, dias))
    conn.commit()

#funcion para que un usuario pueda reportar un evento en la tabla reporte_usuario(id del usuario,la linea en la que ocurrio, el tiempo de demora)
def reportar_evento(conn, id_usuario, linea, tiempo):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reporte_usuario(id_usuario, linea, tiempo) VALUES (?,?,?)", (id_usuario, linea, tiempo))
    conn.commit()

# Ejemplo de uso
#conn = conexion_base_de_datos()
#imprimir_grafo(conn)