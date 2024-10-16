import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint('Items', __name__, description="Item Operation")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
  def get(self, item_id):
    pass

  def delete(self, item_id):
    pass

  def put(self, item_id):
    pass