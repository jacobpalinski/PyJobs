import datetime
import jwt
import os
from flask_mongoengine import MongoEngine
from flask_bcrypt import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

db = MongoEngine()

class jobData(db.Document):
    jobId = db.IntField(primary_key = True)
    company = db.StringField(required = True)
    location = db.StringField(required = True)
    jobTitle = db.StringField(required = True)
    group = db.StringField(choices = ['Data Science / Engineering', 'Management', 'Research', 'Testing', 'Software Engineering / Development',
    'Quantitative Finance / Trading'], required = True)
    databases = db.ListField(db.StringField(choices = ["MySQL", "PostgreSQL", "SQLite", "MongoDB", "MS SQL",
    "MariaDB", "Firebase", "ElasticSearch", "Oracle", "DynamoDB"]), max_length = 11)
    cloudProviders = db.ListField(db.StringField(choices = ["AWS", "Azure", "GCP"]), max_length = 3)
    link = db.StringField(required = True)
    datePosted = db.DateTimeField(default = datetime.date.today())

class User(db.Document):
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    admin = db.BooleanField(required = True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def encode_auth_token(self, user_id):
        # Generate Auth Token
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.environ.get('SECRET_KEY'),
                algorithm = 'HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        # Decode Auth Token
        try:
            payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again'
    
