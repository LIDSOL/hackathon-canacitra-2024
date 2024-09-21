import sqlite3
import networkx as nx
from collections import defaultdict

# Agregar una linea
def agregar_linea(conn, nombre) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lineas (nombre) VALUES (?)", (nombre,))
    conn.commit()

# Agregar una estacion
def agregar_estacion(conn, nombre, linea) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estaciones (nombre, linea) VALUES (?, ?)",
                   (nombre, linea))
    conn.commit()

def obtener_estaciones_de_linea(conn) -> defaultdict:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, linea FROM estaciones
    """)

    estaciones_dict = defaultdict(list)

    estaciones = cursor.fetchall()
    for estacion in estaciones:
        estaciones_dict[estacion[1]].append(estacion[0])

    return estaciones_dict

# Agregar una conexion entre estaciones con un tiempo estimado
def agregar_conexion(conn, origen, destino, tiempo_estimado=4) -> None:
    cursor = conn.cursor()

    # Insertar una nueva conexion
    cursor.execute("""
        INSERT INTO conexiones (estacion_origen, estacion_destino, tiempo_estimado, tiempo_estimado_evento, tiempo_estimado_normal)
        VALUES (?, ?, ?, ?, ?)
    """, (origen, destino, tiempo_estimado, 0, tiempo_estimado))

    conn.commit()

def obtener_estaciones_id(conn) -> defaultdict:
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, linea FROM estaciones")
    estaciones = cursor.fetchall()
    estaciones_id = defaultdict(str)
    for estacion in estaciones:
        estaciones_id[(estacion[1], estacion[2])] = estacion[0]
    return estaciones_id

def obtener_estaciones_info(conn) -> defaultdict:
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, linea FROM estaciones")
    estaciones = cursor.fetchall()
    estaciones_info = defaultdict(str)
    for estacion in estaciones:
        estaciones_info[estacion[0]] = (estacion[1], estacion[2])
    return estaciones_info

def obtener_conexiones_contienen_estacion(conn, estacion_id) -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM conexiones WHERE estacion_origen = ? OR estacion_destino = ?", (estacion_id, estacion_id))
    conexiones = cursor.fetchall()
    return conexiones

def obtener_conexion_id(conn, origen, linea_origen, destino, linea_destino) -> int:
    cursor = conn.cursor()
    estaciones = obtener_estaciones_id(conn)

    origen_id = estaciones[(origen, linea_origen)]
    destino_id = estaciones[(destino, linea_destino)]

    cursor.execute("SELECT id FROM conexiones WHERE estacion_origen = ? AND estacion_destino = ?", (origen_id, destino_id))

    try:
        res = cursor.fetchone()[0]
        return res
    except TypeError:
        return None

def obtener_conexion_info(conn) -> defaultdict:
    cursor = conn.cursor()
    cursor.execute("SELECT id, estacion_origen, estacion_destino, tiempo_estimado FROM conexiones")
    conexiones = cursor.fetchall()
    conexiones_info = defaultdict(str)
    for conexion in conexiones:
        conexiones_info[conexion[0]] = (conexion[1], conexion[2], conexion[3])
    return conexiones_info

# Crear el grafo de las estaciones y conexiones
def obtener_grafo(conn) -> nx.DiGraph:
    G = None
    G = nx.DiGraph()

    # Obtener las estaciones
    estaciones = conn.execute("SELECT id, nombre FROM estaciones").fetchall()

    # Anadir nodos (estaciones)
    for estacion in estaciones:
        G.add_node(estacion[0], nombre=estacion[1])

    # Obtener las conexiones (con su tiempo estimado)
    conexiones = conn.execute("SELECT estacion_origen, estacion_destino, tiempo_estimado FROM conexiones").fetchall()

    # Anadir aristas (conexiones)
    for conexion in conexiones:
        G.add_edge(conexion[0], conexion[1], weight=conexion[2])

    return G

# Crear el grafo ideal de las estaciones y conexiones
def obtener_grafo_ideal(conn) -> nx.DiGraph:
    G = None
    G = nx.DiGraph()

    # Obtener las estaciones
    estaciones = conn.execute("SELECT id, nombre FROM estaciones").fetchall()

    # Anadir nodos (estaciones)
    for estacion in estaciones:
        G.add_node(estacion[0], nombre=estacion[1])

    # Obtener las conexiones (con su tiempo estimado)
    conexiones = conn.execute("SELECT estacion_origen, estacion_destino, tiempo_estimado FROM conexiones").fetchall()

    # Anadir aristas (conexiones)
    for conexion in conexiones:
        G.add_edge(conexion[0], conexion[1], weight=4)

    return G

# Encontrar la ruta más corta entre dos estaciones
def encontrar_rutas(estacion_inicio, estacion_fin, grafo):
    # Encontrar la ruta más corta en tiempo estimado
    try:
        rutas = nx.shortest_path(grafo, source=estacion_inicio, target=estacion_fin, weight='weight')
        tiempo_total = sum(grafo[u][v]['weight'] for u, v in zip(rutas[:-1], rutas[1:]))
        return rutas, tiempo_total
    except nx.NetworkXNoPath:
        return None, None

def stringificar_ruta(conn, ruta):
    s = []

    estaciones_info = obtener_estaciones_info(conn)

    for estacion in ruta:
        s.append((estaciones_info[estacion][0], estaciones_info[estacion][1]))

    return s

def imprimir_grafo(conn, grafo):
    estaciones_info = obtener_estaciones_info(conn)
    conexiones_info = obtener_conexion_info(conn)

    print("Estaciones:")
    for node in grafo.nodes:
        print(f"{node}: {estaciones_info[node]}")

    print("\nConexiones:")
    for edge in grafo.edges:
        origen = estaciones_info[edge[0]]
        destino = estaciones_info[edge[1]]

        linea_origen = origen[1]
        linea_destino = destino[1]
        con_info = conexiones_info[obtener_conexion_id(conn, origen[0], linea_origen, destino[0], linea_destino)]

        print(f"{edge}: {estaciones_info[con_info[0]]} -> {estaciones_info[con_info[1]]} ({con_info[2]} minutos)")


def crear_archivo_de_base_de_datos() -> None:
    # Conectar o crear la base de datos
    conn = sqlite3.connect('metro.db')

    # Activar SpatiaLite
    conn.enable_load_extension(True)
    conn.execute("SELECT load_extension('mod_spatialite')")

    # Ejecutar el script de init.sql para crear las tablas
    with open('init.sql') as f:
        conn.executescript(f.read())

    # Commit para guardar los cambios
    conn.commit()

    # Generar lineas
    agregar_linea(conn, "ML1")
    agregar_linea(conn, "ML2")
    agregar_linea(conn, "ML3")
    agregar_linea(conn, "ML4")
    agregar_linea(conn, "ML5")
    agregar_linea(conn, "ML6")
    agregar_linea(conn, "ML7")
    agregar_linea(conn, "ML8")
    agregar_linea(conn, "ML9")
    agregar_linea(conn, "MLA")
    agregar_linea(conn, "MLB")
    agregar_linea(conn, "ML12")

    # Estaciones de la Linea 1
    agregar_estacion(conn, "Observatorio", "ML1")
    agregar_estacion(conn, "Tacubaya", "ML1")
    agregar_estacion(conn, "Juanacatlan","ML1")
    agregar_estacion(conn, "Chapultepec","ML1")
    agregar_estacion(conn, "Sevilla","ML1")
    agregar_estacion(conn, "Insurgentes","ML1")
    agregar_estacion(conn, "Cuahtemoc","ML1")
    agregar_estacion(conn, "Balderas","ML1")
    agregar_estacion(conn, "Salto del Agua","ML1")
    agregar_estacion(conn, "Isabel la Catolica","ML1")
    agregar_estacion(conn, "Pino Suarez","ML1")
    agregar_estacion(conn, "Merced","ML1")
    agregar_estacion(conn, "Candelaria","ML1")
    agregar_estacion(conn, "San Lazaro","ML1")
    agregar_estacion(conn, "Moctezuma","ML1")
    agregar_estacion(conn, "Balbuena","ML1")
    agregar_estacion(conn, "Boulevard Puerto Aereo","ML1")
    agregar_estacion(conn, "Gomez Farias","ML1")
    agregar_estacion(conn, "Zaragosa","ML1")
    agregar_estacion(conn, "Pantitlan","ML1")

    # Estaciones de la linea 2
    agregar_estacion(conn, "Cuatro caminos","ML2")
    agregar_estacion(conn, "Panteones","ML2")
    agregar_estacion(conn, "Tacuba","ML2")
    agregar_estacion(conn, "Cuitlahuac","ML2")
    agregar_estacion(conn, "Popotla","ML2")
    agregar_estacion(conn, "Colegio Militar","ML2")
    agregar_estacion(conn, "Normal","ML2")
    agregar_estacion(conn, "San Cosme","ML2")
    agregar_estacion(conn, "Revolucion","ML2")
    agregar_estacion(conn, "Hidalgo","ML2")
    agregar_estacion(conn, "Bellas Artes","ML2")
    agregar_estacion(conn, "Allende","ML2")
    agregar_estacion(conn, "Zocalo","ML2")
    agregar_estacion(conn, "Pino Suarez","ML2")
    agregar_estacion(conn, "San Antonio Abad","ML2")
    agregar_estacion(conn, "Chabacano","ML2")
    agregar_estacion(conn, "Viaducto","ML2")
    agregar_estacion(conn, "Xola","ML2")
    agregar_estacion(conn, "Villa de Cortes","ML2")
    agregar_estacion(conn, "Nativitas","ML2")
    agregar_estacion(conn, "Portales","ML2")
    agregar_estacion(conn, "Ermita","ML2")
    agregar_estacion(conn, "General Anaya","ML2")
    agregar_estacion(conn, "Tasquena","ML2")

    #Estaciones de la linea 3
    agregar_estacion(conn, "Indios Verdes","ML3")
    agregar_estacion(conn, "Deportivo 18 de marzo","ML3")
    agregar_estacion(conn, "Potrero","ML3")
    agregar_estacion(conn, "La Raza","ML3")
    agregar_estacion(conn, "Tlatelolco","ML3")
    agregar_estacion(conn, "Guerrero","ML3")
    agregar_estacion(conn, "Hidalgo","ML3")
    agregar_estacion(conn, "Juarez","ML3")
    agregar_estacion(conn, "Balderas","ML3")
    agregar_estacion(conn, "Ninos Heroes","ML3")
    agregar_estacion(conn, "Hospital General","ML3")
    agregar_estacion(conn, "Centro Medico","ML3")
    agregar_estacion(conn, "Etiopia","ML3")
    agregar_estacion(conn, "Eugenia","ML3")
    agregar_estacion(conn, "Division del Norte","ML3")
    agregar_estacion(conn, "Zapata","ML3")
    agregar_estacion(conn, "Coyoacan","ML3")
    agregar_estacion(conn, "Viveros","ML3")
    agregar_estacion(conn, "Miguel Angel de Quevedo","ML3")
    agregar_estacion(conn, "Copilco","ML3")
    agregar_estacion(conn, "Universidad","ML3")

    # Estaciones de la linea 4
    agregar_estacion(conn, "Martin Carrera","ML4")
    agregar_estacion(conn, "Talisman","ML4")
    agregar_estacion(conn, "Bondojito","ML4")
    agregar_estacion(conn, "Consulado","ML4")
    agregar_estacion(conn, "Canal del Norte","ML4")
    agregar_estacion(conn, "Morelos","ML4")
    agregar_estacion(conn, "Candelaria","ML4")
    agregar_estacion(conn, "Fray Servando","ML4")
    agregar_estacion(conn, "Jamaica","ML4")
    agregar_estacion(conn, "Santa Anita","ML4")

    # Estaciones de la linea 5
    agregar_estacion(conn, "Pantitlan","ML5")
    agregar_estacion(conn, "Hangares","ML5")
    agregar_estacion(conn, "Terminal Aerea","ML5")
    agregar_estacion(conn, "Oceania","ML5")
    agregar_estacion(conn, "Aragon","ML5")
    agregar_estacion(conn, "Eduardo Molina","ML5")
    agregar_estacion(conn, "Consulado","ML5")
    agregar_estacion(conn, "Valle Gomez","ML5")
    agregar_estacion(conn, "Misterios","ML5")
    agregar_estacion(conn, "La Raza","ML5")
    agregar_estacion(conn, "Autobuses del Norte","ML5")
    agregar_estacion(conn, "Instituto del Petroleo","ML5")
    agregar_estacion(conn, "Politecnico","ML5")

    # Estaciones de la linea 6
    agregar_estacion(conn, "El Rosario","ML6")
    agregar_estacion(conn, "Tezozomoc","ML6")
    agregar_estacion(conn, "UAM Azcapotzalco","ML6")
    agregar_estacion(conn, "Ferreria","ML6")
    agregar_estacion(conn, "Norte 45","ML6")
    agregar_estacion(conn, "Vallejo","ML6")
    agregar_estacion(conn, "Instituto del Petroleo","ML6")
    agregar_estacion(conn, "Lindavista","ML6")
    agregar_estacion(conn, "Deportivo 18 de marzo","ML6")
    agregar_estacion(conn, "La Villa-Basilica","ML6")
    agregar_estacion(conn, "Martin Carrera","ML6")

    # Estaciones de la linea 7
    agregar_estacion(conn, "El Rosario","ML7")
    agregar_estacion(conn, "Aquiles Serdan","ML7")
    agregar_estacion(conn, "Camarones","ML7")
    agregar_estacion(conn, "Refineria","ML7")
    agregar_estacion(conn, "Tacuba","ML7")
    agregar_estacion(conn, "San Joaquin","ML7")
    agregar_estacion(conn, "Polanco","ML7")
    agregar_estacion(conn, "Auditorio","ML7")
    agregar_estacion(conn, "Constituyentes","ML7")
    agregar_estacion(conn, "Tacubaya","ML7")
    agregar_estacion(conn, "San pedro de los Pinos","ML7")
    agregar_estacion(conn, "San antonio","ML7")
    agregar_estacion(conn, "Mixcoac","ML7")
    agregar_estacion(conn, "Barranca del Muerto","ML7")

    # Estaciones de la linea 8
    agregar_estacion(conn, "Garibaldi","ML8")
    agregar_estacion(conn, "Bellas Artes","ML8")
    agregar_estacion(conn, "San Juan de Letran","ML8")
    agregar_estacion(conn, "Salto del Agua","ML8")
    agregar_estacion(conn, "Doctores","ML8")
    agregar_estacion(conn, "Obrera","ML8")
    agregar_estacion(conn, "Chabacano","ML8")
    agregar_estacion(conn, "La Viga","ML8")
    agregar_estacion(conn, "Santa Anita","ML8")
    agregar_estacion(conn, "Coyuya","ML8")
    agregar_estacion(conn, "Iztacalco","ML8")
    agregar_estacion(conn, "Apatlaco","ML8")
    agregar_estacion(conn, "Aculco","ML8")
    agregar_estacion(conn, "Escuadron 201","ML8")
    agregar_estacion(conn, "Atlalilco","ML8")
    agregar_estacion(conn, "Iztapalapa","ML8")
    agregar_estacion(conn, "Cerro de la Estrella","ML8")
    agregar_estacion(conn, "UAM-I","ML8")
    agregar_estacion(conn, "Constitucion de 1917","ML8")

    # Estaciones de la linea 9
    agregar_estacion(conn, "Tacubaya","ML9")
    agregar_estacion(conn, "Patriotismo","ML9")
    agregar_estacion(conn, "Chilpancingo","ML9")
    agregar_estacion(conn, "Centro Medico","ML9")
    agregar_estacion(conn, "Lazaro Cardenas","ML9")
    agregar_estacion(conn, "Chabacano","ML9")
    agregar_estacion(conn, "Jamaica","ML9")
    agregar_estacion(conn, "Mixiuhca","ML9")
    agregar_estacion(conn, "Velodromo","ML9")
    agregar_estacion(conn, "Ciudad Deportiva","ML9")
    agregar_estacion(conn, "Puebla","ML9")
    agregar_estacion(conn, "Pantitlan","ML9")

    # Estaciones de la linea A
    agregar_estacion(conn, "Pantitlan","MLA")
    agregar_estacion(conn, "Agricola Oriental","MLA")
    agregar_estacion(conn, "Canal de San Juan","MLA")
    agregar_estacion(conn, "Tepalcates","MLA")
    agregar_estacion(conn, "Guelatao","MLA")
    agregar_estacion(conn, "Penon Viejo","MLA")
    agregar_estacion(conn, "Acatitla","MLA")
    agregar_estacion(conn, "Santa Marta","MLA")
    agregar_estacion(conn, "Los Reyes","MLA")
    agregar_estacion(conn, "La Paz","MLA")

    # Estaciones de la linea B
    agregar_estacion(conn, "Ciudad Azteca","MLB")
    agregar_estacion(conn, "Plaza Aragon","MLB")
    agregar_estacion(conn, "Olimpica","MLB")
    agregar_estacion(conn, "Ecatepec","MLB")
    agregar_estacion(conn, "Muzquiz","MLB")
    agregar_estacion(conn, "Rio de los Remedios","MLB")
    agregar_estacion(conn, "Impulsora","MLB")
    agregar_estacion(conn, "Nezahualcoyotl","MLB")
    agregar_estacion(conn, "Villa de Aragon","MLB")
    agregar_estacion(conn, "Bosque de Aragon","MLB")
    agregar_estacion(conn, "Deportivo Oceania","MLB")
    agregar_estacion(conn, "Oceania","MLB")
    agregar_estacion(conn, "Romero Rubio","MLB")
    agregar_estacion(conn, "Ricardo Flores Magon","MLB")
    agregar_estacion(conn, "San Lazaro","MLB")
    agregar_estacion(conn, "Morelos","MLB")
    agregar_estacion(conn, "Tepito","MLB")
    agregar_estacion(conn, "Lagunilla","MLB")
    agregar_estacion(conn, "Garibaldi","MLB")
    agregar_estacion(conn, "Guerrero","MLB")
    agregar_estacion(conn, "Buenavista","MLB")

    # Estaciones de la linea 12
    agregar_estacion(conn, "Mixcoac","ML12")
    agregar_estacion(conn, "Insurgentes Sur","ML12")
    agregar_estacion(conn, "Hospital 20 de Noviembre","ML12")
    agregar_estacion(conn, "Zapata","ML12")
    agregar_estacion(conn, "Parque de los Venados","ML12")
    agregar_estacion(conn, "Eje Central","ML12")
    agregar_estacion(conn, "Ermita","ML12")
    agregar_estacion(conn, "Mexicaltzingo","ML12")
    agregar_estacion(conn, "Atlalilco","ML12")
    agregar_estacion(conn, "Culhuacan","ML12")
    agregar_estacion(conn, "San Andres Tomatlan","ML12")
    agregar_estacion(conn, "Lomas Estrella","ML12")
    agregar_estacion(conn, "Calle 11","ML12")
    agregar_estacion(conn, "Periferico Oriente","ML12")
    agregar_estacion(conn, "Tezonco","ML12")
    agregar_estacion(conn, "Olivos","ML12")
    agregar_estacion(conn, "Nopalera","ML12")
    agregar_estacion(conn, "Zapotitlan","ML12")
    agregar_estacion(conn, "Tlaltenco","ML12")
    agregar_estacion(conn, "Tlahuac","ML12")


    # Diccionario de estaciones
    estaciones = obtener_estaciones_id(conn)
    u = 0
    v = 0

    # Conexiones de la Linea 1
    u = estaciones[("Observatorio", "ML1")]
    v = estaciones[("Tacubaya", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Juanacatlan", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Chapultepec", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Sevilla", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Insurgentes", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Cuahtemoc", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Balderas", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Salto del Agua", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Isabel la Catolica", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Pino Suarez", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Merced", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Candelaria", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "San Lazaro", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Moctezuma", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Balbuena", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Boulevard Puerto Aereo", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Gomez Farias", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Zaragosa", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[( "Pantitlan", "ML1")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    # Conexiones de la Linea 1 con otras lineas
    u = estaciones[("Tacubaya", "ML1")]
    v = estaciones[("Tacuba", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Tacubaya", "ML1")]
    v = estaciones[("Tacubaya", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Balderas", "ML1")]
    v = estaciones[("Balderas", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Salto del Agua", "ML1")]
    v = estaciones[("Salto del Agua", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pino Suarez", "ML1")]
    v = estaciones[("Pino Suarez", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Candelaria", "ML1")]
    v = estaciones[("Candelaria", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("San Lazaro", "ML1")]
    v = estaciones[("San Lazaro", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML1")]
    v = estaciones[("Pantitlan", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML1")]
    v = estaciones[("Pantitlan", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML1")]
    v = estaciones[("Pantitlan", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML1")]
    v = estaciones[("Pantitlan", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 2
    u = estaciones[("Cuatro caminos", "ML2")]
    v = estaciones[("Panteones", "ML2")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tacuba", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Cuitlahuac", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Popotla", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Colegio Militar", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Normal", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Cosme", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Revolucion", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Hidalgo", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Bellas Artes", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Allende", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Zocalo", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Pino Suarez", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Antonio Abad", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Chabacano", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Viaducto", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Xola", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Villa de Cortes", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Nativitas", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Portales", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ermita", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("General Anaya", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tasquena", "ML2")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    # Conexiones de la Linea 2 con otras lineas
    u = estaciones[("Tacuba", "ML2")]
    v = estaciones[("Tacubaya", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Hidalgo", "ML2")]
    v = estaciones[("Hidalgo", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Bellas Artes", "ML2")]
    v = estaciones[("Bellas Artes", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Chabacano", "ML2")]
    v = estaciones[("Chabacano", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Chabacano", "ML2")]
    v = estaciones[("Chabacano", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Ermita", "ML2")]
    v = estaciones[("Ermita", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 3
    u = estaciones[("Indios Verdes", "ML3")]
    v = estaciones[("Deportivo 18 de marzo", "ML3")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Potrero", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("La Raza", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tlatelolco", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Guerrero", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Hidalgo", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Juarez", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Balderas", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ninos Heroes", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Hospital General", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Centro Medico", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Etiopia", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Eugenia", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Division del Norte", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Zapata", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Coyoacan", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Viveros", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Miguel Angel de Quevedo", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Copilco", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Universidad", "ML3")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    # Conexiones de la Linea 3 con otras lineas
    u = estaciones[("Deportivo 18 de marzo", "ML3")]
    v = estaciones[("Deportivo 18 de marzo", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("La Raza", "ML3")]
    v = estaciones[("La Raza", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Guerrero", "ML3")]
    v = estaciones[("Guerrero", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Centro Medico", "ML3")]
    v = estaciones[("Centro Medico", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Zapata", "ML3")]
    v = estaciones[("Zapata", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 4
    u = estaciones[("Martin Carrera", "ML4")]
    v = estaciones[("Talisman", "ML4")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Bondojito", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Consulado", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Canal del Norte", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Morelos", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Candelaria", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Fray Servando", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Jamaica", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Santa Anita", "ML4")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 4 con otras lineas
    u = estaciones[("Martin Carrera", "ML4")]
    v = estaciones[("Martin Carrera", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Consulado", "ML4")]
    v = estaciones[("Consulado", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Morelos", "ML4")]
    v = estaciones[("Morelos", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Jamaica", "ML4")]
    v = estaciones[("Jamaica", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Santa Anita", "ML4")]
    v = estaciones[("Santa Anita", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 5
    u = estaciones[("Politecnico", "ML5")]
    v = estaciones[("Instituto del Petroleo", "ML5")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Autobuses del Norte", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("La Raza", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Misterios", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Valle Gomez", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Consulado", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Eduardo Molina", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Aragon", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Oceania", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Terminal Aerea", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Hangares", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Pantitlan", "ML5")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 5 con otras lineas
    u = estaciones[("Instituto del Petroleo", "ML5")]
    v = estaciones[("Instituto del Petroleo", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Oceania", "ML5")]
    v = estaciones[("Oceania", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML5")]
    v = estaciones[("Pantitlan", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Pantitlan", "ML5")]
    v = estaciones[("Pantitlan", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 6
    u = estaciones[("El Rosario", "ML6")]
    v = estaciones[("Tezozomoc", "ML6")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("UAM Azcapotzalco", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ferreria", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Norte 45", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Vallejo", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Instituto del Petroleo", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Lindavista", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Deportivo 18 de marzo", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("La Villa-Basilica", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Martin Carrera", "ML6")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 6 con otras lineas
    u = estaciones[("El Rosario", "ML6")]
    v = estaciones[("El Rosario", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 7
    u = estaciones[("El Rosario", "ML7")]
    v = estaciones[("Aquiles Serdan", "ML7")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Camarones", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Refineria", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tacuba", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Joaquin", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Polanco", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Auditorio", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Constituyentes", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tacubaya", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San pedro de los Pinos", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San antonio", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Mixcoac", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Barranca del Muerto", "ML7")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 7 con otras lineas
    u = estaciones[("Tacuba", "ML7")]
    v = estaciones[("Tacubaya", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Mixcoac", "ML7")]
    v = estaciones[("Mixcoac", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 8
    u = estaciones[("Garibaldi", "ML8")]
    v = estaciones[("Bellas Artes", "ML8")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Juan de Letran", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Salto del Agua", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Doctores", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Obrera", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Chabacano", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("La Viga", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Santa Anita", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Coyuya", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Iztacalco", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Apatlaco", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Aculco", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Escuadron 201", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Atlalilco", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Iztapalapa", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Cerro de la Estrella", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("UAM-I", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Constitucion de 1917", "ML8")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 8 con otras lineas
    u = estaciones[("Garibaldi", "ML8")]
    v = estaciones[("Garibaldi", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Chabacano", "ML8")]
    v = estaciones[("Chabacano", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    u = estaciones[("Atlalilco", "ML8")]
    v = estaciones[("Atlalilco", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 9
    u = estaciones[("Tacubaya", "ML9")]
    v = estaciones[("Patriotismo", "ML9")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Chilpancingo", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Centro Medico", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Lazaro Cardenas", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Chabacano", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Jamaica", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Mixiuhca", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Velodromo", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ciudad Deportiva", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Puebla", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Pantitlan", "ML9")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 9 con otras lineas
    u = estaciones[("Pantitlan", "ML9")]
    v = estaciones[("Pantitlan", "MLA")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea A
    u = estaciones[("Pantitlan", "MLA")]
    v = estaciones[("Agricola Oriental", "MLA")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Canal de San Juan", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tepalcates", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Guelatao", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Penon Viejo", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Acatitla", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Santa Marta", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Los Reyes", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("La Paz", "MLA")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea B
    u = estaciones[("Buenavista", "MLB")]
    v = estaciones[("Guerrero", "MLB")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Garibaldi", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Lagunilla", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tepito", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Morelos", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Lazaro", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ricardo Flores Magon", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Romero Rubio", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Oceania", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Deportivo Oceania", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Bosque de Aragon", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Villa de Aragon", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Nezahualcoyotl", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Impulsora", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Rio de los Remedios", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Muzquiz", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ecatepec", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Olimpica", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Plaza Aragon", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ciudad Azteca", "MLB")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)

    # Conexiones de la Linea 12
    u = estaciones[("Mixcoac", "ML12")]
    v = estaciones[("Insurgentes Sur", "ML12")]

    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Hospital 20 de Noviembre", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Zapata", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Parque de los Venados", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Eje Central", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Ermita", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Mexicaltzingo", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Atlalilco", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Culhuacan", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("San Andres Tomatlan", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Lomas Estrella", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Calle 11", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Periferico Oriente", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tezonco", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Olivos", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Nopalera", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Zapotitlan", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tlaltenco", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
    u = v

    v = estaciones[("Tlahuac", "ML12")]
    agregar_conexion(conn, u, v)
    agregar_conexion(conn, v, u)
