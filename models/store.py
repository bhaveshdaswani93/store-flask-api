from db import db

class StoreModal(db.Model):
  __tablename__ = 'stores'
  
  id = db.Column(db.Integer, db.ForeignKey("stores.id"), primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
  