import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint('Stores', __name__, description='Operations on stores')

@blp.route('/store/<sting:store_id>')
class Store(MethodView):
  def get(self):
    pass
  
  def delete(self):
    pass

