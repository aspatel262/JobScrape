import time
import requests
from bs4 import BeautifulSoup
from threading import Timer

 

class JobPosting:

    def __init__(self, title, location, link):
        self.title = title
        self.location = location
        self.link = link
 

class Company:

    def __init__(self, site_link, scrape_protocol):
        self.previous_postings = []  # Ensure only the last 20 postings are stored
        self.site_link = site_link
        self.scrape_protocol = scrape_protocol

class Driver:

    def __init__(self, companies):
        self.companies = companies


# Example usage:

if __name__ == "__main__":
    google = Company(site_link="https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&location=United%20States&target_level=INTERN_AND_APPRENTICE", scrape_protocol=('div',"sMn82b"))
    amazon = Company(site_link="https://www.amazon.jobs/content/en/career-programs/student-programs?country%5B%5D=US", scrape_protocol=('div','job-card-module_root__QYXVA'))
    capitalOne = Company(site_link="https://capitalone.wd1.myworkdayjobs.com/Capital_One?workerSubType=a12c70bf789e10572aab83c4780919ad", scrape_protocol=('li','css-1q2dra3'))

 