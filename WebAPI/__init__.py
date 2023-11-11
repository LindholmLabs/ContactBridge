from flask import Blueprint
from flask_restx import Api

from .namespaces.contact import contact_ns
from .namespaces.messages import messages_ns
from .namespaces.spam import spam_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

api.add_namespace(messages_ns)
api.add_namespace(contact_ns)
api.add_namespace(spam_ns)
