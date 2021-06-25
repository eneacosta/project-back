from models import coin
from models.coin import Balance
from models.shareddb import db
from models import User, Operations, Coin
from sqlalchemy.exc import IntegrityError 

users = (
    User(name='Nicolas Acosta', username='nacosta', password=1234, id=1),
    User(name='Franco Corvalan', username='fcorvalan', password=1234, id=2),
    User(name='Federico Diaz', username='fdiaz', password=1234, id=3),
    User(name='Administrador', username='admin', password=1234, id=4),
)
coins = [
    Coin("Dolar Estadounidense","USD"),
    Coin("Bitcoin", "BTC"),
    Coin("Peso Argentino", "ARS"),
]
balances = [
    Balance(1, 1, 100),
    Balance(1, 2, 0.5),
    Balance(1, 3, 1500),
    Balance(2, 1, 200),
    Balance(2, 2, 1.5),
    Balance(2, 3, 3000),
]
operations = (
    Operations(user_from=1, user_to=2, amount=20, id_coin=1),
    Operations(user_from=2, user_to=1, amount=15, id_coin=2),
)

def seed_db(app):
    try:
        with app.app_context():
            
            [db.session.add(user) for user in users]
            [db.session.add(coin) for coin in coins]
            [db.session.add(balance) for balance in balances]
            [db.session.add(operation) for operation in operations]
            db.session.commit()
            print("Migracion exitosa")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Los datos ya han sido migrados {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {str(e)}")
