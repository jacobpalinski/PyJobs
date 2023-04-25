from flask import Flask
from models import db
from views import job_data_blueprint

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    app.register_blueprint(job_data_blueprint, url_prefix='/job_data')
    return app

app = create_app('config')

