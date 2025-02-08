from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
UPLOAD_FOLDER = 'static/uploads'

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)


    from app.models import User, Product

    with app.app_context():
        db.create_all()


    from app.routes import register_routes
    register_routes(app)

    return app
