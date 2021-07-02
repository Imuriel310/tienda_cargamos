import psycopg2

# se crea conexion a base de datos cargamos
conexion = psycopg2.connect(dbname='cargamos', user='postgres', host='localhost', password='postgres')
db = conexion.cursor()
# metodo solo ejecutado al iniciar la aplicacion 
def crea_base_de_datos():
    sql_tienda = '''CREATE TABLE IF NOT EXISTS tienda(
            id serial PRIMARY KEY,
            nombre varchar(20),
            direccion varchar(50),
            telefono varchar(15),
            descripcion TEXT
        )'''

    sql_prducto = '''CREATE TABLE IF NOT EXISTS producto(
            id serial PRIMARY KEY,
            sku varchar(20),
            descripcion TEXT,
            unidad varchar(10),
            proveedor varchar(50)
        )'''

    sql_inventario = '''CREATE TABLE IF NOT EXISTS inventario(
            id serial PRIMARY KEY,
            tienda_id INT,
            producto_id INT,
            cantidad float,
            CONSTRAINT fk_tienda
                FOREIGN KEY(tienda_id)
                    REFERENCES tienda(id),
            CONSTRAINT fk_producto
                FOREIGN KEY(producto_id)
                    REFERENCES producto(id)
            
        )'''
        
    db.execute(sql_tienda)
    db.execute(sql_prducto)
    db.execute(sql_inventario)
    db.close()

# db = psycopg2.connect("user=test password='test'");
# cursor = db.cursor();
# cursor.execute("create database prueba")
