from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ Создаём объект базы данных, но не импортируем маршруты сразу

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)

    # ✅ Импортируем модели перед созданием таблиц
    from app.models import User, Product  

    with app.app_context():
        db.create_all()

    # ✅ Импортируем маршруты ТОЛЬКО ПОСЛЕ `db.init_app(app)`
    from app.routes import register_routes
    register_routes(app)

    return app
