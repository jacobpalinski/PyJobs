from flask_mongoengine import MongoEngine
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

db = MongoEngine()

class jobData(db.Document):
    jobId = db.IntField(required = True, unique = True, primary_key = True)
    company = db.StringField(required = True)
    location = db.StringField(required = True)
    jobTitle = db.StringField(required = True)
    group = db.StringField(required = True)
    programmingLanguages = db.ListField(db.StringField(choices = ['Python','JavaScript','TypeScript']), required = True, max_length = 3)
    databases = db.ListField(db.StringField(choices = ["MySQL","PostgreSQL","SQLite","MongoDB","Microsoft SQL Server",
    "MariaDB","Firebase","ElasticSearch","Oracle","DynamoDB"]), required = True, max_length = 10)
    cloudProviders = db.ListField(db.StringField(choices = ["Amazon Web Services", "AWS", "Azure","Google Cloud","GCP"]), required = True, max_length = 3)
    link = db.StringField(required = True)
    datePosted = db.DateTimeField(default = datetime.date.today())
    
    meta = {'id_field': 'jobId'}

class User(db.Document):
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    admin = db.BooleanField(required = True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self,password):
        return check_password_hash(self.password, password)