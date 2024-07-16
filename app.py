from flask_smorest import abort
from flask import Flask, request
import uuid
from db import stores, items

app = Flask(__name__)


# GET:http://127.0.0.1:5000/
@app.get("/")
def main():
    return "Python flask project", 200


# POST: http://127.0.0.1:5000/store
# {
# 	"store_name": "ikea"
# }
@app.post("/store")
def create_store():
    request_json = request.get_json()

    if ("store_name" not in request_json):
        abort(400, message="store_name data missing")

    for store in stores.values():
        if store["store_name"] == request_json["store_name"]:
            abort(400, message="Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**request_json, "id": store_id}
    stores[store_id] = store
    return store, 200


# GET:http://127.0.0.1:5000/stores
@app.get("/stores")
def get_stores():
    return {"stores": stores}, 200


# POST: http://127.0.0.1:5000/item
# {
# 	"store_id": "e00b46de7ff947a194ad7dd169e5b123",
# 	"name": "chair",
# 	"price": 12.99
# }
@app.post("/item")
def create_item():
    item_data = request.get_json()
    store_id, name, price = item_data.values()

    if ("store_id" not in item_data or
            "price" not in item_data or
            "name" not in item_data):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")

    for item in items.values():
        if (item["name"] == name and
                item["store_id"] == store_id):
            abort(404, message=f"Item {name} already exists")

    if store_id not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item


# GET:http://127.0.0.1:5000/items
@app.get("/items")
def get_items():
    return {"items": list(items.values())}, 200


# GET:http://127.0.0.1:5000/store/e00b46de7ff947a194ad7dd169e5b123
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


# GET:http://127.0.0.1:5000/item/e00b46de7ff947a194ad7dd169e5b123
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found")


# DELETE: http://127.0.0.1:5000/item/e00b46de7ff947a194ad7dd169e5b123
@app.delete("/item/<string:item_id>")
def delete_item_by_id(item_id):
    try:
        print(items[item_id])
        del items[item_id]
        return {"message": "Item deleted successfully"}, 200
    except KeyError:
        abort(404, message="Item not found.")


# PUT: http: // 127.0.0.1: 5000/item/e00b46de7ff947a194ad7dd169e5b123
@app.put("/item/<string:item_id>")
def update_item_by_id(item_id):
    data = request.get_json()

    if ("name" not in data or "price" not in data):
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )

    try:
        item = items[item_id]
        item |= data

        return item
    except KeyError:
        abort(404, message="Item not found.")
