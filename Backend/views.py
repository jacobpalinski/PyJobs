from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from mongoengine.errors import ValidationError
import json
from httpstatus import HttpStatus
from models import jobData, User
from linkedin_scraper import *

# Load environment variables for S3
load_dotenv()

job_data_blueprint = Blueprint('job_data',__name__)
job_data = Api(job_data_blueprint)
auth = HTTPBasicAuth()
s3 = S3Bucket()

@auth.verify_password
def verify_password(username,password):
    user = User.objects(username = username).first()
    if user and user.check_password(password):
        return user

class jobDataResource(Resource):
    def get(self):
        ''' Retrieves jobs list based on request parameters specified in get request / filters on search page.
        Must be able to retrieve jobs based on parameters that take a list as a value eg. 'Programming Languages': ['Python','TypeScript']'''
        # Extract arguments from get request
        query_args = {}
        for arg in request.args:
            if arg == 'location':
                query_args['location__in'] = list(request.args.getlist(arg))
            elif arg == 'company':
                query_args['company__in'] = list(request.args.getlist(arg))
            elif arg == 'group':
                query_args['group__in'] = list(request.args.getlist(arg))
            elif arg == 'language':
                query_args['programmingLanguages__in'] = list(request.args.getlist(arg))
            elif arg == 'database':
                query_args['databases__in'] = list(request.args.getlist(arg))
            elif arg == 'cloud':
                query_args['cloudProviders__in'] = list(request.args.getlist(arg))
            elif arg == 'days_old':
                query_args['datePosted__gte'] = datetime.datetime.now().date() - datetime.timedelta(days = int(request.args.get(arg)))
        # Query jobData. If date_order == ascending specified, return jobs in ascending order else descending
        if request.args.get('date_order'):
            if request.args.get('date_order') == 'ascending':
                data = jobData.objects(**query_args).order_by('+datePosted')
        else:
            data = jobData.objects(**query_args).order_by('-datePosted')
        # Convert QuerySet object to json
        json_data = json.loads(data.to_json())
        # Convert unix timestamp into datetime.date string
        for data in json_data:
            data['datePosted'] = datetime.datetime.fromtimestamp(data['datePosted']['$date'] / 1000.0).date().strftime('%Y-%m-%d')
        # Return output
        return json_data

    @auth.login_required
    def post(self):
        ''' Uses AWS batch function to scrape data using linkedin_scraper.py script, checking for existing data in database,
        removing duplicates from new data, and inserts new data into database'''
        user = auth.current_user()
        if not user.admin:
            return {'message': 'You need admin privileges to add jobs'}, HttpStatus.forbidden_403.value
        
        # Data file named for current date
        current_date = datetime.date.today().strftime('%Y%m%d')
        data_file = f'job_data{current_date}.json'
        
        # Load job data from S3
        job_data = s3.get_data(data_file)

        # Convert to list of dictionaries
        jobs_dict = [dict(job) for job in job_data]
            
        # Check if job_id for job is in jobData database
        for job in jobs_dict:
            queryset = jobData.objects(jobId = job['Job_Id'])
            if len(queryset) != 0:
                continue
            # Append new job to jobData database
            try:
                new_job = jobData(jobId = job['Job_Id'], company = job['Company'], location = job['Location'], jobTitle = job['Job Title'],
                group = job['Group'], programmingLanguages = job['Programming Languages'], databases = job['Databases'], cloudProviders = job['Cloud Providers'],
                link = job['Link'], datePosted = job['Date Posted'])
                print(new_job.to_mongo().to_dict())
                new_job.validate()
                new_job.save()
            except ValidationError as e:
                return {'message': str(e)}, HttpStatus.bad_request_400.value
        return {'message': 'New jobs added successfully'}, HttpStatus.created_201.value

    @auth.login_required
    def patch(self, id):
        ''' Updates jobData based on parameters specified in request.'''
        user = auth.current_user()
        if not user.admin:
            return {'message': 'You need admin privileges to update jobs'}, HttpStatus.forbidden_403.value
        
        data = jobData.objects(jobId = id).first()
        # Check if jobId exists
        if not data:
            return {'message': f"jobID {id} doesn't exist in database"}, HttpStatus.notfound_404.value
        try:
            # Update fields in jobData
            if 'company' in request.args:
                data.company = request.args.get('company')
            if 'location' in request.args:
                data.location = request.args.get('location')
            if 'industry' in request.args:
                data.industry = request.args.get('industry')
            if 'jobTitle' in request.args:
                data.jobTitle = request.args.get('jobTitle')
            if 'group' in request.args:
                data.group = request.args.get('group')
            if 'language' in request.args and 'language_index' in request.args:
                index = int(request.args.get('language_index'))
                language = request.args.get('language')
                if index < len(data.programmingLanguages):
                    data.programmingLanguages[index] = language
                elif index == len(data.programmingLanguages):
                    data.programmingLanguages.append(language)
            if 'database' in request.args and 'database_index' in request.args:
                index = int(request.args.get('database_index'))
                database = request.args.get('database')
                if index < len(data.databases):
                    data.databases[index] = database
                elif index == len(data.databases):
                    data.databases.append(language)
            if 'cloud' in request.args and 'cloud_index' in request.args:
                index = int(request.args.get('cloud_index'))
                cloud = request.args.get('cloud')
                if index < len(data.cloudProviders):
                    data.cloudProviders[index] = cloud
                elif index == len(data.cloudProviders):
                    data.cloudProviders.append(cloud)
            # Validate and save updates to document
            data.validate()
            data.save()
        except ValidationError as e:
            return {'message': str(e)}, HttpStatus.bad_request_400.value
        # Convert document to json
        json_data = json.loads(data.to_json())
        # Convert unix timestamp into datetime.date string
        json_data['datePosted'] = datetime.datetime.fromtimestamp(json_data['datePosted']['$date'] / 1000.0).date().strftime('%Y-%m-%d')
        # Return updated output
        return json_data

    @auth.login_required
    def delete(self):
        ''' Lambda function to delete jobData when job post becomes 14 days old'''
        user = auth.current_user()
        if not user.admin:
            return {'message': 'You need admin privileges to delete old jobs'}, HttpStatus.forbidden_403.value
        # Job posts >= 14 days old will be deleted
        earliest_date = datetime.date.today() - datetime.timedelta(days = 14)
        try:
            data = jobData.objects(datePosted__lte = earliest_date)
            data.delete()
            return {'message': 'Old jobs deleted successfully'}, HttpStatus.ok_200.value
        except Exception as e:
            return {'message': e}, HttpStatus.notfound_404.value

class UserResource(Resource):
    def post(self):
        user_register_dict = request.get_json()
        # Check if I have already created an admin user
        print(User.objects(admin=True))
        is_admin = User.objects(admin = True).count()
        if is_admin != 1:
            try:
                user = User(**user_register_dict) # user_register_dict should contain 'username','password' and 'admin' key value pairs
                user.hash_password()
                user.validate()
                user.save()
                return {'message': 'Admin user successfully registered'}, HttpStatus.created_201.value
            except ValidationError as e:
                return {'message': e.errors}, HttpStatus.unauthorized_401.value
        else:
            return {'message': 'Admin user already exists. If admin login'}, HttpStatus.conflict_409.value

job_data.add_resource(jobDataResource, '/jobData/','/jobData/<int:id>')
job_data.add_resource(UserResource, '/user/')
