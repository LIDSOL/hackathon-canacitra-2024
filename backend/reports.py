from ai import ai_guess_report

# Añadir un reporte de un usuario
# INPUT: id_usuario, mensaje
# OUTPUT: NONE
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
def get_user_reports(conn, id_usuario) -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT linea FROM reportes_usuario WHERE usuario = ? AND fecha > datetime('now', '-1 hour')", (id_usuario,))
    return [report[0] for report in cursor.fetchall()]

# Test
#from db import *

#conn = conexion_base_de_datos()
#user_report(conn, 1, "La linea 3 y 6 va lentisima, llevamos 20 minutos parados en Zapata")

#print(get_user_reports(conn, 1)) # ['ML3', 'ML6']


