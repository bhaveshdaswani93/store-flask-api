from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores
from schema import StoreSchema

blp = Blueprint('Stores', __name__, description='Operations on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
  @blp.response(200, StoreSchema)
  def get(self, store_id):
    try:
     return stores[store_id]
    except KeyError:
     abort(404, message='Store not found')
  
  def delete(self, store_id):
    try:
      del stores[store_id]
      return {'message':'store deleted successfully'}
    except KeyError:
     abort(404, message='Store not found')
  
  @blp.response(200, StoreSchema)
  def put(self, store_id):
    try:
      req_body = request.get_json()
      store = stores[store_id]
      store |= req_body
      return store
    except KeyError:
      abort(404, message="Store not found")

@blp.route('/store')
class StoreList(MethodView):
  @blp.response(200, StoreSchema(many=True))
  def get(self):
    return stores.values()
  
  @blp.arguments(StoreSchema)
  @blp.response(201, StoreSchema)
  def post(self, req_body):
    #req_body = request.get_json()

    for store in stores.values():
      if (store['name'] == req_body['name']):
        abort(400, message='Store name already exists')

    store_id = uuid.uuid4().hex
    new_store = {**req_body, 'id': store_id, 'store_id': store_id }
    stores[store_id] = new_store
    return new_store


