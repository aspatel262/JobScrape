import time
import requests
from bs4 import BeautifulSoup
from threading import Timer

 

class JobPosting:

    def __init__(self, title, location, link):
        self.title = title  # Posting title 
        self.location = location    # Posting location
        self.link = link # Posting link
 

class Company:

    def __init__(self, site_link, scrape_protocol):
        self.previous_postings = []  # Initial state of previous postings
        self.site_link = site_link  # Link to job site
        self.scrape_protocol = scrape_protocol  # Tuple with tag type and className for parsing -- can vary by site

class Driver:

    def __init__(self, companies):
        self.companies = companies  # Array of companies for driving protocol


# Example usage:

if __name__ == "__main__":
    google = Company(site_link="https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&location=United%20States&target_level=INTERN_AND_APPRENTICE", scrape_protocol=('div',"sMn82b"))
    amazon = Company(site_link="https://www.amazon.jobs/content/en/career-programs/student-programs?country%5B%5D=US", scrape_protocol=('div','job-card-module_root__QYXVA'))
    capitalOne = Company(site_link="https://capitalone.wd1.myworkdayjobs.com/Capital_One?workerSubType=a12c70bf789e10572aab83c4780919ad", scrape_protocol=('li','css-1q2dra3'))

 