from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.users import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


users_blp = Blueprint("users", __name__, description="operations on users")


@users_blp.route("/register")
class RegisterUser(MethodView):

    @users_blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)

        print(user_data)

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


# @users_blp.route("/user/<string:user_id>")
# class ManipulateUser(MethodView):

#     def delete(self, user_id):
#         pass
