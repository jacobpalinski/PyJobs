from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from httpstatus import HttpStatus
from models import jobData
import json

job_data_blueprint = Blueprint('job_data',__name__)
job_data = Api(job_data_blueprint)

class jobDataResource(Resource):
    def get(self):
        ''' Retrieves jobs list based on request parameters specified in get request / filters on search page.
        Must be able to retrieve jobs based on parameters that take a list as a value eg. 'Programming Languages': ['Python','TypeScript']'''
        pass
    def post(self):
        ''' Uses Lambda function to scrape data using linkedin_scraper.py script, checking for existing data in database,
        removing duplicates from new data, and inserts new data into database'''
        pass
    def patch(self):
        ''' Updates jobData based on parameters specified in request.'''
    def delete(self):
        ''' Lambda function to delete jobData when job post becomes 14 days old'''

job_data.add_resource(jobDataResource, '/jobData/')
