from ai import ai_guess_report
from db import actualizar_linea
from scrape import save_oficial_reports

# Añadir un reporte de un usuario
# INPUT: id_usuario, mensaje
# OUTPUT: NONE
#user_report(conn, 1, "La linea 3 y 6 va lentisima, llevamos 20 minutos parados en Zapata")
#Res: Agrega los reportes de las lineas 3 y 6 a la base de datos
def user_report(conn, id_usuario, mensaje) -> None:
    cursor = conn.cursor()

    lineas_afectadas = ai_guess_report(mensaje)

    for linea in lineas_afectadas:
        # Verificar que no haya reportado la misma linea en la ultima hora
        cursor.execute("SELECT id FROM reportes_usuario WHERE usuario = ? AND linea = ? AND fecha > datetime('now', '-1 hour')", (id_usuario, linea))

        # Si ya reporto la linea en la ultima hora, actualizar el timestamp
        if cursor.fetchone():
            cursor.execute("UPDATE reportes_usuario SET fecha = datetime('now') WHERE usuario = ? AND linea = ?", (id_usuario, linea))
        # Si no, agregar el reporte
        else:
            cursor.execute("INSERT INTO reportes_usuario (usuario, linea) VALUES (?, ?)", (id_usuario, linea))
    conn.commit()

# Obtener reportes de la ultima hora de un usuario
# INPUT: id_usuario
# OUTPUT: lista de lineas reportadas
#get_user_reports(conn, 1)
#Res: ['ML3', 'ML6']
def get_user_reports(conn, id_usuario) -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT linea FROM reportes_usuario WHERE usuario = ? AND fecha > datetime('now', '-1 hour')", (id_usuario,))
    return [report[0] for report in cursor.fetchall()]

# Obtener numero de reportes de la ultima hora en una linea
# INPUT: linea
# OUTPUT: numero de reportes
# get_line_reports(conn, 'ML6')
# Res: 1
def get_line_reports(conn, linea) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reportes_usuario WHERE linea = ? AND fecha > datetime('now', '-1 hour')", (linea,))
    return cursor.fetchone()[0]

# Actualizar tiempos de espera de las lineas de acuerdo a los reportes
# INPUT: NONE
# OUTPUT: NONE
# update_delays(conn)
# Res: Actualiza los tiempos de espera de las lineas en la base de datos, si hay mas de 3 reportes en la ultima hora se actualiza el tiempo de espera a la cantidad de reportes, si no se actualiza a 0
# Para comprobar los cambios se puede usar bad_lines_list(conn), funcion que se encuentra en maps.py
def update_delays(conn) -> None:
    cursor = conn.cursor()

    save_oficial_reports(conn)

    # Obtener todas las lineas
    cursor.execute("SELECT nombre FROM lineas")
    lineas = [linea[0] for linea in cursor.fetchall()]

    for linea in lineas:
        # Obtener el numero de reportes de la ultima hora
        reportes = get_line_reports(conn, linea)

        # Si hay un reporte del usuario 0 en la última hora, su valor de la fecha significa a la hora que se debe terminar el retraso
        cursor.execute("SELECT fecha FROM reportes_usuario WHERE usuario = 0 AND linea = ? AND fecha > datetime('now', '-1 hour')", (linea,))
        fecha = cursor.fetchone()
        if fecha:
            cursor.execute("SELECT strftime('%s', ?) - strftime('%s', 'now')", (fecha[0],))
            tiempo_restante = cursor.fetchone()[0]
            if tiempo_restante <= 0:
                actualizar_linea(conn, linea, 0)
                continue

        # Si hay reportes, actualizar el tiempo de espera
        if reportes > 3:
            actualizar_linea(conn, linea, reportes)
        else:
            actualizar_linea(conn, linea, 0)
    conn.commit()

# Demo
#from db import conexion_base_de_datos
#conn = conexion_base_de_datos()
#update_delays(conn)
