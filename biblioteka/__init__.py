from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .search import search

db = SQLAlchemy()
db_name = 'database.db'



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'awefioaonwralgalgk12i' #?????

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all()

    from .models import biblioteka, kategorie
    with app.app_context():
        db.create_all()

    return app