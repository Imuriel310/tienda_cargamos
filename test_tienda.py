from app import app
import unittest
from json import loads

# objetivo: verificar que el usuario siempre reciba una respuesta sin importar si el resultado sea
#  el deseado o no 
class TiendaTest(unittest.TestCase):
    def test_inserta_tienda(self):
        # prueba unitaria para insertar tienda
        tester = app.test_client(self)
        datos = {
            'nombre': 'tienda test',
            'descripcion': 'tienda ingresada por unittest',
            'telefono': '8745896',
            'direccion': 'direcccion unitaria'
            
        }
        response = tester.post('/tienda', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        
    def test_obtiene_tiendas(self):
        # se obtienen todas las tiendas
        tester = app.test_client(self)
        response = tester.get('/tienda')
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_tiendas_por_id(self):
        # se obtiene tienda en especifico
        params = {
            'tienda_id':1
        }
        tester = app.test_client(self)
        response = tester.get('/tienda', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
    def test_tienda_por_nombre(self):
        # se obtiene tienda por su parametro nombre
        params = {
            'nombre':'tienda test'
        }
        tester = app.test_client(self)
        response = tester.get('/tienda', query_string=params)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)

    def test_update_tienda(self):
        #  actualizacion de tienda
        tester = app.test_client(self)
        datos = {
            'tienda_id': 5,
            'nombre': 'tienda actualizada',
            'descripcion': 'tienda ingresada por unittest',
            'telefono': '8745896',
            'direccion': 'direcccion unitaria'
            
        }
        response = tester.put('/tienda', content_type='multipart/form-data', data=datos)
        statuscode = response.status_code
        datos = loads(response.data)
        self.assertEqual(statuscode, 200)
        self.assertGreater(len(datos), 0)
        

if __name__ == "__main__":
    unittest.main()