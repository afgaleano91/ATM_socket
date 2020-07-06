CREATE TABLE IF NOT EXISTS pais (
  id_pais serial PRIMARY KEY,
  nombre VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS ciudad (
  id_ciudad serial PRIMARY KEY,
  nombre VARCHAR(20),
  pais_id INTEGER,
  FOREIGN KEY (pais_id) REFERENCES pais(id_pais)
);

CREATE TABLE IF NOT EXISTS telefono (
  id_telefono serial PRIMARY KEY,
  numero VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS cliente (
  id_cliente serial PRIMARY KEY,
  nombres VARCHAR(30),
  apellidos VARCHAR(30),
  email VARCHAR(30) NOT NULL,
  telefono_id INTEGER,
  ciudad_id INTEGER,
  FOREIGN KEY (telefono_id) REFERENCES telefono(id_telefono),
  FOREIGN KEY (ciudad_id) REFERENCES telefono(id_telefono)
);

CREATE TABLE IF NOT EXISTS cuenta (
  numero_cuenta serial PRIMARY KEY,
  saldo NUMERIC(10, 2),
  FcApertura TIMESTAMP default current_timestamp,
  cliente_id INTEGER,
  FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente)
);

CREATE TABLE IF NOT EXISTS tipoMvto (
  id_tipoMvto serial PRIMARY KEY,
  descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS movimiento (
  id_movimiento serial PRIMARY KEY,
  numero_cuenta INTEGER,
  Fmovimiento TIMESTAMP default current_timestamp,
  tipoMvto_id INTEGER,
  VlrMovimiento NUMERIC(10, 2),
  FOREIGN KEY (numero_cuenta) REFERENCES cuenta(numero_cuenta),
  FOREIGN KEY (tipoMvto_id) REFERENCES tipoMvto(id_tipoMvto)
);

INSERT INTO pais (nombre) VALUES ("colombia");
INSERT INTO ciudad (nombre, pais_id) VALUES ("Bogota", '1');