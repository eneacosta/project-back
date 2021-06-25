from operator import and_
from flask import request
from models.users import User
from models.operations import Deposit, Operations
from flask_restplus import Namespace, Resource, fields, reqparse
from models.operations import Operations
from models.coin import Balance, Coin
from models.shareddb import db
from utils import decode_auth_token, HTTPException
from .users import user_model
from .coin import coin_model

namespace = Namespace('operations', 'Endpoints de operaciones')

operation_model = namespace.model('Operation', {
    'id': fields.Integer,
    'user_from': fields.Nested(user_model),
    'user_to': fields.Nested(user_model),
    'coin': fields.Nested(coin_model),
    'amount': fields.Float,
})
simple_model = namespace.model('Simple message', {
    'message': fields.String,
})

money_req_parser = reqparse.RequestParser()
money_req_parser.add_argument('to', type=str, help='Username de usuario recibe la operacion', location='form', required=True)
money_req_parser.add_argument('amount', type=float, help='Cantidad de dinero', location='form', required=True)
money_req_parser.add_argument('coin', type=int, help='ID de la moneda', location='form', required=True)


@namespace.route('')
@namespace.response(401, "UNAUTHORIZED", model=simple_model)
@namespace.response(500, "SERVER ERROR", model=simple_model)
class OperationsEndpoints(Resource):
    @namespace.response(200, "OK", model=[operation_model])
    @namespace.doc(security='protected')
    def get(self):
        '''Trae operaciones del usuario logueado'''
        try:
            authorization = request.headers.get("Authorization")
            id_user_from = decode_auth_token(authorization)
            operations = Operations.query.filter((Operations.id_user_from == id_user_from) | (Operations.id_user_to == id_user_from))
            print(operations[0].to_dict())
            return [operation.to_dict() for operation in operations]
        except HTTPException as e:
            return e.response()

    @namespace.expect(money_req_parser)
    @namespace.doc(security='protected')
    def post(self):
        '''Envio de dinero'''
        try:
            args = money_req_parser.parse_args()
            token = request.headers.get("Authorization")
            id_user_from = decode_auth_token(token)
            user_to = args["to"]
            id_coin = args["coin"]
            db_user_to: User = User.query.filter_by(username=user_to).first()

            if not db_user_to:
                raise HTTPException(
                    "El usuario al que destina la operacion no existe :(",
                    status_code=404
                )

            amount = args["amount"]
            if amount <= 0:
                raise HTTPException(
                    "Debe enviar un monto mayor a 0",
                    status_code=400
                )
            operation = Operations(
                id_user_from,
                db_user_to.id,
                amount=amount,
                id_coin=id_coin
            )
            user_to_balance: Balance = Balance.query.filter(and_(Balance.id_user == db_user_to.id, Balance.id_coin == id_coin)).first()
            if not user_to_balance:
                #Primer deposito en esta moneda
                new_user_balance = Balance(id_user=db_user_to.id, id_coin=id_coin, balance=amount)
                db.session.add(new_user_balance)
            else:
                user_to_balance.balance += amount

            user_from_balance: Balance = Balance.query.filter(and_(Balance.id_user == id_user_from, Balance.id_coin == id_coin)).first()
            if (user_from_balance.balance - amount) < 0:
                raise HTTPException(f"No tiene suficiente saldo en {user_from_balance.coin.cod} para realizar esta operación")
            user_from_balance.balance -= amount

            db.session.add(operation)
            db.session.commit()

            return {
                'message': f'Envio de dinero correcto al usuario {db_user_to.username}'
            }
        except HTTPException as e:
            db.session.rollback()
            return e.response()
        except Exception as e:
            db.session.rollback()
            return HTTPException.unespected(str(e))


deposit_req_parser = reqparse.RequestParser()
deposit_req_parser.add_argument('amount', type=float, help='Cantidad de dinero', location='form', required=True)
deposit_req_parser.add_argument('coin', type=int, help='ID de la moneda', location='form', required=True)

@namespace.route('/deposit')
@namespace.response(401, "UNAUTHORIZED", model=simple_model)
@namespace.response(500, "SERVER ERROR", model=simple_model)
class DepositEndpoints(Resource):
    @namespace.response(200, "OK", model=[operation_model])
    @namespace.doc(security='protected')
    def get(self):
        '''Trae los depositos del usuario logueado'''
        try:
            authorization = request.headers.get("Authorization")
            id_user = decode_auth_token(authorization)

            deposits = Deposit.query.filter_by(id_user = id_user).all()
            return [deposit.to_dict() for deposit in deposits]
        except HTTPException as e:
            return e.response()



    @namespace.response(200, "OK", model=simple_model)
    @namespace.expect(deposit_req_parser)
    @namespace.doc(security='protected')
    def post(self):
        '''Realiza un nuevo deposito'''
        try:
            authorization = request.headers.get("Authorization")
            id_user = decode_auth_token(authorization)
            args = deposit_req_parser.parse_args()
            id_coin = args["coin"]
            amount = args["amount"]
            if amount <= 0:
                raise HTTPException("Debe depositar un monto mayor a 0.", status_code=400)
            coin = Coin.query.filter_by(id=id_coin).first()
            if not coin:
                raise HTTPException("ID de moneda invalido o inexistente.", status_code=404)
            deposit: Deposit = Deposit(id_user=id_user,id_coin=id_coin,amount=amount)
            user_balance: Balance = Balance.query.filter(and_(Balance.id_user == id_user, Balance.id_coin == id_coin)).first()
            if not user_balance:
                #Primer deposito en esta moneda
                new_user_balance = Balance(id_user=id_user, id_coin=id_coin, balance=amount)
                db.session.add(new_user_balance)
            else:
                user_balance.balance += amount
            
            db.session.add(deposit)
            
            db.session.commit()
            return {"message":f"Deposito de {deposit.amount} {deposit.coin.cod} realizado con éxito"}
        except HTTPException as e:
            db.session.rollback()
            return e.response()
        except Exception as e:
            db.session.rollback()
            return HTTPException.unespected(str(e))