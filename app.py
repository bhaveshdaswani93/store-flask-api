import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from db import db
import models

print(__name__)
"""
stores = [{
  'name': 'My Wonderful Store',
  'items': [{
    'name': 'My Item',
    'price': 15.99
  }]
}]
"""

def create_app(db_url=None):

  app = Flask(__name__)



  app.config['POPULATE_EXCEPTIONS'] = True
  app.config['API_TITLE'] = 'Stores Rest Api'
  app.config['API_VERSION'] = 'v1'
  app.config['OPENAPI_VERSION'] = '3.0.3'
  app.config['OPENAPI_URL_PREFIX'] = '/'
  app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
  app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URI', 'sqlite:///data.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  db.init_app(app)
  api = Api(app)
  
  app.config['JWT_SECRET_KEY'] = '243298653354856329497319100674191169490'
  
  jwt = JWTManager(app)

  with app.app_context():
    db.create_all()

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  api.register_blueprint(TagBluePrint)
  
  return app


