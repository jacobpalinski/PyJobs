from flask_mongoengine import MongoEngine
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

db = MongoEngine()

class jobData(db.Document):
    jobId = db.IntField(primary_key = True)
    company = db.StringField(required = True)
    location = db.StringField(required = True)
    jobTitle = db.StringField(required = True)
    group = db.StringField(choices = ['Data Science / Engineering','Management','Research','Testing','Software Engineering / Development',
    'Quantitative Finance / Trading'],required = True)
    programmingLanguages = db.ListField(db.StringField(choices = ['Python','JavaScript','TypeScript']), required = True, max_length = 3)
    databases = db.ListField(db.StringField(choices = ["MySQL","PostgreSQL","SQLite","MongoDB","MS SQL","SQL Server",
    "MariaDB","Firebase","ElasticSearch","Oracle","DynamoDB"]), max_length = 11)
    cloudProviders = db.ListField(db.StringField(choices = ["Amazon Web Services", "AWS", "Azure","Google Cloud","GCP"]), max_length = 3)
    link = db.StringField(required = True)
    datePosted = db.DateTimeField(default = datetime.date.today())

class User(db.Document):
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    admin = db.BooleanField(required = True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self,password):
        return check_password_hash(self.password, password)