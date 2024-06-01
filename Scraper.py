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

    def __init__(self, site_link):
        self.previous_postings = []  # Ensure only the last 20 postings are stored
        self.site_link = site_link

class Driver:

    def __init__(self, companies):
        self.companies = companies


# Example usage:

if __name__ == "__main__":
    google = Company(site_link="https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&location=United%20States&target_level=INTERN_AND_APPRENTICE")
    amazon = Company(site_link="https://www.amazon.jobs/content/en/career-programs/student-programs?country%5B%5D=US")
    capitalOne = Company(site_link="https://capitalone.wd1.myworkdayjobs.com/Capital_One?workerSubType=a12c70bf789e10572aab83c4780919ad")

 