from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from models.users import User
from utils import encode_auth_token, HTTPException
namespace = Namespace('auth', 'Endpoints de autenticacion')


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Nombre de usuario', location='form')
login_parser.add_argument('password', type=str, required=True, help='Contraseña de usuario', location='form')



@namespace.route('')
class UserEndpoints(Resource):

    @namespace.expect(login_parser)
    def post(self):
        '''Logueo de usuario'''
        try:
            args = login_parser.parse_args()
            username = args["username"] 
            password = args["password"] 
            user: User = User.query.filter_by(username=username).first()
            if not user:
                raise HTTPException(
                    "Usuario inexistente",
                    status_code=401
                )
            if user.password != password:
                raise HTTPException(
                    "Contraseña incorrecta",
                    status_code=401
                )
            token = encode_auth_token(user.id)
            return {
                "access_token":token.decode(),
                "token_type":"bearer"
            }
        except HTTPException as e:
            return e.response()
        #except Exception as e:
        #    return HTTPException.unespected(str(e))
        
