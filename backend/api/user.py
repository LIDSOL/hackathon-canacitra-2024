def agregar_usuario(conn, nombre, email, contrasena) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, contrasena) VALUES (?, ?)", (nombre, contrasena))
    conn.commit()

def comprobar_credenciales(conn, email, contrasena) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        return False
    return resultado[0] == contrasena