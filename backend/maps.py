from db import *

# INPUT: "NONE"
# OUTPUT: "List of lineas malas and delay in minutes of each one"
# OUTPUT FORMAT: [("ML1", 30), ("ML2", 20), ..., ("linea", delay)]
def bad_lines_list(conn) -> list:
    cursor = conn.cursor()
    bad_lines = []
    query = "SELECT tiempo_estimado_evento FROM conexiones WHERE estacion_origen = ? AND estacion_destino = ?"

    estaciones_id = obtener_estaciones_id(conn)

    # Estado linea 1
    cursor.execute(query, (estaciones_id[("Juanacatlan", "ML1")], estaciones_id[("Chapultepec", "ML1")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML1", tiempo_estimado_evento))

    # Estado linea 2
    cursor.execute(query, (estaciones_id[("Cuatro caminos", "ML2")], estaciones_id[("Panteones", "ML2")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML2", tiempo_estimado_evento))

    # Estado linea 3
    cursor.execute(query, (estaciones_id[("Indios Verdes", "ML3")], estaciones_id[("Deportivo 18 de marzo", "ML3")]))
    tiempo_estimado_evento = cursor.fetchone()[0]


    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML3", tiempo_estimado_evento))

    # Estado linea 4
    cursor.execute(query, (estaciones_id[("Martin Carrera", "ML4")], estaciones_id[("Talisman", "ML4")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML4", tiempo_estimado_evento))

    # Estado linea 5
    cursor.execute(query, (estaciones_id[("Politecnico", "ML5")], estaciones_id[("Instituto del Petroleo", "ML5")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML5", tiempo_estimado_evento))

    # Estado linea 6
    cursor.execute(query, (estaciones_id[("El Rosario", "ML6")], estaciones_id[("Tezozomoc", "ML6")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML6", tiempo_estimado_evento))

    # Estado linea 7
    cursor.execute(query, (estaciones_id[("El Rosario", "ML7")], estaciones_id[("Aquiles Serdan", "ML7")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML7", tiempo_estimado_evento))

    # Estado linea 8
    cursor.execute(query, (estaciones_id[("Garibaldi", "ML8")], estaciones_id[("Bellas Artes", "ML8")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML8", tiempo_estimado_evento))

    # Estado linea 9
    cursor.execute(query, (estaciones_id[("Tacubaya", "ML9")], estaciones_id[("Patriotismo", "ML9")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML9", tiempo_estimado_evento))

    # Estado linea A
    cursor.execute(query, (estaciones_id[("La Paz", "MLA")], estaciones_id[("Los Reyes", "MLA")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("MLA", tiempo_estimado_evento))

    # Estado linea B
    cursor.execute(query, (estaciones_id[("Ciudad Azteca", "MLB")], estaciones_id[("Plaza Aragon", "MLB")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("MLB", tiempo_estimado_evento))

    # Estado linea 12
    cursor.execute(query, (estaciones_id[("Mixcoac", "ML12")], estaciones_id[("Insurgentes Sur", "ML12")]))
    tiempo_estimado_evento = cursor.fetchone()[0]

    if tiempo_estimado_evento > 0:
        bad_lines.append(("ML12", tiempo_estimado_evento))

    return bad_lines
