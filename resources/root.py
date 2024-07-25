from flask.views import MethodView
from flask_smorest import Blueprint


root_blp = Blueprint("root", __name__, description="operations on root")


@root_blp.route("/")
class Root(MethodView):

    def get(self):
        return "python-flask-smorest-jwt-app", 200
