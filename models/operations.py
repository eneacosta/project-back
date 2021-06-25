from .shareddb import db
from enum import Enum
from .users import User
from .coin import Coin

class Operations(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    id_user_from = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_from = db.relationship(User, foreign_keys=[id_user_from])
    id_user_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_to = db.relationship(User, foreign_keys=[id_user_to])
    id_coin = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)
    coin = db.relationship(Coin, foreign_keys=[id_coin])
    amount = db.Column(db.Float)

    def __init__(self, user_from:str, user_to:str, amount:float, id_coin:int):
        self.id_user_from = user_from
        self.id_user_to = user_to
        self.amount = amount
        self.id_coin = id_coin

    def to_dict(self):
        return {
            'id': self.id,
            'user_from': self.user_from.to_dict(),
            'user_to': self.user_to.to_dict(),
            'coin': self.coin.to_dict(),
            'amount': self.amount,
        }

class Deposit(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, foreign_keys=[id_user])
    id_coin = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)
    coin = db.relationship(Coin, foreign_keys=[id_coin])
    amount = db.Column(db.Float)

    def __init__(self, id_user:str, amount:float, id_coin:int):
        self.type = type
        self.id_user = id_user
        self.amount = amount
        self.id_coin = id_coin

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'coin': self.coin.to_dict(),
            'amount': self.amount,
        }
    
