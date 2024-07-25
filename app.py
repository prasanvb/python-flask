import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.root import root_blp
from resources.stores import stores_blp
from resources.items import items_blp
from resources.tags import tags_blp
from resources.users import users_blp
from db import db


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
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRETS", "jose")

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_required, jwt_payload):
        return (jsonify({
                "message": "The token has expired.",
                "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({
                "message": "Signature verification failed.",
                "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return (jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
                }), 401)

    @jwt.additional_claims_loader
    def additional_claims_callback(identity):
        if identity == "prasan":
            return {"is_admin": True}
        else:
            return {"is_admin": False}

    db.init_app(app)

    api = Api(app)

    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(root_blp)
    api.register_blueprint(stores_blp)
    api.register_blueprint(items_blp)
    api.register_blueprint(tags_blp)
    api.register_blueprint(users_blp)

    return app


# GET:http://127.0.0.1:3000/
# @app.get("/")
# def main():
#     return "Python flask project", 200
