# blueprints/documented_endpoints/__init__.py
from flask import Blueprint
from flask_restplus import Api
from flask_restplus.apidoc import apidoc
from routes.operations import namespace as operations_ns
from routes.users import namespace as users_ns
from routes.auth import namespace as auth_ns
from routes.coin import namespace as coin_ns

apidoc.url_prefix = "/api"
blueprint = Blueprint('Endpoints', __name__)

 
authorizations = {
    'protected': {
            'type': 'oauth2',
            'flow': 'password',
            'tokenUrl': '/auth',
            'scopes': {
                'read': 'Esto seria un permiso de escritura',
                'write': 'Y esto uno de escritura',
            }
        }
}

api_extension = Api(
    blueprint,
    title='Ripio Coin System API',
    version='1.0',
    description="Application flask/flask-restplus para implementacion de sistema rest spara envio de monedas entre usuarios",
    doc='/doc',
    authorizations=authorizations
)

api_extension.add_namespace(operations_ns)
api_extension.add_namespace(users_ns)
api_extension.add_namespace(auth_ns)
api_extension.add_namespace(coin_ns)