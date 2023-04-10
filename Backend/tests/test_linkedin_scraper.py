import pytest
from linkedin_scraper import *
import requests_mock

@pytest.fixture
def mock_html_results():
    with open('mock_html/Sydney _Python_ OR _Javascript_ OR _Typescript_ Jobs_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_software_engineer():
    with open('mock_html/Macquarie_Group_Software_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def soup_object_results(mock_html_results, requests_mock):
    url = 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'
    requests_mock.get(url, text = mock_html_results)
    soup = LinkedinScraper.get_html(url)
    return soup

@pytest.fixture
def soup_object_job_details_software_engineer(mock_html_job_details_software_engineer, requests_mock):
    url = f'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3436011836'
    requests_mock.get(url, text = mock_html_job_details_software_engineer)
    soup = LinkedinScraper.get_html(url)
    return soup

def test_generate_listings_url():
    city = 'Sydney'
    start_num = 0
    url = LinkedinScraper.generate_listings_url(city,start_num)
    assert url == 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'

def test_generate_job_details_url():
    job_id = '12345'
    url = LinkedinScraper.generate_job_details_url(job_id)
    assert url == 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/12345'

def test_get_html(mock_html_results, requests_mock):
    url = 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'
    requests_mock.get(url, text = mock_html_results)
    soup = LinkedinScraper.get_html(url)
    assert soup != None
    assert soup.title.text == '30 "Python" OR "Javascript" OR "Typescript" jobs in Sydney, New South Wales, Australia (30 new)'

def test_extract_job_ids(soup_object_results):
    linkedin_scraper = LinkedinScraper()
    linkedin_scraper.extract_job_ids(soup_object_results)
    assert len(linkedin_scraper.job_ids) == len(set(linkedin_scraper.job_ids))
    assert len(linkedin_scraper.job_ids) == 24

def test_extract_job_data_software_engineer(soup_object_job_details_software_engineer):
    linkedin_scraper = LinkedinScraper()
    linkedin_scraper.extract_job_data('3436011836',soup_object_job_details_software_engineer)
    print(linkedin_scraper.job_data)
    assert len(linkedin_scraper.job_data[0]) == 11
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3436011836
    assert linkedin_scraper.job_data[0]['Company'] == 'Macquarie Group'
    assert linkedin_scraper.job_data[0]['Location'] == 'Sydney'
    assert linkedin_scraper.job_data[0]['Industry'] == 'Banking, Financial Services, and Investment Banking'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Software Engineer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Software Engineering / Development'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['AWS']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/software-engineer-at-macquarie-group-3436011836?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()
