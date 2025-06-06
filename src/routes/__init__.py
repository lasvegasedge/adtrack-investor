from flask import Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "AdTrack Investor — Now Live!"
