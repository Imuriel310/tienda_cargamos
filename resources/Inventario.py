import re
from flask_restx import Resource
from  flask import request
from json import loads
from models.Inventario import Inventario
from models.Producto import Producto
from models.Tienda import Tienda

def compra(inventario_especifico, cantidad):
    inventario = Inventario()
    cantidad_final = inventario_especifico['cantidad'] + cantidad
    inventario.actualiza_inventario(cantidad_final, inventario_especifico['id'])
    return {
                'mensaje' :' compra realizada correctamente '
            }
def venta(inventario_especifico, cantidad):
    inventario = Inventario()
    cantidad_final = inventario_especifico['cantidad'] - cantidad
    if cantidad_final < 0:
        # si la cantidad final es menor a 0 no se puede realizar la venta
        return {'error': 'no se dispone de stock suficiente'}
    inventario.actualiza_inventario(cantidad_final, inventario_especifico['id'])
    return {
                'mensaje' :' venta realizada correctamente '
            }
class InventarioResource(Resource):
    # se usa get para obtener los inventarios ya dados de alta
    def get(self):
        # se buscan los posibles parametros para obtener inventarios de diferentes maneras
        parametros = request.args
        producto_sku = parametros.get('producto_sku', None)
        tienda_nombre = parametros.get('tienda_nombre', None)
        inventario_id = parametros.get('inventario_id', None)
        inventario = Inventario()
        producto = Producto()
        tienda = Tienda()
        # CASO 1
        # si se obtiene un sku y un nombre de tienda, se busca un inventario en especifico
        if producto_sku is not None and tienda_nombre is not None:
            producto_especifico = producto.obtiene_producto_por_sku(producto_sku)
            tienda_especifica = tienda.obtiene_tienda_por_nombre(tienda_nombre)
            if producto_especifico is None:
                return {
                    'error': ' no existe un producto con el sku '+ producto_sku
                }
            if tienda_especifica is None:
                return {
                    'error': ' no existe una tienda con el nombre '+ tienda_nombre
                }
            inventario_especifico = inventario.busca_inventario(tienda_especifica['id'],producto_especifico['id'])
            if inventario_especifico is None:
                return {
                    'error': ' la tienda  '+ tienda_nombre + ' no tiene el producto '+ producto_sku 
                }
            return inventario_especifico
        # FIN CASO 1
        # CASO 2
        # se obtienen todas las tiendas que tengan el producto sku recibido
        if producto_sku is not None:
            
            producto_especifico = producto.obtiene_producto_por_sku(producto_sku)
            if producto_especifico is not None:
                inventarios = inventario.inventario_por_producto_id(producto_especifico['id'])
                if len(inventarios) > 0:
                    return inventarios
                return {
                    'mensaje': ' no se encontaron tiendas que tengan el producto '+ producto_sku
                }
            return {
                'error': ' no existe un producto con el sku '+ producto_sku
            }
        # FIN CASO 2
        
        # CASO 3
        # se obtienen todos los productos de una tienda
        if tienda_nombre is not None:
            
            tienda_especifica = tienda.obtiene_tienda_por_nombre(tienda_nombre)
            if tienda_especifica is not None:
                inventarios = inventario.inventario_por_tienda_id(tienda_especifica['id'])
                if len(inventarios ) > 0:
                    return inventarios
                return {
                        'mensaje': ' la tienda' + tienda_nombre + ' no tiene ningun producto '
                    }
            return {
                'error': ' no existe una tienda con el nombre '+ tienda_nombre
            }
        # FIN CASO 3
        
        # CASO 4
        # si se recibio un inventario_id se regresa el inventario en especifico
        if inventario_id is not None:
            inventario_especifico = inventario.inventario_por_id(int(inventario_id))
            if inventario_especifico is None:
                return {
                    'error': ' el inventario con el id '+ inventario_id + ' no existe'
                }
            return inventario_especifico
        
        #FIN CASO 4
        
        #  si no se obtuvo ningun parametro se regresan todos los inventarios existentes
        inventarios = inventario.obtiene_inventarios()
        return inventarios
    
    # se usa post para dar de alta nuevos productos a tiendas
    def post(self):
        try:
            error = ""
            parametros = request.form
            inventario = Inventario()
            producto = Producto()
            tienda = Tienda()
            producto_sku = parametros.get('producto_sku' , None)
            tienda_nombre = parametros.get('tienda_nombre', None)
            # PRIMERA VALIDACION
            # validacion para asegurarse que todos los parametros tengan valor
            if producto_sku is not None or producto_sku != "":
                producto_especifico = producto.obtiene_producto_por_sku(producto_sku)
            else: 
                error = error +' se necesita un sku '
            
            if tienda_nombre is not None or tienda_nombre != "":
                tienda_especifica = tienda.obtiene_tienda_por_nombre(tienda_nombre)
            else:
                error = error+ ' se necesita un nombre de tienda '
            if error != "":
                raise Exception(error)
            # FIN PRIMERA VALIDACION
            
            # SEGUNDA VALIDACION
            # se verifica la existencia del producto, tienda
            if producto_especifico is None :
                error = error + ' el producto con el sku '+ producto_sku + ' no existe'
            if tienda_especifica is None:
                error = error + ' la tienda con el nombre '+tienda_nombre+ ' no existe'
            if error != "":
                raise Exception(error)
            # FIN SEGUNDA VALIDACION
            
            # TERCERA VALIDACION
            # se verifica que la tienda no tenga ya registrado el producto recibido
            if inventario.busca_inventario(tienda_especifica['id'], producto_especifico['id']) is not None:
                error = error + ' el producto '+producto_sku+ ' ya se encuentra asociado a la tienda ' + tienda_nombre
            if error != "":
                raise Exception(error)
            #FIN TERCERA VALIDACION
            
            # se crea el nuevo inventario
            
            objeto_inventario = {
                'tienda_id': tienda_especifica['id'],
                'producto_id': producto_especifico['id'],
                'cantidad': 0
            }
            respuesta = inventario.inserta_inventario(objeto_inventario)
            return respuesta
        except Exception as e:
            return {'error':error}
    # se usa put para realizar compras y ventas de inventario
    def put(self):
        try:
            error = ""
            parametros = request.form
            producto = Producto()
            tienda = Tienda()
            inventario = Inventario()
            producto_sku = parametros.get('producto_sku', None)
            tienda_nombre = parametros.get('tienda_nombre', None)
            operacion = parametros.get('operacion', None)
            cantidad = float(parametros.get('cantidad', 0))
            # VALIDACION UNO
            #se verifica que existan todos los parametros
            if producto_sku == "" or producto_sku is None  or tienda_nombre == "" or tienda_nombre is None:
                error = ' se necesita el nombre de la tienda y el sku del producto '
            if operacion is None:
                error = error + ' se necesita especificar el tipo de operacion: compra o venta '
            if cantidad <= 0:
                error = error + ' se necesita una cantidad mayor a  0 '
            if error != "":
                raise Exception(error)
            #  FIN VALIDACION UNO
            
            # VALIDACION DOS
            # se verifica existencia de tienda y producto
            producto_especifico = producto.obtiene_producto_por_sku(producto_sku)
            tienda_especifica = tienda.obtiene_tienda_por_nombre(tienda_nombre)
            if  producto_especifico is None:
                error =   ' el producto '+ producto_sku +  ' no existe '
            if tienda_especifica is None:
                error = error + ' la tienda con el nombre '+ tienda_nombre + ' no existe'
            if operacion.upper() != 'COMPRA' and operacion.upper() != 'VENTA':
                error = error + ' operacion no valida, especificar compra o venta '
            if error != "":
                raise Exception(error)
            # FIN VALIDACION DOS
            
            # se verifica que exista un invetario con la tienda y el producto recibidos
            inventario_especifico = inventario.busca_inventario(tienda_especifica['id'], producto_especifico['id'])
            if inventario_especifico is None:
                error = " la tienda "+ tienda_nombre + " no tiene el producto con sku " + producto_sku
            # si existe el inventario se hacen las operaciones correspondientes
            if operacion.upper() == 'COMPRA':
                respuesta = compra(inventario_especifico, cantidad)
            else:
                respuesta = venta(inventario_especifico, cantidad)
            
            return respuesta
        except Exception as e:
            return {'error':error}
            
