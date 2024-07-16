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
    store_id = uuid.uuid4().hex
    store = {**request_json, "id": store_id}
    stores[store_id] = store
    return store, 200


# GET:http://127.0.0.1:5000/stores
@app.get("/stores")
def get_stores():
    return list(stores.values()), 200

# POST: http://127.0.0.1:5000/item
# {
# 	"store_id": "e00b46de7ff947a194ad7dd169e5b123",
# 	"name": "chair",
# 	"price": 12.99
# }


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item
