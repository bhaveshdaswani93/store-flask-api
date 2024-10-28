from db import db

class TagModel(db.model):
  __tablename__ = 'tags'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False, unique=True)
  store_id = db.Column(db.Integer, db.Forigien('store_id'), nullable=False)
  store = db.relationship('StoreModel', back_populates='tags')
  
  