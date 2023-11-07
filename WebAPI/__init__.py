from flask import Blueprint
from flask_restx import Api
from .namespaces.messages import messages_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

api.add_namespace(messages_ns)

from . import routes
