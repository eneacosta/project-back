# main.py
from flask import Flask
from routes import blueprint as endpoints
from flask_cors import CORS
from seeds import seed_db
import os


def init_app():    
    app = Flask(__name__)
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.sqlite3"
    app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from models import init_app
    from models.shareddb import db
    init_app(app)
    with app.app_context():
        db.create_all()
        seed_db(app)
        app.register_blueprint(endpoints, url_prefix=os.environ.get("ROOT_PATH", ""))
        return app

app = init_app()


CORS(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)