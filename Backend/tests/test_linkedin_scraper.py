import pytest
from linkedin_scraper import *
import requests_mock

@pytest.fixture
def generate_url_instance():
    generate_url = GenerateUrl()
    return generate_url

@pytest.fixture
def html_retriever_instance():
    html_retriever = HTMLRetriever()
    return html_retriever

@pytest.fixture
def linkedin_scraper():
    scraper = Scraper()
    return scraper

@pytest.fixture
def mock_html_results():
    with open('mock_html/Sydney _Python_ OR _Javascript_ OR _Typescript_ Jobs_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_data_engineer():
    with open('mock_html/Quantexa_Data_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_data_developer():
    with open('mock_html/Info_Way_Big_Data_Developer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_senior_manager_investment_data_management():
    with open('mock_html/Macquarie_Group_Martech_Analytics_Manager_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_data_analyst():
    with open('mock_html/Cashrewards_Data_Analyst_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_software_engineer():
    with open('mock_html/Macquarie_Group_Software_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def soup_object_results(html_retriever_instance,mock_html_results, requests_mock):
    url = 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'
    requests_mock.get(url, text = mock_html_results)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_engineer(html_retriever_instance,mock_html_job_details_data_engineer, requests_mock):
    url = 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3556628474'
    requests_mock.get(url, text = mock_html_job_details_data_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_developer(html_retriever_instance,mock_html_job_details_data_developer, requests_mock):
    url = 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3554271516'
    requests_mock.get(url, text = mock_html_job_details_data_developer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_senior_manager_investment_data_management(html_retriever_instance,mock_html_job_details_senior_manager_investment_data_management, requests_mock):
    url = 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3278353456'
    requests_mock.get(url, text = mock_html_job_details_senior_manager_investment_data_management)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_analyst(html_retriever_instance,mock_html_job_details_data_analyst, requests_mock):
    url = 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3514297385'
    requests_mock.get(url, text = mock_html_job_details_data_analyst)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_software_engineer(html_retriever_instance,mock_html_job_details_software_engineer, requests_mock):
    url = 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3436011836'
    requests_mock.get(url, text = mock_html_job_details_software_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

def test_generate_listings_url(generate_url_instance):
    city = 'Sydney'
    start_num = 0
    generate_url_instance.generate_listings_url(city,start_num)
    assert generate_url_instance.url == 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'

def test_generate_job_details_url(generate_url_instance):
    job_id = '12345'
    generate_url_instance.generate_job_details_url(job_id)
    assert generate_url_instance.url == 'https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/12345'

def test_get_html(html_retriever_instance,mock_html_results, requests_mock):
    url = 'https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'
    requests_mock.get(url, text = mock_html_results)
    html_retriever_instance.get_html(url)
    assert html_retriever_instance.html != None
    assert html_retriever_instance.html.title.text == '30 "Python" OR "Javascript" OR "Typescript" jobs in Sydney, New South Wales, Australia (30 new)'

def test_extract_job_ids(linkedin_scraper,soup_object_results):
    linkedin_scraper.extract_job_ids(soup_object_results)
    assert len(linkedin_scraper.job_ids) == len(set(linkedin_scraper.job_ids))
    assert len(linkedin_scraper.job_ids) == 24

def test_extract_job_data_data_engineer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_data_developer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_senior_manager_investment_data_management(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_data_analyst(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_machine_learning_scientist(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_machine_learning_engineer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_etl_developer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_software_engineering_manager(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_quality_assurance_engineer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_software_engineer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_frontend_developer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_quantitative_developer(linkedin_scraper,soup_object_job_details_software_engineer):
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

def test_extract_job_data_trader(linkedin_scraper,soup_object_job_details_software_engineer):
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
