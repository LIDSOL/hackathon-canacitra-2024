# Agregar un usuario a la base de datos
def add_user(conn, name, email, password) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()

# Comprobar credenciales de un usuario
def check_login(conn, email, password) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE correo = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        return False
    return resultado[0] == password