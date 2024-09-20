-- Crear tabla de líneas de transporte
CREATE TABLE IF NOT EXISTS lineas (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Crear tabla de estaciones de transporte
CREATE TABLE IF NOT EXISTS estaciones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    linea INTEGER NOT NULL,
    FOREIGN KEY (linea) REFERENCES lineas(id)
);

-- Crear tabla de conexiones entre estaciones
CREATE TABLE IF NOT EXISTS conexiones (
    id INTEGER PRIMARY KEY,
    estacion_origen INTEGER NOT NULL,
    estacion_destino INTEGER NOT NULL,
    tiempo_estimado INTEGER NOT NULL,
    tiempo_estimado_evento INTEGER NOT NULL,
    tiempo_estimado_normal INTEGER NOT NULL,
    FOREIGN KEY (estacion_origen) REFERENCES estaciones(id),
    FOREIGN KEY (estacion_destino) REFERENCES estaciones(id)
);

-- Crear tabla de catalogo de eventos
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    tiempo_estimado INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    usuario_creador INTEGER NULL,
    FOREIGN KEY (usuario_creador) REFERENCES usuarios(id)
);

-- Crear tabla de eventos en estaciones
CREATE TABLE IF NOT EXISTS eventos_estaciones (
    id INTEGER PRIMARY KEY,
    evento INTEGER NOT NULL,
    estacion INTEGER NOT NULL,
    FOREIGN KEY (evento) REFERENCES eventos(id),
    FOREIGN KEY (estacion) REFERENCES estaciones(id)
);

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    contrasena TEXT NOT NULL
);

-- Crear tabla de ruta de usuario
CREATE TABLE IF NOT EXISTS rutas (
    id INTEGER PRIMARY KEY,
    usuario INTEGER NOT NULL,
    origen INTEGER NOT NULL,
    destino INTEGER NOT NULL,
    hora INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    FOREIGN KEY (usuario) REFERENCES usuarios(id),
    FOREIGN KEY (origen) REFERENCES estaciones(id),
    FOREIGN KEY (destino) REFERENCES estaciones(id)
);
