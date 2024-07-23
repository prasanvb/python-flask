from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.tags import TagModel
from models.stores import StoreModel
from models.items import ItemModel
from schemas import TagSchema, CreateTagSchema, TagAndItemSchema
from sqlalchemy.exc import SQLAlchemyError

# MethodView: Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
# blueprint: Decorators to specify Marshmallow schema for view functions I/O and API documentation registration

tags_blp = Blueprint("tags", __name__, description="operations on tags")


@tags_blp.route("/tag")
class create_tag(MethodView):

    @tags_blp.arguments(CreateTagSchema)
    @tags_blp.response(200, CreateTagSchema)
    def post(self, tag_data):
        if TagModel.query.filter(TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with same name already exists")

        tag = TagModel(**tag_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@tags_blp.route("/tags")
class Items(MethodView):

    @tags_blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()


@tags_blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @tags_blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    # def delete(self):
    #     return 200, "delete ItemTags"


@tags_blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):

    @tags_blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @tags_blp.arguments(TagSchema)
    @tags_blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(400, message="A tag with same name already exists in the store")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@tags_blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @tags_blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @tags_blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


# /item/{id}/tag/{id} POST DELETE
# @tags_blp.route("/item/<string:item_id>/tag/<string:tag_id>")
# class ItemTags(MethodView):
#     def post(self):
#         return 200, "Post ItemTags"

#     def delete(self):
#         return 200, "delete ItemTags"
