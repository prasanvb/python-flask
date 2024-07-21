from db import db


# {
# 	"id": 1,
# 	"store_name": "ikea",
#   "items": []
# }
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic"
    )  # store from the ItemModel
