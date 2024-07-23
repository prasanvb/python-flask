from flask import Flask
from flask_smorest import Api
from resources.stores import stores_blp
from resources.items import items_blp
from resources.tags import tags_blp
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
import os


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Flask_Smorest REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(stores_blp)
    api.register_blueprint(items_blp)
    api.register_blueprint(tags_blp)

    return app


# GET:http://127.0.0.1:3000/
# @app.get("/")
# def main():
#     return "Python flask project", 200
