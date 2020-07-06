from manage_conection import postgresController
import configs
import psycopg2


def version():
    pc = postgresController(configs.db_config)
    cur, con = pc.get_instance()
    cur.execute("SELECT version();")
    record = cur.fetchone()
    pc.close_manager()
    return ("You are connected to -" + str(record) + "\n")


def create_db():
    pc = postgresController(configs.db_config)
    cur, con = pc.get_instance()
    cur.execute("""CREATE TABLE IF NOT EXISTS pais (
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
  FOREIGN KEY (ciudad_id) REFERENCES ciudad(id_ciudad)
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
);""")
    cur.execute("""
insert INTO pais (nombre) select 'colombia' where not exists (select nombre from pais where nombre = 'colombia');
insert INTO ciudad (nombre, pais_id) select 'Bogota', '1' where not exists (select nombre from ciudad where nombre = 'Bogota');
insert INTO tipoMvto (descripcion) select 'consignacion' where not exists (select descripcion from tipomvto where descripcion = 'consignacion');
insert INTO tipoMvto (descripcion) select 'retiro' where not exists (select descripcion from tipomvto where descripcion = 'retiro');""")
    con.commit()
    pc.close_manager()
    return ("Ok se realizo la operacion \n")


def consultValue(data):
    email = data["email"]
    pc = postgresController(configs.db_config)
    cur, con = pc.get_instance()
    cur.execute(
        "select saldo from cuenta join cliente on cliente.id_cliente = cuenta.cliente_id where cliente.email = (%s);", [email])
    result = cur.fetchone()
    pc.close_manager()
    return ("Su saldo es: " + str(result[0]) + "\n")

def updateBalance(cur, con, email):
  cur.execute(""" update cuenta c
    set saldo = (
	  select
  	sum(mv.vlrmovimiento) as total
  	from movimiento mv
  	join cuenta cc on mv.numero_cuenta = cc.numero_cuenta
  	join cliente cl on cc.cliente_id = cl.id_cliente
  	where cl.email = (%s)
    ) 
    from cliente cli
    where c.cliente_id = cli.id_cliente
    and cli.email = (%s);""", (email, email))
  con.commit()

def makeTransaction(cur, con, data_tuple):
  cur.execute("""insert into movimiento (numero_cuenta, tipomvto_id, vlrmovimiento) values (
  (select numero_cuenta from cuenta join cliente on cliente.id_cliente = cuenta.cliente_id where cliente.email = %s), 
  (select id_tipomvto from tipomvto where id_tipomvto = %s), %s);""", data_tuple)
  con.commit()

def consignment(data):
  email = data["email"]
  value = abs(float(data["valor"]))
  pc = postgresController(configs.db_config)
  cur, con = pc.get_instance()
  makeTransaction(cur, con, (email, 1, value))
  updateBalance(cur, con, email)
  pc.close_manager()
  return ("¡Consignacion Realizada!")

def retirement(data):
  email = data["email"]
  value = abs(float(data["valor"]))
  pc = postgresController(configs.db_config)
  cur, con = pc.get_instance()
  cur.execute("select saldo from cuenta join cliente on cliente.id_cliente = cuenta.cliente_id where cliente.email = (%s);", [email])
  result = cur.fetchone()
  if result:
    if result[0] <= 0:
      return("Sin fondos")
    elif result[0] < value:
      return("Saldo insuficiente")
    else:
      makeTransaction(cur, con, (email, 2, -value))
      updateBalance(cur, con, email)
      pc.close_manager()
      return("!Retiro realizado¡")
  else:
    return ("Error en los datos de ingreso")


def create_client(data):
    name = data["nombres"]
    last_name = data["apellidos"]
    email = data["email"]
    phone = data["telefono"]
    city = data["ciudad"]
    pc = postgresController(configs.db_config)
    cur, con = pc.get_instance()
    cur.execute("insert into telefono (numero) values (%s)", [phone])
    cur.execute("insert into cliente (nombres, apellidos, email, ciudad_id, telefono_id) values (%s, %s, %s, %s, (select id_telefono from telefono where numero = %s)) ",
                (name, last_name, email, city, phone))
    cur.execute(
        "insert into cuenta (saldo, cliente_id) values (%s, (select id_cliente from cliente where email = %s))", (0, email))
    con.commit()
    pc.close_manager()
    return ("¡Cliente creado!")