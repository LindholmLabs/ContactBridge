from flask import Blueprint

web_interface = Blueprint('web_interface', __name__)

from . import routes