from db import db

class ItemModel(db.Model):
  __tablename__ = "items"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Columb(db.String(80), unique=True, nullable=False)
  price = db.Column(db.float(precision= 2), unique=False, nullable=False)
  store_id = db.Column(db.Integer, unique=False, nullable=False)
  store = db.relationship("StoreModel", back_populates="items")