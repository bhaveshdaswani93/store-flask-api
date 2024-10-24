from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from schema import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('Items', __name__, description="Item Operation")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
  @blp.response(200, ItemSchema)
  def get(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item

  def delete(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    raise NotImplementedError('Implenting of delete item is pending')
    
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
      item = ItemModel(**req_body)

      try:
        db.session.add(item)
        db.session.commit()
      except SQLAlchemyError:
        abort(500, message="an error occurred while inserting the item")

      return item
    