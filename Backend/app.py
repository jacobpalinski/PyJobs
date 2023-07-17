import os
from flask import Flask
from flask_cors import CORS
from models import db
from views import job_data_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Config for Docker
    app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('HOST'),
        'username': os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
        'password': os.environ.get('MONGO_INITDB_ROOT_PASSWORD'),
        'authentication_source': 'admin'
    }
    db.init_app(app)
    app.register_blueprint(job_data_blueprint, url_prefix = '/v1')
    return app

app = create_app()

