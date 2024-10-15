from email import message
from flask import Flask, request
from db import stores, items
import uuid
from flask_smorest import abort

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
  if ('name' not in req_body):
    abort(400, message="Name is required")

  for store in stores.values():
    if (store['name'] == req_body['name']):
      abort(400, message='Store name already exists')

  store_id = uuid.uuid4().hex
  new_store = {**req_body, 'store_id': store_id }
  stores[store_id] = new_store
  return new_store, 201

@app.post('/item')
def create_item():
  req_body = request.get_json()
  if ('price' not in req_body
    or 'store_id' not in req_body
    or 'name' not in req_body):
      abort(400, message='price, store_id, name is required')
  
  for item in items.values():
    if (item['name'] == req_body['name'] and item['store_id'] == req_body['store_id']):
      abort(400, message='Item already exists')
  
  store_id = req_body['store_id']

  if store_id not in stores.keys():
    abort(404, message='Store not found')

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
    abort(404, message='Store not found')

@app.get('/item/<string:item_id>')
def get_item(item_id):
  try:
    item = items[item_id]
    return {'item': item}
  except KeyError:
    abort(404, message='item not found')

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
  try:
    del items[item_id]
    return {'message': 'Item deleted successfully'}
  except KeyError:
    abort(404, 'Item not found')
    
@app.put('/item/<string:item_id>')
def update_item(item_id):
  req_body = request.get_json()
  if ('name' not in req_body or 'price' not in req_body):
    abort(400, message='price, name is required')
  try:
    item = items[item_id]
    item |= req_body
    
    return {'item': item}
  except KeyError:
    abort(404, message='item not found')
    
@app.delete('/store/<string:store_id>')
def delete_store(store_id):
  try:
    del stores[store_id]
    return {'message':'store deleted successfully'}
  except KeyError:
    abort(404, message='Store not found')
  