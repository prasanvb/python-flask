import uuid
from flask import request
from db import stores
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema

# MethodView: Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
# blueprint: Decorators to specify Marshmallow schema for view functions I/O and API documentation registration

stores_blp = Blueprint("stores", __name__, description="operations on stores")


@stores_blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores["store_id"]
            return {"message": "Store deleted successfully"}, 200
        except KeyError:
            abort(404, message="Store not found.")


@stores_blp.route("/stores")
class Stores(MethodView):
    def get(self):
        return {"stores": stores}, 200


@stores_blp.route("/store")
class Create_Store(MethodView):

    @stores_blp.arguments(StoreSchema)
    def post(self, store_data):
        # store_data is returned in json formate after all the validation performed by StoreSchema on `request.get_json()`

        if "store_name" not in store_data:
            abort(400, message="store_name data missing")

        for store in stores.values():
            if store["store_name"] == store_data["store_name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 200
