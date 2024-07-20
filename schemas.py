from marshmallow import Schema, fields


# {
# 	"id": "0d8574cca8214577998375a3496743ab",
# 	"store_name": "ikea"
# }
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    store_name = fields.Str(required=True)


# {
# 	"id": "50a6f60aea5a4a04ae8d783d31e0ea43",
# 	"name": "chair",
# 	"price": 12.99,
# 	"store_id": "f3a3c3b478b14e8eb4efda52af0b0ade"
# }
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


# optional data
# {
# 	"name": "chair",
# 	"price": 12.99,
# }
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
