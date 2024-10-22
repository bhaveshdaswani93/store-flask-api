import os
from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from db import db
import models

print(__name__)

def create_app(db_url=None):

  app = Flask(__name__)

"""
stores = [{
  'name': 'My Wonderful Store',
  'items': [{
    'name': 'My Item',
    'price': 15.99
  }]
}]
"""

  app.config['POPULATE_EXCEPTIONS'] = True
  app.config['API_TITLE'] = 'Stores Rest Api'
  app.config['API_VERSION'] = 'v1'
  app.config['OPENAPI_VERSION'] = '3.0.3'
  app.config['OPENAPI_URL_PREFIX'] = '/'
  app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
  app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URI', 'sqllite:///data.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  db.init_app(app)
  

  api = Api(app)

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  
  return app


