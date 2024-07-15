from flask import Flask, request
from db import stores, items
app = Flask(__name__)

stores = [{"name": "ikea", "items": [{"name": "lamp", "price": 15.99}]}]


@app.get("/stores")  # GET:http://127.0.0.1:5000/stores
def get_stores():


@app.get("/")  # GET:http://127.0.0.1:5000/
def main():
    return "Python flask project", 200

    return {"stores": stores}, 200


# POST:http://127.0.0.1:5000/store # body:{"store":"home depot"}
@app.post("/store")
def create_store():
    request_json_data = request.get_json()
    print({"type": type(request_json_data).__name__, "data": request_json_data})
    new_store = {"name": request_json_data["store"], "items": []}
    stores.append(new_store)
    return stores, 201


@app.post(
    "/store/<string:name>/item"
)  # POST:http://127.0.0.1:5000/store/ikea/item  # body:{'item': 'table', 'price': 72.0}}
def create_store_item(name):
    request_json_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            store["items"].append(request_json_data)
            return store, 201
    return {"error_message": "store not found"}, 404


# GET: http://127.0.0.1:5000/store/ikea/items
@app.get("/store/<string:name>/items")
def get_store_items(name):
    for store in stores:
        store["name"] == name
        return store["items"], 200
    return {"error_message": "store not found"}, 404
