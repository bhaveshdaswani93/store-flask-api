from flask import Flask, request
from db import stores, items
import uuid

print(__name__)

app = Flask(__name__)

"""
stores = [{
  'name': 'My Wonderful Store',
  'items': [{
    'name': 'My Item',
    'price': 15.99
  }]
}]
"""

@app.get('/store')
def get_stores():
  return {
    'stores': list(stores.values())
  }

@app.post('/store')
def create_store():
  req_body = request.get_json()
  store_id = uuid.uuidv4().hex
  new_store = {**req_body, 'store_id': store_id }
  stores[store_id] = new_store
  return new_store, 201

@app.post('/store/<string:name>/item')
def create_item_in_store(name):
  req_body = request.get_json()
  for store in stores:
    if store['name'] == name:
      new_item = {'name': req_body['name'], 'price': req_body['price']}
      store['items'].append(new_item)
      return new_item, 201
  return "Store not found", 404
  
  @app.get('/store/<string:store_id>')
  def get_store(store_id):
    try:
      return {'store': stores[store_id]}
    except KeyError:
      return {'message': 'Store not found'}, 404
  
  @app.get('/store/<string:name>/items')
  def get_items_in_store(name):
    for store in stores:
      if store['name'] == name:
        return {'items': store['items']}
    return {'message': 'store not found'}, 404
  