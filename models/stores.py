from db import db


# {
#     "id": 1,
#     "store_name": "ikea"
#     "items": [
#         {
#             "id": 1,
#             "name": "chair",
#             "price": 12.99
#         }
#     ],
#     "tags": [
#         {
#             "id": 1,
#             "name": "furniture",
#         }
#     ],

# }


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel",
        back_populates="store",  # store from the ItemModel
        lazy="dynamic",
        # passive_deletes="all",    # deletes the store and marks all associated items with the store_id as null
        cascade="all",  # recursively deletes all items in the store
    )
    tags = db.relationship(
        "TagModel",
        back_populates="store",  # store from the ItemModel
        lazy="dynamic",
        cascade="all",  # recursively deletes all items in the store
    )
