import uuid
from flask import request
from db import items, stores
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

# MethodView: Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
# blueprint: Decorators to specify Marshmallow schema for view functions I/O and API documentation registration

items_blp = Blueprint("items", __name__, description="operations on items")


@items_blp.route("/item")
class CreateItem(MethodView):

    @items_blp.arguments(ItemSchema)
    @items_blp.response(200, ItemSchema)
    def post(self, item_data):
        # item_data is returned in json formate after all the validation performed by ItemSchema on `request.get_json()`
        name, price, store_id = item_data.values()

        for item in items.values():
            if item["name"] == name and item["store_id"] == store_id:
                abort(404, message=f"Item {name} already exists")

        if store_id not in stores:
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item


@items_blp.route("/items")
class Items(MethodView):

    @items_blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()


@items_blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted successfully"}, 200
        except KeyError:
            abort(404, message="Item not found.")

    @items_blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        # item_data is returned in json formate after all the validation performed by ItemSchema on `request.get_json()`

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")
