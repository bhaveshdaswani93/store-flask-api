from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.store import StoreModel
from db import db
from schema import StoreSchema, StoreUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint('Stores', __name__, description='Operations on stores')

@blp.route('/store/<int:store_id>')
class Store(MethodView):
  @blp.response(200, StoreSchema)
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store
  
  def delete(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    
    db.session.delete(store)
    db.session.commit()
    return {'message': 'store deleted successfully'}
    #NotImplementedError("Implementation pending for Delete store")
  
  @blp.arguments(StoreUpdateSchema)
  @blp.response(200, StoreSchema)
  def put(self, store_data, store_id):
    print(store_data)
    store = StoreModel.query.get(store_id)
    
    if store:
      store.name = store_data['name']
    else:
      store = StoreModel(id=store_id, **store_data)

    db.session.add(store)
    db.session.commit()

    return store

@blp.route('/store')
class StoreList(MethodView):
  @blp.response(200, StoreSchema(many=True))
  def get(self):
    return StoreModel.query.all()
  
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


