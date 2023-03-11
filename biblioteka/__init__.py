from flask import Flask
from os import environ

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ['COOKIES_KEY']
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app