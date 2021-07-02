from database_controller import conexion
from psycopg2.extras import RealDictCursor

class Producto:
    
    def obtiene_productos(self):
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = ' SELECT id, sku, descripcion, unidad, proveedor from producto'
        db.execute(query)
        productos = db.fetchall()
        db.close()
        return productos

    def obtiene_producto_por_id(self, producto_id):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = 'SELECT sku, descripcion, unidad, proveedor from producto Where id = %s'
            db.execute(query,(producto_id,))
            producto = db.fetchone()
            db.close()
            return producto
        except Exception as e:
            return None
    
    def obtiene_producto_por_sku(self, sku):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = 'SELECT id, sku, descripcion, unidad, proveedor  from producto Where sku = %s'
            db.execute(query, (sku.upper(),))
            producto = db.fetchone()
            db.close()
            return producto
        except Exception as e:
            return None
        
    def inserta_producto(self, producto):
        try:
            db = conexion.cursor()
            query = 'INSERT INTO producto (sku, descripcion, unidad, proveedor) VALUES(%s,%s,%s,%s)'
            db.execute(
                        query,
                        (
                            producto['sku'].upper(),
                            producto['descripcion'],
                            producto['unidad'],
                            producto['proveedor']
                        )
                    )
            conexion.commit()
            db.close()
            return {
                'statusCode': 200,
                'mensaje': ' producto ingresado correctamente'
            }
        except Exception as e:
            return e
    def actualiza_producto(self, producto):
        try:
            db = conexion.cursor()
            query = ' UPDATE producto set sku = %s, descripcion = %s, unidad = %s, proveedor = %s where id = %s'
            db.execute(
                        query,
                        (
                            producto['sku'].upper(),
                            producto['descripcion'],
                            producto['unidad'],
                            producto['proveedor'],
                            producto['producto_id'],
                        )
                    )
            conexion.commit()
            db.close()
            return {
                'statusCode': 200,
                'mensaje': ' el producto con el id: '+producto['producto_id']+' ha sido actualizado correctamente'
            }
        except Exception as e:
            return e

    def comprueba_sku(self, producto_id, sku):
        try:
            db = conexion.cursor()
            query = 'SELECT sku from producto Where sku = %s and id != %s'
            db.execute(query, (sku.upper(), producto_id))
            producto = db.fetchone()
            db.close()
            return producto
        except Exception as e:
            return None

    def obtiene_prodcutos_por_proveedor(self, proveedor):
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = 'SELECT id, sku, descripcion, unidad, proveedor from producto where proveedor = %s'
        db.execute(query, (proveedor,))
        productos = db.fetchall()
        db.close()
        return productos