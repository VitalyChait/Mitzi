from flask import Blueprint

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

from . import main_routes, auth_routes, events