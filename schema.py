from marshmallow import Schema, fields

class PlainItemSchema(Schema):
  id = fields.Str(dump_only=True)
  name = fields.Str(required=True)
  price = fields.Float(required=True)
 # store_id = fields.Str(required=True)

class PlainStoreSchema(Schema):
  id = fields.Str(dump_only=True)
  name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
  name = fields.Str()
  price = fields.Float()

class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required=True, load_only=True)

# class StoreSchema(Schema):
#   id = fields.Str(dump_only=True)
#   name = fields.Str(required=True)
