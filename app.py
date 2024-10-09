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
  new_store = {'name': req_body['name'], items: [] }
  stores.append(new_store)
  return new_store, 201