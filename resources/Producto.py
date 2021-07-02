from flask_restx import Resource
from  flask import request
from json import loads
from models.Producto import Producto

class ProductoResource(Resource):
    # se usa get para obtener productos ya dados de alta
    def get(self):
        # se buscan los posibles parametros para obtener los productos de difentes maneras
        parametros = request.args
        producto_id = parametros.get('producto_id', None)
        sku = parametros.get('sku', None)
        proveedor = parametros.get('proveedor')
        producto = Producto()
        # se obtiene el producto por id
        if producto_id is not None:
            
            producto_especifico = producto.obtiene_producto_por_id(producto_id)
            if producto_especifico is not None:
                # si se obtuvo el producto se regresa como respuesta
                return producto_especifico
            # si no se obtuvo el producto, se regresa mensaje de error
            return {
                'error': ' no existe un producto con el id '+ producto_id
            }
        #  se obtiene el producto por sku
        if sku is not None:
            producto_especifico = producto.obtiene_producto_por_sku(sku)
            if producto_especifico is not None: 
                # si se obtuvo el producto se regresa como respuesta
                return producto_especifico
            # si no se obtuvo el producto, se regresa mensaje de error
            return {
                'error': 'no existe el producto con el sku '+sku
            }
        if proveedor is not None:
            productos = producto.obtiene_prodcutos_por_proveedor(proveedor)
            if len(productos) > 0: 
                # si se obtuvieron productos se regresan como respuesta
                return productos
            # si no se obtuvo el producto, se regresa mensaje de error
            return {
                'error': 'no existen el productos asociados al proveedor '+proveedor
            }
        # si no se tienen parametros se obtienen todos los productos
        productos = producto.obtiene_productos()
        return productos
    # se usa post para dar de alta nuevos productos
    def post(self):
        try:
            error = ""
            parametros = request.form
            producto = Producto()
            sku = parametros.get('sku' , None)
            descripcion = parametros.get('descripcion', None)
            unidad = parametros.get('unidad', None)
            proveedor = parametros.get('proveedor', None)
            #se verifica si el sku no esta vacio, no puede haber productos sin sku
            if sku is None or sku == '':
                error =  ' se necesita un sku para el producto '
            # se verifica que no exista un producto con el mismo nombre
            if producto.obtiene_producto_por_sku(sku) is not None:
                error = ' el producto con el sku '+ sku + ' ya existe'
            if error != "":
                raise Exception(error)
            #fin de validaciones
            objeto_produto = {
                'sku': sku,
                'descripcion': descripcion,
                'unidad': unidad,
                'proveedor': proveedor
            }
            respuesta = producto.inserta_producto(objeto_produto)
            return respuesta
        except Exception as e:
            return {'error':error}
    # se usa put para editar productos
    def put(self):
        try:
            error = ""
            parametros = request.form
            producto = Producto()
            producto_id = parametros.get('producto_id', None)
            sku = parametros.get('sku' , None)
            descripcion = parametros.get('descripcion', None)
            proveedor = parametros.get('proveedor', None)
            unidad = parametros.get('unidad', None)
            #se verifica si el sku no esta vacio, no puede haber productos sin sku
            if producto_id is None:
                error = ' se necesita el parametro producto_id '
            if sku is None or sku == '':
                error =  error + ' se necesita un sku para el producto '
            if producto.obtiene_producto_por_id(producto_id) is None:
                error = error + ' el producto con el id '+ producto_id + '  no existe'
            if producto.comprueba_sku(producto_id, sku) is not None:
                error = error + ' el producto con el sku '+ sku + ' ya existe'
            if error != "":
                raise Exception(error)
            #fin de validaciones
            objeto_producto = {
                'sku': sku,
                'descripcion': descripcion,
                'proveedor': proveedor,
                'unidad': unidad,
                'producto_id': producto_id
            }
            respuesta = producto.actualiza_producto(objeto_producto)
            return respuesta
        except Exception as e:
            return {'error':error}
            
