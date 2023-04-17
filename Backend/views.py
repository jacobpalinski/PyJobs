from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from httpstatus import HttpStatus
from models import jobData, User
from linkedin_scraper import *
import json
import datetime

job_data_blueprint = Blueprint('job_data',__name__)
job_data = Api(job_data_blueprint)

class jobDataResource(Resource):
    def get(self):
        ''' Retrieves jobs list based on request parameters specified in get request / filters on search page.
        Must be able to retrieve jobs based on parameters that take a list as a value eg. 'Programming Languages': ['Python','TypeScript']'''
        # Extract arguments from get request
        query_args = {}
        for arg in request.args:
            if arg == 'location':
                query_args['location'] = request.args.get(arg)
            elif arg == 'industry':
                query_args['industry'] = request.args.get(arg)
            elif arg == 'group':
                query_args['group'] = request.args.get(arg)
            elif arg == 'language':
                query_args['programmingLanguages__in'] = list(request.args.getlist(arg))
            elif arg == 'database':
                query_args['databases__in'] = list(request.args.getlist(arg))
            elif arg == 'cloud':
                query_args['cloudProviders__in'] = list(request.args.getlist(arg))
        # Query jobData. If date_order == ascending specified, return jobs in ascending order else descending
        if request.args.get('date_order'):
            if request.args.get('date_order') == 'ascending':
                data = jobData.objects(**query_args).order_by('+datePosted')
        else:
            data = jobData.objects(**query_args).order_by('-datePosted')
        # Convert QuerySet object to json and return output
        json_data = data.to_json()
        return jsonify(json.loads(json_data))

    def post(self):
        ''' Uses Lambda function to scrape data using linkedin_scraper.py script, checking for existing data in database,
        removing duplicates from new data, and inserts new data into database'''
        linkedin_scraper = Scraper()
        for location in Scraper.locations:
            # Retrieve total number of listings from initial loading page
            initial_url = linkedin_scraper.generate_url.generate_listings_url(location,0)
            html = linkedin_scraper.html_retriever.get_html(initial_url)
            title = html.title.text
            num_listings = re.search(r'\d+',title)

            if num_listings:
                num_loops = math.ceil(int(num_listings)/25)
                start_num = 0
                # Extract job_id from all listings
                for loop in range(0,num_loops):
                    url = linkedin_scraper.generate_url.generate_listings_url(location,start_num)
                    html = linkedin_scraper.html_retriever.get_html(url)
                    linkedin_scraper.extract_job_ids(html)
                    start_num += 25
                # Extract relevant job details from each listing
                for job_id in linkedin_scraper.job_ids:
                    job_details_url = linkedin_scraper.generate_url.generate_job_details_url(job_id)
                    job_details_html = linkedin_scraper.html_retriever.get_html(job_details_url)
                    linkedin_scraper.extract_job_data(job_id,job_details_html)
            
        # Check if job_id for job is in jobData database
        for job in linkedin_scraper.job_data:
            if jobData.objects(jobId = job['Job_Id']):
                continue
            # Append new job to jobData database
            try:
                new_job = jobData(jobID = job['Job_Id'], company = job['Company'], location = job['Location'], industry = job['Industry'], jobTitle = job['Job Title'],
                group = job['Group'], programmingLanguages = job['Programming Languages'], databases = job['Databases'], cloudProviders = job['Cloud Providers'],
                link = job['Link'], datePosted = job['Date Posted'])
                new_job.validate()
                new_job.save()
            except Exception as e:
                return {'message': e}, HttpStatus.bad_request_400.value
        return {'message': 'New jobs added successfully'}, HttpStatus.created_201.value

    def patch(self, id):
        ''' Updates jobData based on parameters specified in request.'''
        data = jobData.objects(jobId = id).first()
        # Check if jobId exists
        if not data:
            return {'message': f"jobID {id} doesn't exist in database"}, HttpStatus.notfound_404.value
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
        # Save updates to document
        data.save()
        # Convert document to json and return updated output
        json_data = data.to_json()
        return jsonify(json.loads(json_data))

    def delete(self):
        ''' Lambda function to delete jobData when job post becomes 14 days old'''
        # Job posts >= 14 days old will be deleted
        earliest_date = datetime.date.today() - datetime.timedelta(days = 14)
        try:
            data = jobData.objects(datePosted__lte = earliest_date)
            data.delete()
            return {'message': 'Old jobs deleted successfully'}, HttpStatus.no_content_204.value
        except Exception as e:
            return {'message': e}, HttpStatus.notfound_404.value

class UserResource(Resource):
    def post(self):
        user_register_dict = request.get_json()
        # Check if I have already created an admin user
        is_admin = User.objects(admin = True).count()
        if is_admin != 1:
            try:
                user = User(**user_register_dict) # user_register_dict should contain 'username','password' and 'admin' key value pairs
                user.hash_password()
                user.validate()
                user.save()
                return {'message': 'Admin user successfully registered'}, HttpStatus.created_201.value
            except Exception as e:
                return {'message': 'Error. Please try again'}, HttpStatus.unauthorized_401.value
        else:
            return {'message': 'Admin user already exists. If admin login'}, HttpStatus.conflict_409.value

job_data.add_resource(jobDataResource, '/jobData/','/jobData/<int:id>')
job_data.add_resource(UserResource, '/User/')
