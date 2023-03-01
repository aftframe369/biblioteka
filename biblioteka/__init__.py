from flask import Flask
from .search import search

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'awefioaonwralgalgk12i' #?????
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app