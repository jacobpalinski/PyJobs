from flask_mongoengine import MongoEngine

db = MongoEngine()

class jobData(db.Document):
    pass