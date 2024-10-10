from flask import Flask, request

print(__name__)

app = Flask(__name__)

stores = [{
  'name': 'My Wonderful Store',
  'items': [{
    'name': 'My Item',
    'price': 15.99
  }]
}]

@app.get('/store')
def get_stores():
  return {
    'stores': stores
  }

@app.post('/store')
def create_store():
  req_body = request.get_json()
  new_store = {'name': req_body['name'], 'items': [] }
  stores.append(new_store)
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
  
@app.get('/store/<string:name>')
def get_store(name):
  for store in stores:
    if store['name'] == name:
      return {'store': store}
  return {'message': 'Store not found'}, 404

@app.get('/store/<string:name>/items')
def get_items_in_store(name):
  for store in stores:
    if store['name'] == name:
      return {'items': store['items']}
  return {'message': 'store not found'}, 404
  