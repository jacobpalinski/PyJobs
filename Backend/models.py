from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class jobData(db.Document):
    jobId = db.IntField(required = True, unique = True, primary_key = True)
    company = db.StringField(required = True)
    location = db.StringField(required = True)
    industry = db.StringField(required = True)
    jobTitle = db.StringField(required = True)
    group = db.StringField(required = True)
    programmingLanguages = db.ListField(db.StringField(choices = ['Python','JavaScript','TypeScript']), required = True, max_length = 3)
    databases = db.ListField(db.StringField(choices = ["MySQL","PostgreSQL","SQLite","MongoDB","Microsoft SQL Server",
    "MariaDB","Firebase","ElasticSearch","Oracle","DynamoDB"]), required = True, max_length = 10)
    cloudProviders = db.ListField(db.StringField(choices = ["Amazon Web Services", "AWS", "Azure","Google Cloud","GCP"]), required = True, max_length = 3)
    link = db.StringField(required = True)
    datePosted = db.DateTimeField(default = datetime.date.today())
    
    meta = {'id_field': 'jobId'}