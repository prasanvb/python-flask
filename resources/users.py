from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.users import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

users_blp = Blueprint("users", __name__, description="operations on users")


@users_blp.route("/user/register")
class RegisterUser(MethodView):

    @users_blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="username already exists")
        except SQLAlchemyError:
            abort(500, message="error while creating the user data")

        return {"message": "User created successfully."}, 201


@users_blp.route("/users")
class Users(MethodView):

    @users_blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@users_blp.route("/user/<string:user_id>")
class ManipulateUser(MethodView):

    @users_blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": f"user_id {user_id} deleted successfully"}, 200


# HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
# jwt signing we need "algorithm", "payload" and "secret"
# create_access_token
# HEADER
# {
#   "alg": "HS256",
#   "typ": "JWT"
# }
# PAYLOAD
# {
#   "fresh": false,
#   "iat": 1721799720,
#   "jti": "f8cdc3fa-d440-45c1-af88-70549eb6909f",
#   "type": "access",
#   "sub": "prasan",
#   "nbf": 1721799720,
#   "csrf": "2a8e3e33-dc0d-4054-896c-90577fe3713f",
#   "exp": 1721800620
# }

@users_blp.route("/user/login")
class LoginUser(MethodView):

    @users_blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # create_access_token takes care of jwt signing
            # identity value is used as sub within payload
            access_token = create_access_token(identity=user.username)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
