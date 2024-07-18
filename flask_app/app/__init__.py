import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.ekiqftvfqjfcfvfbdfkq:tomandjerryare24@aws-0-eu-west-1.pooler.supabase.com:5432/postgres'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    # Session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'scrabble_'
    app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    Session(app)
    CORS(app)

    from .auth_route import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .game_route import game_blueprint
    app.register_blueprint(game_blueprint)

    return app