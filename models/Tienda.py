from database_controller import conexion
from psycopg2.extras import RealDictCursor
import json

class Tienda:
    
    def obtiene_tiendas(self):
        # se usa el realDictCursor para mapear las columnas de la tabla con sus respectivos valores
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = ' SELECT id, nombre, descripcion, direccion, telefono from tienda '
        db.execute(query)
        tiendas = db.fetchall()
        db.close()
        return tiendas

    def obtiene_tienda_por_id(self, tienda_id):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = 'SELECT nombre, descripcion, direccion, telefono from tienda Where id = %s'
            db.execute(query, (tienda_id,))
            tienda = db.fetchone()
            db.close()
            return tienda
        except Exception as e:
            return None
    
    def obtiene_tienda_por_nombre(self, nombre):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = 'SELECT id, nombre, descripcion, direccion, telefono from tienda Where nombre = %s'
            db.execute(query, (nombre.upper(),))
            tienda = db.fetchone()
            db.close()
            return tienda
        except Exception as e:
            return None
        
    def inserta_tienda(self, tienda):
        try:
            db = conexion.cursor()
            query = 'INSERT INTO tienda (nombre, descripcion, direccion, telefono) VALUES(%s,%s,%s,%s)'
            db.execute(
                        query,
                        (
                            tienda['nombre'].upper(),
                            tienda['descripcion'],
                            tienda['direccion'],
                            tienda['telefono']
                        )
                    )
            conexion.commit()
            db.close()
            return {
                'statusCode': 200,
                'mensaje': ' tienda ingresada correctamente'
            }
        except Exception as e:
            return e
    def actualiza_tienda(self, tienda):
        try:
            db = conexion.cursor()
            query = ' UPDATE tienda set nombre = %s, descripcion = %s, direccion = %s, telefono = %s where id = %s'
            db.execute(
                        query,
                        (
                            tienda['nombre'].upper(),
                            tienda['descripcion'],
                            tienda['direccion'],
                            tienda['telefono'],
                            tienda['tienda_id']
                        )
                    )
            conexion.commit()
            db.close()
            return {
                'statusCode': 200,
                'mensaje': ' la tienda con el id: '+tienda['tienda_id']+' ha sido actualizada correctamente'
            }
        except Exception as e:
            return e
    def comprueba_nombre(self, tienda_id, nombre):
        try:
            db = conexion.cursor()
            query = 'SELECT nombre from tienda Where nombre = %s and id != %s'
            db.execute(query, (nombre.upper(), tienda_id))
            tienda = db.fetchone()
            db.close()
            return tienda
        except Exception as e:
            return None