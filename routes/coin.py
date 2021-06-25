from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from models.coin import Coin
from models.shareddb import db

namespace = Namespace('coin', 'Endpoints de moneda')


coin_model = namespace.model('Coin', {
    'id': fields.Integer,
    'name': fields.String,
    'cod': fields.String,
})

coin_parser = reqparse.RequestParser()
coin_parser.add_argument('name', type=str, required=True, help='Nombre de la moneda', location='form')
coin_parser.add_argument('cod', type=str, required=True, help='Código ed la moneda', location='form')




@namespace.route('')
class CoinEndpoints(Resource):
    @namespace.marshal_list_with(coin_model)
    def get(self):
        '''Traer monedas'''
        coins = Coin.query.all()
        return [coin.to_dict() for coin in coins]

    @namespace.expect(coin_parser)
    @namespace.doc(security='protected')
    def post(self):
        '''Agregar nueva moneda'''
        try:
            args = coin_parser.parse_args()
            new_coin = Coin(
                name= args["name"],
                cod=args["cod"],
                )
            db.session.add(new_coin)
            db.session.commit()
            return {"message":"se creo joya"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}