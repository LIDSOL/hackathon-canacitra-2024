# Agregar un usuario a la base de datos
# INPUT: "Juan", "juan@email.com", "password"
# OUTPUT: "NONE"
def add_user(conn, name, email, password) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()

# Comprobar credenciales de un usuario
# INPUT: "email", "password"
# OUTPUT: "True" si las credenciales son correctas, "False" si no
def check_login(conn, email, password) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE correo = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        return False
    return resultado[0] == password

# Obtener el id de un usuario por su correo
# INPUT: "email"
# OUTPUT: "id" del usuario
def get_user_id(conn, email) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (email,))
    return cursor.fetchone()[0]

# Cambiar el nombre de un usuario
# INPUT: "id", "new_name"
# OUTPUT: "NONE"
def change_user_name(conn, id, new_name) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (new_name, id))
    conn.commit()

# Obtener el nombre de un usuario por su id
# INPUT: "id"
# OUTPUT: "name" del usuario
def get_user_name(conn, id) -> str:
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM usuarios WHERE id = ?", (id,))
    return cursor.fetchone()[0]