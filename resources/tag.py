from email import message
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schema import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Blueprint for tags")

@blp.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
  @blp.response(200, TagSchema(many=True))
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    
    return store.tags.all()

  @blp.arguments(TagSchema)
  @blp.response(201, TagSchema)
  def post(self, tag_data, store_id):
    if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
      abort(400, message='Tag with this name already exists')
    tag = TagModel(**tag_data)

    try:
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))
      
    return tag
    
@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
  @blp.response(200, TagSchema)
  def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag
  
  @blp.response(202, description='Deletes a tag if not item is attached to it', example={'message': 'Tag deleted'})
  @blp.alt_response(404, description='Tag not found')
  @blp.response(400, description='when tag is assigned item')
  def delete(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    
    if not tag.items:
      db.session.delete(tag)
      db.session.commit()
      return {'message': 'tag deleted successfully'}
    
    abort(400, message='tag is associated with item, please disassociate them first, then try again')

@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagToItem(MethodView):
  
  @blp.response(201, TagSchema)
  def post(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)

    if item.store_id != tag.store_id:
      abort(400, message="cannot link item, tag from different store")

    item.tags.append(tag)

    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))
    
    return tag

  @blp.response(200, TagAndItemSchema)
  def delete(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)

    item.tags.remove(tag)

    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return {'message': 'Tag removed from item', 'item': item, 'tag': tag}
