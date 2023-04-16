from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from httpstatus import HttpStatus
from models import jobData
from linkedin_scraper import *
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

    def patch(self):
        ''' Updates jobData based on parameters specified in request.'''
    def delete(self):
        ''' Lambda function to delete jobData when job post becomes 14 days old'''

job_data.add_resource(jobDataResource, '/jobData/')
