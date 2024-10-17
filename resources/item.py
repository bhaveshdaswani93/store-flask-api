import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint('Items', __name__, description="Item Operation")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
  def get(self, item_id):
    try:
     item = items[item_id]
     return {'item': item}
    except KeyError:
     abort(404, message='item not found')

  def delete(self, item_id):
    try:
     del items[item_id]
     return {'message': 'Item deleted successfully'}
    except KeyError:
     abort(404, 'Item not found')
    

  def put(self, item_id):
    req_body = request.get_json()
    if ('name' not in req_body or 'price' not in req_body):
      abort(400, message='price, name is required')
    try:
      item = items[item_id]
      item |= req_body
    
      return {'item': item}
    except KeyError:
      abort(404, message='item not found')
      
  class ItemList(MethodView):
    def get(self):
      return {'items': list(items.values())}
    
    def post(self):
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