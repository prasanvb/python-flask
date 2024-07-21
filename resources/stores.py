from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.stores import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# MethodView: Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
# blueprint: Decorators to specify Marshmallow schema for view functions I/O and API documentation registration

stores_blp = Blueprint("stores", __name__, description="operations on stores")


@stores_blp.route("/store")
class Create_Store(MethodView):

    @stores_blp.arguments(StoreSchema)
    @stores_blp.response(200, StoreSchema)
    def post(self, store_data):
        # store_data is returned in json formate after all the validation performed by StoreSchema on `request.get_json()`
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="store name already exists")
        except SQLAlchemyError:
            abort(500, message="error while creating the store")

        return store


@stores_blp.route("/stores")
class Stores(MethodView):

    @stores_blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@stores_blp.route("/store/<string:store_id>")
class Store(MethodView):

    @stores_blp.response(200, StoreSchema)
    def get(self, store_id):
        stores = StoreModel.query.get_or_404(store_id)
        return stores

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted successfully"}, 200
