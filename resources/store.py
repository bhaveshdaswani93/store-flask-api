import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint('Stores', __name__, description='Operations on stores')

@blp.route('/store/<sting:store_id>')
class Store(MethodView):
  def get(self, store_id):
    try:
     return {'store': stores[store_id]}
    except KeyError:
     abort(404, message='Store not found')
  
  def delete(self, store_id):
    try:
      del stores[store_id]
      return {'message':'store deleted successfully'}
    except KeyError:
     abort(404, message='Store not found')

@blp.route('/store')
class StoreList(MethodView):
  def get(self):
    return {
      'stores': list(stores.values())
    }
  
  def post(self):
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


