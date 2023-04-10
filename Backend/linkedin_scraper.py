import requests
from bs4 import BeautifulSoup
import math
import regex as re
import datetime

class LinkedinScraper():
    # Programming languages, databases and cloud providers to search for when parsing html
    programming_languages = ["Python","JavaScript","TypeScript"]
    databases = ["MySQL","PostgreSQL","SQLite","MongoDB","Microsoft SQL Server",
    "MariaDB","Firebase","ElasticSearch","Oracle","DynamoDB"]
    cloud_providers = ["Amazon Web Services", "AWS", "Azure","Google Cloud","GCP"]
    location = ["Sydney"] # Other locations to be added later when AWS code works

    def __init__(self):
        self.job_ids= []
        self.job_data= []
    
    @staticmethod
    def generate_listings_url(city: str, start_num: int) -> str:
        url = f'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location={city}&f_TPR=r86400&position=1&pageNum=0&start={start_num}'
        return url

    @staticmethod
    def generate_job_details_url(job_id: str) -> str:
        url = f'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}'
        return url

    @staticmethod
    def get_html(url: str):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            print("Error occurred: ", e)
    
    def extract_job_ids(self,soup: BeautifulSoup):
        # Check if there are job listings for given url
        title = soup.title.text
        match = re.search(r'\d+',title)
        if match:
            # Extract job id for each listing
            job_divs = soup.find_all('div', class_ = 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
            for job in job_divs:
                job_id = job.get('data-entity-urn').split(':')[3]
                self.job_ids.append(job_id)
        else:
            return ('No jobs were posted')
    
    def extract_job_data(self, job_id: str, soup: BeautifulSoup):
        ''' To include in job_data {} object (in specified order):
            - Job ID
            - Company
            - Location
            - Industry
            - Job Title
            - Group (Data Science / Engineering, Software Engineering, Quantitative Finance / Trading, Research, Testing, Management)
            - Programming languages
            - Databases
            - Cloud Providers
            - Link
            - Date Posted'''
        # Job id
        id = int(job_id)
        # Extract company
        try:
            company = soup.find('div', class_ = 'topcard__flavor-row').find('a').text.strip()
        except:
            company = None
        # Extract location
        try:
            location = soup.find('div', class_ = 'topcard__flavor-row')\
            .find('span', class_ = 'topcard__flavor topcard__flavor--bullet').text.strip().split(',')[0]
        except:
            location = None
        # Extract industry
        try:
            industry = soup.find('ul', class_ = 'description__job-criteria-list').find_all('li')[3]\
            .text.replace('Industries', '').strip()
        except:
            industry = None
        # Extract job title
        try:
            job_title = soup.find('div', class_ = 'top-card-layout__entity-info').find('a').text.strip()
        except:
            job_title = None
        # Extract group
        try:
            if job_title != None:
                if 'data' in job_title.lower():
                    if 'data engineer' in job_title.lower():
                        group = 'Data Science / Engineering'
                    elif 'data developer' in job_title.lower():
                        group = 'Data Science / Engineering'
                    elif 'manager' in job_title.lower() or 'director' in job_title.lower() or 'head' in job_title.lower():
                        group = 'Management'
                    else:
                        group = 'Data Science / Engineering'
                elif ('research' in job_title.lower() and 'quantitative' not in job_title.lower()) \
                or ('scientist' in job_title.lower() and 'machine learning' in job_title.lower()) or ('researcher' in job_title.lower() and 'ai' in job_title.lower()):
                    group = 'Research'
                elif 'machine learning' in job_title.lower() or 'ml' in job_title.lower() or 'computer vision' in job_title.lower():
                        group = 'Data Science / Engineering'
                elif 'etl' in job_title.lower():
                    group = 'Data Science / Engineering'
                elif 'manager' in job_title.lower() or 'director' in job_title.lower() or 'head' in job_title.lower():
                    group = 'Management'
                elif 'test' in job_title.lower() or 'testing' in job_title.lower() or 'qa' in job_title.lower() or 'quality assurance' in job_title.lower() \
                or 'sdet' in job_title.lower():
                    group = 'Testing'
                elif 'engineer' in job_title.lower():
                    group = 'Software Engineering / Development'
                elif 'developer' in job_title.lower():
                    group = 'Software Engineering / Development'
                elif 'quantitative' in job_title.lower() or 'quant' in job_title.lower():
                    group = 'Quantitative Finance / Trading'
                elif 'trader' in job_title.lower() or 'trading' in job_title.lower():
                    group = 'Quantitative Finance / Trading'
                else:
                    group = None
            else:
                group = None
        except:
            group = None
        # Extract programming languages
        try:
            description = soup.find('div', class_ = 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5').get_text()
            programming_languages = []
            for language in LinkedinScraper.programming_languages:
                if language in description:
                    programming_languages.append(language)
        except:
            programming_languages = None
        # Extract databases
        try:
            description = soup.find('div', class_ = 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5').get_text()
            databases = []
            for database in LinkedinScraper.databases:
                if database in description:
                    databases.append(database)
        except:
            databases = None
        # Extract cloud provider
        try:
            description = soup.find('div', class_ = 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5').get_text()
            cloud_providers = []
            for provider in LinkedinScraper.cloud_providers:
                if provider in description:
                    cloud_providers.append(provider)
        except:
            cloud_providers = None
        # Extract link
        try:
            link = soup.find('a', class_ = 'topcard__link').get('href')
        except:
            link = None
        # Date posted
        date_posted = datetime.date.today()
        # Append to list
        self.job_data.append({'Job_Id':id, 'Company': company, 'Location': location, 'Industry': industry, 'Job Title': job_title, 'Group': group,
        'Programming Languages': programming_languages, 'Databases': databases, 'Cloud Providers': cloud_providers, 'Link': link, 'Date Posted': date_posted})



        

        

