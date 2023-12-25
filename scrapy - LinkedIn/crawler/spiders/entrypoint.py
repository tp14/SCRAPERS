# -- coding: utf-8 --
import logging
import re
import scrapy
from scrapy import Spider
import pdb
from scrapy import Request

LOGGER = logging.getLogger('EntrypointCrawler')

class EntrypointCrawler(Spider):
    name = "entrypoint"
    start_urls = ['https://phg.tbe.taleo.net/phg01/ats/servlet/Rss?org=PRPL&cws=53']
    #start_urls = ['https://www.linkedin.com/enterprise-jobs/3719665055?refId=JOB_SEARCH_JOB_CARD_CLICK%3A%3Ajobs_list_link%3A%3A4e062ab7-1c12-46f8-8271-c131bf9f880a&trackingId=GXFWh7%2BsX4bZDTUPBjn6Qg%3D%3D&refId=JOB_SEARCH_JOB_CARD_CLICK%3A%3Ajobs_list_link%3A%3A4e062ab7-1c12-46f8-8271-c131bf9f880a&trackingId=GXFWh7%2BsX4bZDTUPBjn6Qg%3D%3D&trk=jobs_list_link']


    domain_regexes = ['']

    career_regexes = [
        r'https://www\.linkedin\.com/careersite/(?P<account_id>[^/\s\.]+)'
    ]

    job_id_regexes = [
        r'https://www\.linkedin\.com/enterprise-jobs/(?P<job_id>\d+)'
    ]

    all_jobs = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'COOKIES_ENABLED': False,  # Depending on your use case, you may set this to True
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
            'Cache-Control': 'no-cache',
            'Origin': 'https://www.linkedin.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.linkedin.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        },
        'DOWNLOAD_DELAY': 5,  # Adjust the delay according to your scraping needs
        'DOWNLOAD_TIMEOUT': 30,  # Adjust the timeout as needed
    }
        
    def parse(self, response):
        pdb.set_trace()
        try:
            self.all_jobs = response.xpath('//tbody[@class="jobs-list__table-body"]/tr')
        except Exception as e:
            self.notify_sentry('Failed loading jobs', exception=e)
            return

        company_website = response.xpath('//*[@id="career-navbar-brand-link"]/@href').get()

        if len(self.all_jobs) == 0:
            yield self.parse_company_info(len(self.all_jobs), self.build_start_url(), response, company_website)
            LOGGER.info('No jobs were found on {}'.format(response.url))
            return

        yield from self.check_next_page(response, self.build_start_url(), company_website)

    def check_next_page(self, response, career_site_url, company_website):
        next_page = response.xpath('//a[@class="pagination_button pagination_button--next"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url= career_site_url + next_page,
                callback=self.get_jobs_next_page,
                cb_kwargs={
                    'career_site_url': career_site_url,
                    'company_website': company_website
                }
            )
        else:
            yield self.parse_company_info(len(self.all_jobs), self.build_start_url(), response, company_website)

            for job in self.all_jobs:
                title = job.xpath('.//td[@class="jobs-list__table-item-job-title"]/a/text()').get().strip()
                job_link = job.xpath('.//td[@class="jobs-list__table-item-job-title"]/a/@href').get()
                job_url = self.get_job_url(job_link)
                job_id = self.get_job_id(job_url)
                job_function = job.xpath('.//td[@class="jobs-list__table-item-function"]/text()').get().strip().replace('\xa0', ' ')
                location = job.xpath('.//td[@class="jobs-list__table-item-location"]/span[@data-test-jobs-list-location-place]/text()').get().strip()
                job_workplace = job.xpath('.//td[@class="jobs-list__table-item-location"]/span[@data-test-jobs-list-location-workplacetype]/text()').get().strip()

                yield self.validate_item(
                    dict(
                        type='job_info',
                        timestamp=self.timestamp,
                        url=job_url,
                        account_id=self.account_id,
                        job_id=job_id,
                        title=title,
                        location=location,
                        job_function= job_function,
                        job_type= job_workplace.strip('()')
                    ),
                    url=response.url
                )

    def get_jobs_next_page(self, response, career_site_url, company_website):
        self.all_jobs += response.xpath('//tbody[@class="jobs-list__table-body"]/tr')

        yield from self.check_next_page(response, career_site_url, company_website)

    def get_job_url(self, url):
        for rgx in self.job_id_regexes:
            match = re.search(rgx, url)
            if match:
                return match.group(0)

        return url
'''
import random
from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from time import sleep
import pdb

class EntrypointCrawler(Spider):
    name = "entrypoint"
    start_urls = ["https://www.linkedin.com/careersite/mdesignhomedecor"]

    def __init__(self, *args, **kwargs):
        super(EntrypointCrawler, self).__init__(*args, **kwargs)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)


    def parse(self, response):
        pdb.set_trace()
        self.driver.get(self.start_urls[0])

        # Simulate scrolling down the page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for some random time to mimic human behavior
        sleep(random.randint(3, 10))

        # Simulate clicking on an element (e.g., a "Load More" button)
        element = self.driver.find_element_by_xpath('//*[@id="jobs-list-filters__function-select"]')
        element.click()
        sleep(random.randint(3, 10))

        # Capture the current page source after scrolling and clicking
        page_source = self.driver.page_source

        # Create a Scrapy HtmlResponse object for further parsing
        #response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        # Use Scrapy selectors or Beautiful Soup for parsing
        #data = response.css('your-css-selector').extract()

        title = response.css('tr.jobs-list__table-item td.jobs-list__table-item-job-title a[data-test-jobs-list-title]::text').get()

        # Continue parsing and scraping as needed

        print(title)

        # Randomize delays between requests
        sleep(random.randint(5, 15))

        # Close the browser window
        self.driver.quit()
'''