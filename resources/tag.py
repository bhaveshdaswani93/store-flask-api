from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schema import TagSchema

blp = Blueprint("Tags", "tags", description="Blueprint for tags")

@blp.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
  def get(self, store_id):
    pass

  @blp.arguments(TagSchema)
  @blp.response(201, TagSchema)
  def post(self, tag_data, store_id):
    pass
