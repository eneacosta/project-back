from .shareddb import db
from .operations import Operations
from .users import User
from .coin import Coin

def init_app(app):
    db.init_app(app)
