from db import db


# {
# 	"id": 1,
# 	"name": "furniture",
#   "store": {
# 	    "id": 1,
# 	    "store_name": "ikea"
#   }
# }
class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship(
        "StoreModel", back_populates="tags"
    )  # store from the StoreModel
