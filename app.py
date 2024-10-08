from flask import Flask

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