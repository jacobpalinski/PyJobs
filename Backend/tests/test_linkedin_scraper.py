import pytest
import requests_mock
import boto3
from linkedin_scraper import *

@pytest.fixture
def mock_job_data():
    job_data = [{'Job_Id':3556628474, 'Company': 'Quantexa', 'Location': 'Sydney', 'Job Title': 'Data Engineer', 'Group': 'Data Science / Engineering',
    'Programming Languages': ['Python'], 'Databases': ['ElasticSearch'], 'Cloud Providers': ['GCP'], 
    'Link': 'https://au.linkedin.com/jobs/view/data-engineer-at-quantexa-3556628474?trk=public_jobs_topcard-title', 
    'Date Posted': datetime.date.today().strftime('%Y-%m-%d')},
    {'Job_Id':3554271516, 'Company': 'Info Way Solutions', 'Location': 'Fremont', 'Job Title': 'Big Data Developer', 'Group': 'Data Science / Engineering',
    'Programming Languages': ['Python'], 'Databases': [], 'Cloud Providers': ['AWS'], 
    'Link': 'https://www.linkedin.com/jobs/view/big-data-developer-at-info-way-solutions-3554271516?trk=public_jobs_topcard-title', 
    'Date Posted': datetime.date.today().strftime('%Y-%m-%d')}]
    return job_data

@pytest.fixture
def s3_mock(mocker,mock_job_data):
    mocker.patch("boto3.client", return_value = mocker.MagicMock())
    s3_mock = S3Bucket('pyscript-scraped-jobs','access_key','secret access key')
    s3_mock.s3.get_object.return_value = {
        'Body': mocker.MagicMock(read = mocker.MagicMock(return_value = json.dumps(mock_job_data).encode('utf-8')))
    }
    return s3_mock

def test_put_data(s3_mock,mock_job_data):
    current_date = datetime.date.today().strftime('%Y%m%d')
    s3_mock.put_data(mock_job_data,f'job_data{current_date}.json')
    s3_mock.s3.put_object.assert_called_once_with(Bucket = 'pyscript-scraped-jobs', Key = 'job_data20230505.json', Body=json.dumps(mock_job_data))

