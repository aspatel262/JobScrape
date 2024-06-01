import time
import requests
from bs4 import BeautifulSoup
from threading import Timer

 

class JobPosting:

    def __init__(self, title, link):
        self.title = title
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

 