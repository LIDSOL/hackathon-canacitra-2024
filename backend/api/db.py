import sqlite3
import networkx as nx

def conexion_base_de_datos() -> sqlite3.Connection:
    # Conectar o crear la base de datos
    conn = sqlite3.connect('metro.db')

    # Activar SpatiaLite
    conn.enable_load_extension(True)
    conn.execute("SELECT load_extension('mod_spatialite')")

    # Crear tabla para las estaciones
    conn.execute('''
    CREATE TABLE IF NOT EXISTS estaciones (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        linea TEXT NOT NULL
    )
    ''')

    # Crear tabla para las líneas
    conn.execute('''
    CREATE TABLE IF NOT EXISTS lineas (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    )
    ''')

    # Crear tabla para las conexiones entre estaciones
    conn.execute('''
    CREATE TABLE IF NOT EXISTS conexiones (
        id INTEGER PRIMARY KEY,
        estacion_origen INTEGER NOT NULL,
        estacion_destino INTEGER NOT NULL,
        tiempo_estimado INTEGER NOT NULL,
        FOREIGN KEY (estacion_origen) REFERENCES estaciones(id),
        FOREIGN KEY (estacion_destino) REFERENCES estaciones(id)
    )
    ''')

    conn.commit()
    return conn

# Agregar una línea
def agregar_linea(conn, nombre) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lineas (nombre) VALUES (?)", (nombre,))
    conn.commit()

# Agregar una estación
def agregar_estacion(conn, nombre, linea) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estaciones (nombre, linea) VALUES (?, ?)",
                   (nombre, linea))
    conn.commit()

# Agregar una conexión entre estaciones con un tiempo estimado
def agregar_conexion(conn, origen, destino, tiempo_estimado) -> None:
    cursor = conn.cursor()

    # Verificar si la conexión ya existe
    cursor.execute("""
        SELECT id FROM conexiones
        WHERE estacion_origen = ? AND estacion_destino = ?
    """, (origen, destino))

    resultado = cursor.fetchone()

    if resultado:
        # Si la conexión existe, actualizar el tiempo estimado
        conexion_id = resultado[0]
        cursor.execute("""
            UPDATE conexiones
            SET tiempo_estimado = ?
            WHERE id = ?
        """, (tiempo_estimado, conexion_id))
    else:
        # Si la conexión no existe, insertar una nueva
        cursor.execute("""
            INSERT INTO conexiones (estacion_origen, estacion_destino, tiempo_estimado) 
            VALUES (?, ?, ?)
        """, (origen, destino, tiempo_estimado))

    conn.commit()

def imprimir_tiempo_estimado(conn, conexion_id) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT tiempo_estimado FROM conexiones WHERE id = ?", (conexion_id,))
    tiempo_estimado = cursor.fetchone()[0]
    print(f"Tiempo estimado: {tiempo_estimado} minutos")

# Crear el grafo de las estaciones y conexiones
def obtener_grafo(conn) -> nx.DiGraph:
    G = None
    G = nx.DiGraph()

    # Obtener las estaciones
    estaciones = conn.execute("SELECT id, nombre FROM estaciones").fetchall()

    # Añadir nodos (estaciones)
    for estacion in estaciones:
        G.add_node(estacion[0], nombre=estacion[1])

    # Obtener las conexiones (con su tiempo estimado)
    conexiones = conn.execute("SELECT estacion_origen, estacion_destino, tiempo_estimado FROM conexiones").fetchall()

    # Añadir aristas (conexiones)
    for conexion in conexiones:
        G.add_edge(conexion[0], conexion[1], weight=conexion[2])

    return G

# Encontrar la ruta más corta entre dos estaciones
def encontrar_rutas(conn, estacion_inicio, estacion_fin):
    G = obtener_grafo(conn)

    # Encontrar la ruta más corta en tiempo estimado
    try:
        rutas = nx.shortest_path(G, source=estacion_inicio, target=estacion_fin, weight='weight')
        tiempo_total = sum(G[u][v]['weight'] for u, v in zip(rutas[:-1], rutas[1:]))
        return rutas, tiempo_total
    except nx.NetworkXNoPath:
        return None, None

def verificar_conexiones(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conexiones")
    conexiones = cursor.fetchall()
    for conexion in conexiones:
        print(conexion)

# Ejemplo de uso
conn = conexion_base_de_datos()

# Crear Linea 1, 2 y 3 del metro
agregar_linea(conn, "Línea 1")
agregar_linea(conn, "Línea 2")
agregar_linea(conn, "Línea 3")

# Crear estaciones de la Línea 1
agregar_estacion(conn, "Estación A", "Línea 1")
agregar_estacion(conn, "Estación B", "Línea 1")
agregar_estacion(conn, "Estación C", "Línea 1")

# Crear conexiones entre estaciones
agregar_conexion(conn, 1, 2, 10)  # Estación A -> Estación B
agregar_conexion(conn, 2, 1, 10)  # Estación B -> Estación A
agregar_conexion(conn, 2, 3, 15)  # Estación B -> Estación C
agregar_conexion(conn, 3, 2, 15)  # Estación C -> Estación B

# Crear estaciones de la Línea 2
agregar_estacion(conn, "Estación D", "Línea 2")
agregar_estacion(conn, "Estación E", "Línea 2")
agregar_estacion(conn, "Estación F", "Línea 2")

# Crear conexiones entre estaciones
agregar_conexion(conn, 4, 5, 20)  # Estación D -> Estación E
agregar_conexion(conn, 5, 4, 20)  # Estación E -> Estación D
agregar_conexion(conn, 5, 6, 25)  # Estación E -> Estación F
agregar_conexion(conn, 6, 5, 25)  # Estación F -> Estación E

# Crear estaciones de la Línea 3
agregar_estacion(conn, "Estación G", "Línea 3")
agregar_estacion(conn, "Estación H", "Línea 3")
agregar_estacion(conn, "Estación I", "Línea 3")

# Crear conexiones entre estaciones
agregar_conexion(conn, 7, 8, 30)  # Estación G -> Estación H
agregar_conexion(conn, 8, 7, 30)  # Estación H -> Estación G
agregar_conexion(conn, 8, 9, 35)  # Estación H -> Estación I
agregar_conexion(conn, 9, 8, 35)  # Estación I -> Estación H

# Crear conexión entre estaciones de diferentes líneas
agregar_conexion(conn, 3, 4, 5)  # Estación C -> Estación D
agregar_conexion(conn, 4, 3, 5)  # Estación D -> Estación C
agregar_conexion(conn, 1, 9, 10)  # Estación I -> Estación A
agregar_conexion(conn, 9, 1, 10)  # Estación A -> Estación I
agregar_conexion(conn, 5, 8, 15)  # Estación E -> Estación H
agregar_conexion(conn, 8, 5, 15)  # Estación H -> Estación E

# Ejemplo de impresión de tiempo estimado
#imprimir_tiempo_estimado(conn, 6)

# Verificar conexiones después de la actualización
verificar_conexiones(conn)

# Ejemplo: encontrar la ruta entre estación E(5) y estación A(1)
rutas, tiempo_total = encontrar_rutas(conn, 5, 1)
if rutas:
    # Imprimir ruta, tiempo estimado
    print(f"Ruta: {rutas}, Tiempo estimado: {tiempo_total} minutos")
else:
    print("No hay rutas disponibles entre las estaciones seleccionadas.")

