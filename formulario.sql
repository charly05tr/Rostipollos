CREATE DATABASE formulario;
CREATE TABLE personas (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nombre TEXT, hash TEXT, correo TEXT, telefono TEXT, role TEXT);
CREATE TABLE restaurantes (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, restaurante TEXT NOT NULL);
CREATE TABLE meseros (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, restaurante_id, nombreMesero TEXT, FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id));
CREATE TABLE calidadServicio (id_mesero, id_cliente, comentario TEXT, calidad_servicio TEXT, amabilidad TEXT, promo TEXT, fecha TEXT,  FOREIGN KEY (id_mesero) REFERENCES meseros(id), FOREIGN KEY (id_cliente) REFERENCES personas(id));
CREATE TABLE calidadInstalaciones (id_restaurante, id_cliente, ambiente TEXT, limpiezaBaños TEXT, calidad_comida TEXT, FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id), FOREIGN KEY (id_cliente) REFERENCES personas(id));


