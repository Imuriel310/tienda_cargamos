from app import app
import unittest
from json import loads
# objetivo: verificar que el usuario siempre reciba una respuesta sin importar si el resultado sea
#  el deseado o no 
class ProductoTest(unittest.TestCase):
    def test_inserta_producto(self):
        # insercion de nuevo producto
        tester = app.test_client(self)
        datos = {
            'sku': 'unit-test',
            'descripcion': 'producto ingresado por unittest',
            'unidad': 'kg',
            'proveedor': 'pruebas automatizadas'
            
        }
        response = tester.post('/producto', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        
    def test_obtiene_producto(self):
        # obtencion de productos
        tester = app.test_client(self)
        response = tester.get('/producto')
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_producto_por_id(self):
        # obtencion de producto por id
        params = {
            'producto_id':1
        }
        tester = app.test_client(self)
        response = tester.post('/producto', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_producto_por_sku(self):
        # obtencion de producto por sku
        params = {
            'sku':'unit-test'
        }
        tester = app.test_client(self)
        response = tester.get('/producto', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
    
    def test_producto_por_proveedor(self):
        # se obtienen los productos de un proveedor en especifico
        params = {
            'proveedor':'cargamos'
        }
        tester = app.test_client(self)
        response = tester.get('/producto', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_update_producto(self):
        # actualizacion de producto
        tester = app.test_client(self)
        datos = {
            'producto_id': 2,
            'sku': 'unit-test',
            'descripcion': 'producto ingresado por unittest',
            'unidad': 'pieza',
            'proveedor': 'cargamos'
            
        }
        response = tester.put('/producto', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        

if __name__ == "__main__":
    unittest.main()