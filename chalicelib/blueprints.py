
from chalice import Blueprint, Chalice

# from chalicelib.api.features import bp as feature_bp
from chalicelib.api.auth import bp as auth_routes
health_routes = Blueprint(__name__)

@health_routes.route('/')
def health():
    return 'ok'


def init_blueprint(app: Chalice):
    # v1


    app.register_blueprint(health_routes, url_prefix='/v1')
    app.register_blueprint(auth_routes, url_prefix='/auth')

    return app

