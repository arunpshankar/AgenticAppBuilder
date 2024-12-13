from app.database import db, init_db
from src.app.config import Config
from flask_cors import CORS
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    with app.app_context():
        init_db()

    from src.app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
