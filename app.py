from flask import Flask, request
import uuid

app = Flask(__name__)

stores = {}
items = {}

@app.get("/store") # http://127.0.0.1:5000/store
def get_stores(): 
    return {"stores": list(stores.values())}  

@app.post("/store")
def create_store(): 
    store_data = request.get_json()
    store_id = uuid.uuid4().hex 
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item(): 
    item_data = request.get_json()
    if item_data["store_id"] not in stores: 
        return {"message": "Store not found"}, 404 
    
    item_id = uuid.uuid4().hex 
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())} 

@app.post("/store/<string:name>")
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores.values(): 
        if store["name"] == name: 
            new_item = {"name": request_data["name"], "price": request_data["price"]} 
            store["items"].append(new_item) 
            return new_item, 201 
    return {"message": "Store not found"}, 404

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError: 
        return {"message": "Store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores.values(): 
        if store["name"] == name:
            return {"items": store.get("items", [])} 
    return {"message": "Store not found"}, 404 
