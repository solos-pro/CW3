from flask import Flask
from app.config import Config
from flask_restx import Api
from app.database import db

from app.views.genre import genre_ns
from app.views.director import director_ns
from app.views.movies import movie_ns
from app.views.auth import auth_ns
from app.views.users import user_ns


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


app_config = Config()
app = create_app(app_config)
configure_app(app)


# if __name__ == '__main__':
#
#     app_config = Config()
#     app = create_app(app_config)
#     configure_app(app)
#     app.run()











