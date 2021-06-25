
from .shareddb import db
from .users import User

class Coin(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    cod = db.Column(db.String(6))

    def __init__(self, name:str, cod):
        self.name = name
        self.cod = cod

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cod': self.cod,
        }
    
class Balance(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, foreign_keys=[id_user])
    id_coin = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)
    coin = db.relationship(Coin, foreign_keys=[id_coin])
    balance = db.Column(db.Float)
    table_pk = db.PrimaryKeyConstraint(id_user, id_coin)

    def __init__(self, id_user:int, id_coin:int, balance:float) -> None:
        self.id_user = id_user
        self.id_coin = id_coin
        self.balance = balance
        
    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'coin': self.coin.to_dict(),
            'balance': self.balance,
        }