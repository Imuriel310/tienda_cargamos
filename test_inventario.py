from app import app
import unittest
from json import loads

class InventarioTest(unittest.TestCase):
    def test_a_inserta_inventario(self):
        tester = app.test_client(self)
        datos = {
            'producto_sku': 'unit-test',
            'tienda_nombre': 'tienda test',
            
        }
        response = tester.post('/inventario', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        
    def test_obtiene_inventarios(self):
        tester = app.test_client(self)
        response = tester.get('/inventario')
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_inventario_por_id(self):
        params = {
            'inventario_por_id':1
        }
        tester = app.test_client(self)
        response = tester.post('/inventario', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_inventario_por_sku(self):
        params = {
            'producto_sku':'unit-test'
        }
        tester = app.test_client(self)
        response = tester.get('/inventario', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        
    def test_inventario_por_tienda(self):
        params = {
            'tienda_nombre':'tienda_test'
        }
        tester = app.test_client(self)
        response = tester.get('/inventario', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_compra_inventario(self):
        tester = app.test_client(self)
        datos = {
            'producto_sku': 'unit-test',
            'tienda_nombre': 'tienda test',
            'operacion': 'compra',
            'cantidad': 200,
            'proveedor': 'cargamos'
            
        }
        response = tester.put('/inventario', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        
    def test_venta_inventario(self):
        tester = app.test_client(self)
        datos = {
            'producto_sku': 'unit-test',
            'tienda_nombre': 'tienda test',
            'operacion': 'venta',
            'cantidad': 150,
            'proveedor': 'cargamos'
            
        }
        response = tester.put('/inventario', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

if __name__ == "__main__":
    unittest.main()