from flask import Flask
from models import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    #Add app.register_blueprint (blueprint_name) from views
    return app

app = create_app('config')

