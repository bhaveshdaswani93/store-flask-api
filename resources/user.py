from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schema import UserSchema

blp = Blueprint('Users', 'users', description="Operations on user")

@blp.route('/register')
class UserRegister(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
    if UserModel.query.filter(UserModel.username == user_data['username']).first():
      abort(400, message=f'User with username {user_data['username']} already exists')
    
    user = UserModel(
        username = uaer_data['username'],
        password = pbkdf2_sha256.hash(user_data['password'])
      )
      
      db.session.add(user)
      db.session.commit()
      
      return {'message': 'User created successfully'}, 201
    

