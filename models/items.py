from db import db


# {
# 	"id": 1,
# 	"name": "chair",
# 	"price": 12.99,
# 	"store_id": "f3a3c3b478b14e8eb4efda52af0b0ade"
#   "store": []
# }
class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship(
        "StoreModel", back_populates="items"
    )  # items from the StoreModel
