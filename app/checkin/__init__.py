from flask import Blueprint

checkin_bp = Blueprint('checkin', __name__, url_prefix='/checkin')

from app.checkin import routes
