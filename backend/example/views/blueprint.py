from flask import Blueprint

# keep name of blueprint reference same as the bundle name
example = Blueprint('blog', __name__, url_prefix='/blog')
