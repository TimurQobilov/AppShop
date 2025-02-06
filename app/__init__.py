from flask import Flask
from config import Config
from app.models import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Инициализация Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрация маршрутов
    from app.routes import main_routes
    from app.auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    with app.app_context():
        db.create_all()  # Создаем таблицы в базе данных

    return app