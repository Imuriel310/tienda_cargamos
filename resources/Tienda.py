from flask_restx import Resource
from  flask import request
from json import loads
from models.Tienda import Tienda

class TiendaResource(Resource):
    # se usa get para obtener tiendas ya creadas
    def get(self):
        # si se buscan los posibles parametros para obtener tiendas
        parametros = request.args
        tienda_id = parametros.get('tienda_id', None)
        nombre = parametros.get('nombre', None)
        tienda = Tienda()
        # se obtiene la tienda por id
        if tienda_id is not None:
            tienda_especifica = tienda.obtiene_tienda_por_id(tienda_id)
            if tienda_especifica is not None:
                return tienda_especifica
            return {
                        'error': " no existe una tienda con el id: "+ tienda_id
                    }
        #  se obtiene la tienda por nombra
        if nombre is not None:
            tienda_especifica = tienda.obtiene_tienda_por_nombre(nombre)
            if tienda_especifica is not None: 
                return tienda_especifica
            return {
                'error': 'no existe una tienda con el nombre '+ nombre
            }
        # si no se tienen parametros se obtienen todas las tiendas
        tiendas = tienda.obtiene_tiendas()
        return tiendas
    # se usa post para dar de alta nuevas tiendas
    def post(self):
        try:
            error = ""
            parametros = request.form
            tienda = Tienda()
            nombre = parametros.get('nombre' , None)
            descripcion = parametros.get('descripcion', None)
            telefono = parametros.get('telefono', None)
            direccion = parametros.get('direccion', None)
            #se verifica si el nombre no esta vacio, no puede haber tiendas sin nombre
            if nombre is None or nombre == '':
                error =  ' se necesita un nombre para la tienda '
            # se verifica que no exista una tienda con el mismo nombre
            if tienda.obtiene_tienda_por_nombre(nombre) is not None:
                error = ' la tienda con el nombre '+ nombre + ' ya existe'
            if error != "":
                raise Exception(error)
            #fin de validaciones
            objeto_tienda = {
                'nombre': nombre,
                'descripcion': descripcion,
                'telefono': telefono,
                'direccion': direccion
            }
            respuesta = tienda.inserta_tienda(objeto_tienda)
            return respuesta
        except Exception as e:
            return {'error':error}
    # se usua put para editar tiendas
    def put(self):
        try:
            error = ""
            parametros = request.form
            tienda = Tienda()
            tienda_id = parametros.get('tienda_id', None)
            nombre = parametros.get('nombre' , None)
            descripcion = parametros.get('descripcion', None)
            telefono = parametros.get('telefono', None)
            direccion = parametros.get('direccion', None)
            #se verifica si el nombre no esta vacio, no puede haber tiendas sin nombre
            if tienda_id is None or tienda_id == '':
                error = ' se necesita el parametro tienda_id '
            if nombre is None or nombre == '':
                error =  error + ' se necesita un nombre para la tienda '
            if tienda.obtiene_tienda_por_id(tienda_id) is None:
                error = error + ' la tienda con el id '+ tienda_id + '  no existe'
            if tienda.comprueba_nombre(tienda_id, nombre) is not None:
                error = error + ' la tienda con el nombre '+ nombre + ' ya existe'
            if error != "":
                raise Exception(error)
            #fin de validaciones
            objeto_tienda = {
                'nombre': nombre,
                'descripcion': descripcion,
                'telefono': telefono,
                'direccion': direccion,
                'tienda_id': tienda_id
            }
            respuesta = tienda.actualiza_tienda(objeto_tienda)
            return respuesta
        except Exception as e:
            return {'error':error}
            
