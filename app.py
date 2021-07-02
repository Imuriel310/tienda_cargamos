from flask import Flask
from flask_restx import Api
from flask import Blueprint
from resources.Tienda import TiendaResource
from resources.Producto import ProductoResource
from resources.Inventario import InventarioResource
import database_controller

app = Flask(__name__)
api = Api(app)
database_controller.crea_base_de_datos()
if __name__ == '__main__':
    app.run(debug=True)
    

application = Blueprint("api", __name__)
api.add_resource(TiendaResource, '/tienda')
api.add_resource(ProductoResource, '/producto')
api.add_resource(InventarioResource, '/inventario')