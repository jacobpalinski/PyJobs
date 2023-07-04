import os
from flask import Flask
from flask_cors import CORS
from models import db
from views import job_data_blueprint

def create_app(config_filename):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)

    # Config for Docker below
    ''' app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('HOST'),
        'username': os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
        'password': os.environ.get('MONGO_INITDB_ROOT_PASSWORD'),
        'authentication_source': 'admin'
    }'''
    db.init_app(app)
    app.register_blueprint(job_data_blueprint, url_prefix='/job_data')
    return app

app = create_app('config')

