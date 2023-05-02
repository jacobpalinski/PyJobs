from flask import Flask
from models import db
from views import job_data_blueprint

def create_app(config_filename):
    app = Flask(__name__)
    # app.config.from_object(config_filename)
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://mongo:27017/pyscript',
        'username': 'ZingJP469',
        'password': 'Forzschem10',
        'authentication_source': 'admin'
    }
    db.init_app(app)
    app.register_blueprint(job_data_blueprint, url_prefix='/job_data')
    return app

app = create_app('config')

