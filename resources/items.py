import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.items import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

# MethodView: Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
# blueprint: Decorators to specify Marshmallow schema for view functions I/O and API documentation registration

items_blp = Blueprint("items", __name__, description="operations on items")


@items_blp.route("/item")
class CreateItem(MethodView):

    @items_blp.arguments(ItemSchema)
    @items_blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error while inserting")

        return item


@items_blp.route("/items")
class Items(MethodView):

    @items_blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


@items_blp.route("/item/<string:item_id>")
class Item(MethodView):

    @items_blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted successfully"}, 200

    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data is returned in json formate after all the validation performed by ItemSchema on `request.get_json()`
        item = ItemModel.query.get(item_id)

        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error while inserting")

        return item
