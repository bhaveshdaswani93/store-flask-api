from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schema import UserSchema

blp = Blueprint('Users', 'users', description="Operations on user")

