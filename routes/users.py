from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from models import coin
from models.users import User
from models.shareddb import db
from models.coin import Balance
from .coin import coin_model
from utils import decode_auth_token, HTTPException

namespace = Namespace('users', 'Endpoints de usuarios')


user_model = namespace.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
})

balance_model = namespace.model("Balance",{
    "user":fields.Nested(user_model),
    "coin":fields.Nested(coin_model),
    "balance":fields.Float,
})

simple_model = namespace.model('Simple message', {
    'message': fields.String,
})

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Usuario que envia dinero', location='form')
user_parser.add_argument('password', type=str, required=True, help='Contraseña', location='form')
user_parser.add_argument('name', type=str, required=True, help='Usuario que recibe dinero', location='form')
user_parser.add_argument('amount', type=int, required=True, help='Cantidad de dinero', location='form')
user_parser.add_argument('Authorization', type=str, help='Token de authenticacion', location='headers')



@namespace.response(401, "UNAUTHORIZED", model=simple_model)
@namespace.response(500, "SERVER ERROR", model=simple_model)
@namespace.route('')
class UserEndpoints(Resource):
    @namespace.response(200, "OK", model=[user_model])
    def get(self):
        '''Traer usuarios'''
        users = User.query.all()
        return [user.to_dict() for user in users]

    @namespace.expect(user_parser)
    @namespace.doc(security='protected')
    @namespace.response(200, "OK", model=simple_model)
    def post(self):
        '''Agregar nuevo usuario'''
        try:
            args = user_parser.parse_args()
            new_user = User(
                name= args["name"],
                username=args["username"],
                password=args["password"],
                amount=args["amount"])
            db.session.add(new_user)
            db.session.commit()
            return {"message":"se creó joya"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}

@namespace.response(401, "UNAUTHORIZED", model=simple_model)
@namespace.response(500, "SERVER ERROR", model=simple_model)
@namespace.route('/saldo')
class UserSaldoEndpoints(Resource):
    @namespace.response(200, "OK", model=[balance_model])
    @namespace.doc(security='protected')
    def get(self):
        '''Traer saldos'''
        try:
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException("Debe iniciar sesión", status_code=401)
            id_user = decode_auth_token(authorization)
            balances = Balance.query.filter_by(id_user=id_user).order_by(Balance.balance.desc())
            return [balance.to_dict() for balance in balances]
        except HTTPException as e:
            return e.response()
