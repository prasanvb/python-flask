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


@users_blp.route("/user/login")
class LoginUser(MethodView):

    @users_blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
