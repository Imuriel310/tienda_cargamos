from database_controller import conexion
from psycopg2.extras import RealDictCursor

class Inventario:
    
    def obtiene_inventarios (self):
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = ''' SELECT inv.id, t.nombre, p.sku, inv.cantidad from inventario inv 
                    INNER JOIN producto p on p.id = inv.producto_id 
                    INNER JOIN tienda t on t.id = inv.tienda_id 
                '''
        db.execute(query)
        inventarios = db.fetchall()
        db.close()
        return inventarios
        
    def inserta_inventario(self, inventario):
        try:
            db = conexion.cursor()
            query = 'INSERT INTO inventario (tienda_id, producto_id, cantidad ) VALUES(%s,%s,%s)'
            db.execute(
                        query,
                        (
                            inventario['tienda_id'],
                            inventario['producto_id'],
                            inventario['cantidad'],
                        )
                    )
            conexion.commit()
            db.close()
            return  {
                        'statusCode': 200,
                        'body': 'producto asociado correctamente'
                    }
        except Exception as e:
            return e
    
    def busca_inventario(self, tienda_id, producto_id):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = ''' SELECT inv.id, t.nombre, p.sku, inv.cantidad from inventario inv 
                        INNER JOIN producto p on p.id = inv.producto_id 
                        INNER JOIN tienda t on t.id = inv.tienda_id
                        WHERE tienda_id = %s and producto_id = %s
                    '''
            db.execute(query,(tienda_id, producto_id))
            inventario = db.fetchone()
            db.close()
            return inventario
        except Exception as e:
            return None
    
    def inventario_por_producto_id(self, producto_id):
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = ''' SELECT inv.id, t.nombre, p.sku, inv.cantidad from inventario inv 
                    INNER JOIN producto p on p.id = inv.producto_id 
                    INNER JOIN tienda t on t.id = inv.tienda_id
                    WHERE producto_id = %s
                '''
        db.execute(query,(producto_id,))
        inventarios = db.fetchall()
        db.close()
        return inventarios
    
    def inventario_por_tienda_id(self, tienda_id):
        db = conexion.cursor(cursor_factory=RealDictCursor)
        query = ''' SELECT inv.id, t.nombre, p.sku, inv.cantidad from inventario inv 
                    INNER JOIN producto p on p.id = inv.producto_id 
                    INNER JOIN tienda t on t.id = inv.tienda_id
                    WHERE tienda_id = %s
                '''
        db.execute(query,(tienda_id,))
        inventarios = db.fetchall()
        db.close()
        return inventarios
    
    def inventario_por_id(self, inventario_id):
        try:
            db = conexion.cursor(cursor_factory=RealDictCursor)
            query = ''' SELECT inv.id, t.nombre, p.sku, inv.cantidad from inventario inv 
                        INNER JOIN producto p on p.id = inv.producto_id 
                        INNER JOIN tienda t on t.id = inv.tienda_id
                        WHERE inv.id = %s
                    '''
            db.execute(query,(inventario_id,))
            inventario = db.fetchone()
            db.close()
            return inventario
        except Exception as e:
            return None
    
    def actualiza_inventario(self, cantidad, id):
        try:
            db = conexion.cursor()
            query = ' UPDATE inventario set cantidad = %s where id = %s'
            db.execute(
                        query,
                        (
                            cantidad,
                            id
                        )
                    )
            conexion.commit()
            db.close()
            return True
        except Exception as e:
            return e
    