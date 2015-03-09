import os
from flask import Flask
from .models import db
from .auth import auth
from .decorators import json


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'config')

    db.init_app(app)

    from api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    if app.config['USE_TOKEN_AUTH']:
        from api.token import token as token_blueprint
        app.register_blueprint(token_blueprint, url_prefix='/auth')

    @app.route('/')
    @auth.login_required
    @json
    def index():
        from api.v1 import get_catalog as v1_catalog
        return {'versions': {'v1': v1_catalog()}}

    return app

