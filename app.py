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
  store_id = uuid.uuid4().hex
  new_store = {**req_body, 'store_id': store_id }
  stores[store_id] = new_store
  return new_store, 201

@app.post('/item')
def create_item():
  req_body = request.get_json()
  store_id = req_body['store_id']

  if store_id not in stores.keys():
    return {'message': "store not found"}, 404

  item_id = uuid.uuid4().hex
  new_item = {**req_body, 'item_id': item_id}
  items[item_id] = new_item
  return new_item, 201

@app.get('/item')
def get_all_items():
  return {'items': list(items.values())}

@app.get('/store/<string:store_id>')
def get_store(store_id):
  try:
    return {'store': stores[store_id]}
  except KeyError:
    return {'message': 'Store not found'}, 404

@app.get('/item/<string:item_id>')
def get_item(item_id):
  try:
    item = items[item_id]
    return {'item': item}
  except KeyError:
    return {'message': 'item not found'}, 404
  