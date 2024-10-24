from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.store import StoreModel
from db import db
from schema import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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
    store = StoreModel(**req_body)

    try:
      db.session.add(store)
      db.session.commit()
    except IntegrityError:
      abort(400, message="Store with that name already exists")
    except SQLAlchemyError:
      abort(500, message="Something Went wrong while saving store info")


    # store_id = uuid.uuid4().hex
    # new_store = {**req_body, 'id': store_id, 'store_id': store_id }
    # stores[store_id] = new_store
    return store


