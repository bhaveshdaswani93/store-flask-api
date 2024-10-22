import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import ItemSchema, ItemUpdateSchema
# from db import items, stores

blp = Blueprint('Items', __name__, description="Item Operation")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
  @blp.response(200, ItemSchema)
  def get(self, item_id):
    try:
     item = items[item_id]
     return item
    except KeyError:
     abort(404, message='item not found')

  def delete(self, item_id):
    try:
     del items[item_id]
     return {'message': 'Item deleted successfully'}
    except KeyError:
     abort(404, 'Item not found')
    
  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema)
  def put(self, req_body, item_id):
    #req_body = request.get_json()
    try:
      item = items[item_id]
      item |= req_body
    
      return item
    except KeyError:
      abort(404, message='item not found')
      
  @blp.route('/item')
  class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
      return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, req_body):
     # req_body = request.get_json()
  
      for item in items.values():
        if (item['name'] == req_body['name'] and item['store_id'] == req_body['store_id']):
          abort(400, message='Item already exists')
      
      store_id = req_body['store_id']

      if store_id not in stores.keys():
        abort(404, message='Store not found')

      item_id = uuid.uuid4().hex
      new_item = {**req_body, 'item_id': item_id, "id": item_id}
      items[item_id] = new_item
      return new_item, 201