def test_get_data(s3_mock,mock_job_data):
    output = s3_mock.get_data('job_data20230505.json')
    print(output)
    s3_mock.s3.get_object.assert_called_once_with(Bucket = 'pyscript-scraped-jobs', Key = 'job_data20230505.json')
    assert output == mock_job_data

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
def mock_html_job_details_senior_manager_customer_data_science():
    with open('mock_html/Etsy_Senior_Manager_Customer_Data_Science_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_data_analyst():
    with open('mock_html/Cashrewards_Data_Analyst_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_machine_learning_scientist():
    with open('mock_html/BioSpace_Machine_Learning_Scientist_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_machine_learning_engineer():
    with open('mock_html/Rose_AI_Machine_Learning_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_etl_developer():
    with open('mock_html/ShiftCode_Analytics_ETL_Developer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_engineering_manager_software():
    with open('mock_html/Commonwealth_Bank_Engineering_Manager_Software_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_junior_quality_assurance_engineer():
    with open('mock_html/SMG_Studio_Junior_Quality_Assurance_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_software_engineer():
    with open('mock_html/Macquarie_Group_Software_Engineer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_frontend_developer():
    with open('mock_html/Real_Time_Australia_Frontend_Developer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_quantitative_developer():
    with open('mock_html/Quanteam_Quantitative_Developer_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def mock_html_job_details_quantitative_trader():
    with open('mock_html/Atto_Trading_Quantitative_Trader_job_details_Mock.html','r',encoding = 'utf-8') as html_content:
        html = html_content.read()
        yield html

@pytest.fixture
def soup_object_results(html_retriever_instance,mock_html_results, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0'
    requests_mock.get(url, text = mock_html_results)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_engineer(html_retriever_instance,mock_html_job_details_data_engineer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3556628474'
    requests_mock.get(url, text = mock_html_job_details_data_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_developer(html_retriever_instance,mock_html_job_details_data_developer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3554271516'
    requests_mock.get(url, text = mock_html_job_details_data_developer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_senior_manager_customer_data_science(html_retriever_instance,mock_html_job_details_senior_manager_customer_data_science, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3571787190'
    requests_mock.get(url, text = mock_html_job_details_senior_manager_customer_data_science)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_data_analyst(html_retriever_instance,mock_html_job_details_data_analyst, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3514297385'
    requests_mock.get(url, text = mock_html_job_details_data_analyst)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_machine_learning_scientist(html_retriever_instance,mock_html_job_details_machine_learning_scientist, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3573992159'
    requests_mock.get(url, text = mock_html_job_details_machine_learning_scientist)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_machine_learning_engineer(html_retriever_instance,mock_html_job_details_machine_learning_engineer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3555733284'
    requests_mock.get(url, text = mock_html_job_details_machine_learning_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_etl_developer(html_retriever_instance,mock_html_job_details_etl_developer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3569908450'
    requests_mock.get(url, text = mock_html_job_details_etl_developer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_engineering_manager_software(html_retriever_instance,mock_html_job_details_engineering_manager_software, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3568553070'
    requests_mock.get(url, text = mock_html_job_details_engineering_manager_software)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_junior_quality_assurance_engineer(html_retriever_instance,mock_html_job_details_junior_quality_assurance_engineer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3574765264'
    requests_mock.get(url, text = mock_html_job_details_junior_quality_assurance_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_software_engineer(html_retriever_instance,mock_html_job_details_software_engineer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3436011836'
    requests_mock.get(url, text = mock_html_job_details_software_engineer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_frontend_developer(html_retriever_instance,mock_html_job_details_frontend_developer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3556440712'
    requests_mock.get(url, text = mock_html_job_details_frontend_developer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_quantitative_developer(html_retriever_instance,mock_html_job_details_quantitative_developer, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3570855585'
    requests_mock.get(url, text = mock_html_job_details_quantitative_developer)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

@pytest.fixture
def soup_object_job_details_quantitative_trader(html_retriever_instance,mock_html_job_details_quantitative_trader, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://au.linkedin.com/jobs-guest/jobs/api/jobPosting/3567412548'
    requests_mock.get(url, text = mock_html_job_details_quantitative_trader)
    html_retriever_instance.get_html(url)
    return html_retriever_instance.html

def test_generate_listings_url(generate_url_instance):
    city = 'Sydney'
    start_num = 0
    generate_url_instance.generate_listings_url(city,start_num)
    assert generate_url_instance.url == 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0&dynamic=false'

def test_generate_job_details_url(generate_url_instance):
    job_id = '12345'
    generate_url_instance.generate_job_details_url(job_id)
    assert generate_url_instance.url == 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://linkedin.com/jobs-guest/jobs/api/jobPosting/12345&dynamic=false'

def test_get_html(html_retriever_instance,mock_html_results, requests_mock):
    url = 'https://api.scrapingdog.com/scrape?api_key=6443435218d5084d7d0e6e65&url=https://linkedin.com/jobs/search?keywords=%22Python%22%20OR%20%22Javascript%22%20OR%20%22TypeScript%22&location=Sydney&f_TPR=r86400&position=1&pageNum=0&start=0&dynamic=false'
    requests_mock.get(url, text = mock_html_results)
    html_retriever_instance.get_html(url)
    assert html_retriever_instance.html != None
    assert html_retriever_instance.html.title.text == '30 "Python" OR "Javascript" OR "Typescript" jobs in Sydney, New South Wales, Australia (30 new)'

def test_extract_job_ids(linkedin_scraper,soup_object_results):
    linkedin_scraper.extract_job_ids(soup_object_results)
    assert len(linkedin_scraper.job_ids) == len(set(linkedin_scraper.job_ids))
    assert len(linkedin_scraper.job_ids) == 24

def test_extract_job_data_data_engineer(linkedin_scraper,soup_object_job_details_data_engineer):
    linkedin_scraper.extract_job_data('3556628474',soup_object_job_details_data_engineer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3556628474
    assert linkedin_scraper.job_data[0]['Company'] == 'Quantexa'
    assert linkedin_scraper.job_data[0]['Location'] == 'Sydney'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Data Engineer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Data Science / Engineering'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == ['ElasticSearch']
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['GCP']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/data-engineer-at-quantexa-3556628474?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_data_developer(linkedin_scraper,soup_object_job_details_data_developer):
    linkedin_scraper.extract_job_data('3554271516',soup_object_job_details_data_developer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3554271516
    assert linkedin_scraper.job_data[0]['Company'] == 'Info Way Solutions'
    assert linkedin_scraper.job_data[0]['Location'] == 'Fremont'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Big Data Developer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Data Science / Engineering'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['AWS']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/big-data-developer-at-info-way-solutions-3554271516?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_senior_manager_customer_data_science(linkedin_scraper,soup_object_job_details_senior_manager_customer_data_science):
    linkedin_scraper.extract_job_data('3571787190',soup_object_job_details_senior_manager_customer_data_science)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3571787190
    assert linkedin_scraper.job_data[0]['Company'] == 'Etsy'
    assert linkedin_scraper.job_data[0]['Location'] == 'Brooklyn'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Senior Manager, Customer Data Science'
    assert linkedin_scraper.job_data[0]['Group'] == 'Management'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/senior-manager-customer-data-science-at-etsy-3571787190?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_data_analyst(linkedin_scraper,soup_object_job_details_data_analyst):
    linkedin_scraper.extract_job_data('3514297385',soup_object_job_details_data_analyst)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3514297385
    assert linkedin_scraper.job_data[0]['Company'] == 'Cashrewards'
    assert linkedin_scraper.job_data[0]['Location'] == 'Sydney'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Data Analyst'
    assert linkedin_scraper.job_data[0]['Group'] == 'Data Science / Engineering'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == ['MS SQL']
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/data-analyst-at-cashrewards-3514297385?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_machine_learning_scientist(linkedin_scraper,soup_object_job_details_machine_learning_scientist):
    linkedin_scraper.extract_job_data('3573992159',soup_object_job_details_machine_learning_scientist)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3573992159
    assert linkedin_scraper.job_data[0]['Company'] == 'BioSpace'
    assert linkedin_scraper.job_data[0]['Location'] == 'San Mateo'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Machine Learning Scientist (Remote)'
    assert linkedin_scraper.job_data[0]['Group'] == 'Research'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/machine-learning-scientist-remote-at-biospace-3573992159?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_machine_learning_engineer(linkedin_scraper,soup_object_job_details_machine_learning_engineer):
    linkedin_scraper.extract_job_data('3555733284',soup_object_job_details_machine_learning_engineer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3555733284
    assert linkedin_scraper.job_data[0]['Company'] == 'Rose AI'
    assert linkedin_scraper.job_data[0]['Location'] == 'New York'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Machine Learning Engineer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Data Science / Engineering'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['AWS','Azure','GCP']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/machine-learning-engineer-at-rose-ai-3555733284?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_etl_developer(linkedin_scraper,soup_object_job_details_etl_developer):
    linkedin_scraper.extract_job_data('3569908450',soup_object_job_details_etl_developer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3569908450
    assert linkedin_scraper.job_data[0]['Company'] == 'ShiftCode Analytics, Inc.'
    assert linkedin_scraper.job_data[0]['Location'] == 'Iselin'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'ETL Developer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Data Science / Engineering'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['Azure']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/etl-developer-at-shiftcode-analytics-inc-3569908450?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_engineering_manager_software(linkedin_scraper,soup_object_job_details_engineering_manager_software):
    linkedin_scraper.extract_job_data('3568553070',soup_object_job_details_engineering_manager_software)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3568553070
    assert linkedin_scraper.job_data[0]['Company'] == 'Commonwealth Bank'
    assert linkedin_scraper.job_data[0]['Location'] == 'Sydney'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Engineering Manager Software'
    assert linkedin_scraper.job_data[0]['Group'] == 'Management'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/engineering-manager-software-at-commonwealth-bank-3568553070?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_junior_quality_assurance_engineer(linkedin_scraper,soup_object_job_details_junior_quality_assurance_engineer):
    linkedin_scraper.extract_job_data('3574765264',soup_object_job_details_junior_quality_assurance_engineer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3574765264
    assert linkedin_scraper.job_data[0]['Company'] == 'SMG Studio'
    assert linkedin_scraper.job_data[0]['Location'] == 'Ultimo'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Junior Quality Assurance Engineer (Game Development)'
    assert linkedin_scraper.job_data[0]['Group'] == 'Testing'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/junior-quality-assurance-engineer-game-development-at-smg-studio-3574765264?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_software_engineer(linkedin_scraper,soup_object_job_details_software_engineer):
    linkedin_scraper.extract_job_data('3436011836',soup_object_job_details_software_engineer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3436011836
    assert linkedin_scraper.job_data[0]['Company'] == 'Macquarie Group'
    assert linkedin_scraper.job_data[0]['Location'] == 'Sydney'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Software Engineer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Software Engineering / Development'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == ['AWS']
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/software-engineer-at-macquarie-group-3436011836?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_frontend_developer(linkedin_scraper,soup_object_job_details_frontend_developer):
    linkedin_scraper.extract_job_data('3556440712',soup_object_job_details_frontend_developer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3556440712
    assert linkedin_scraper.job_data[0]['Company'] == 'Real Time Australia'
    assert linkedin_scraper.job_data[0]['Location'] == 'Redfern'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Frontend Developer'
    assert linkedin_scraper.job_data[0]['Group'] == 'Software Engineering / Development'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['JavaScript']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://au.linkedin.com/jobs/view/frontend-developer-at-real-time-australia-3556440712?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_quantitative_developer(linkedin_scraper,soup_object_job_details_quantitative_developer):
    linkedin_scraper.extract_job_data('3570855585',soup_object_job_details_quantitative_developer)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3570855585
    assert linkedin_scraper.job_data[0]['Company'] == 'Quanteam'
    assert linkedin_scraper.job_data[0]['Location'] == 'New York'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Quantitative Developer – New York'
    assert linkedin_scraper.job_data[0]['Group'] == 'Software Engineering / Development'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/quantitative-developer-%E2%80%93-new-york-at-quanteam-3570855585?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()

def test_extract_job_data_quantitative_trader(linkedin_scraper,soup_object_job_details_quantitative_trader):
    linkedin_scraper.extract_job_data('3567412548',soup_object_job_details_quantitative_trader)
    assert len(linkedin_scraper.job_data[0]) == 10
    assert linkedin_scraper.job_data[0]['Job_Id'] == 3567412548
    assert linkedin_scraper.job_data[0]['Company'] == 'Atto Trading'
    assert linkedin_scraper.job_data[0]['Location'] == 'New York County'
    assert linkedin_scraper.job_data[0]['Job Title'] == 'Quantitative Trader'
    assert linkedin_scraper.job_data[0]['Group'] == 'Quantitative Finance / Trading'
    assert linkedin_scraper.job_data[0]['Programming Languages'] == ['Python']
    assert linkedin_scraper.job_data[0]['Databases'] == []
    assert linkedin_scraper.job_data[0]['Cloud Providers'] == []
    assert linkedin_scraper.job_data[0]['Link'] == 'https://www.linkedin.com/jobs/view/quantitative-trader-at-atto-trading-3567412548?trk=public_jobs_topcard-title'
    assert linkedin_scraper.job_data[0]['Date Posted'] == datetime.date.today()
