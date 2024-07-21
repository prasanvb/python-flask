from marshmallow import Schema, fields


# {
# 	"id": 1,
# 	"store_name": "ikea"
# }
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)


# {
# 	"id": 1,
# 	"name": "chair",
# 	"price": 12.99,
# 	"store_id": "f3a3c3b478b14e8eb4efda52af0b0ade"
# }
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


# optional data
# {
# 	"name": "chair",
# 	"price": 12.99,
# }
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
