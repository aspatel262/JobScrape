import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

class JobPosting:
    def __init__(self, title, location, link):
        self.title = title  # Posting title 
        self.location = location  # Posting location
        self.link = link  # Posting link

    def __eq__(self, other):
        if isinstance(other, JobPosting):
            return self.title == other.title and self.location == other.location and self.link == other.link
        return False

    def __repr__(self):
        return f"JobPosting(title='{self.title}', location='{self.location}', link='{self.link}')"

class Company:
    def __init__(self, site_link, scrape_protocol, recent_posting=None):
        self.site_link = site_link  # Link to job site
        self.scrape_protocol = scrape_protocol  # Tuple with tag type and className for parsing -- can vary by site
        self.previous_postings = self.fetch_current_postings()  # Initial state of previous postings
        self.recent_posting = recent_posting  # Most recent job posting

    def fetch_current_postings(self):
        response = requests.get(self.site_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_elements = soup.find_all(self.scrape_protocol[0], class_=self.scrape_protocol[1])

        if not job_elements:
            job_elements = self.fetch_dynamic_content()

        current_postings = []
        for job_element in job_elements:
            title_tag = job_element.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'

            company_tag = job_element.find('span', class_='RP7SMd')
            company = company_tag.find('span').get_text(strip=True) if company_tag else 'N/A'

            location_tag = job_element.find('span', class_='r0wTof')
            location = location_tag.get_text(strip=True) if location_tag else 'N/A'

            link_tag = job_element.find('a', href=True)
            link = link_tag['href'] if link_tag else 'N/A'

            current_postings.append(JobPosting(title, f"{company} - {location}", link))

        return current_postings

    def fetch_dynamic_content(self):
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(self.site_link)
        time.sleep(5)  # Wait for JavaScript to load content

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all(self.scrape_protocol[0], class_=self.scrape_protocol[1])

        driver.quit()

        return job_elements

    def check_change(self):
        current_postings = self.fetch_current_postings()
        new_postings = []

        if self.recent_posting:
            for posting in current_postings:
                if posting == self.recent_posting:
                    break
                new_postings.append(posting)
            new_postings.reverse()
        else:
            new_postings = current_postings

        if new_postings:
            self.recent_posting = new_postings[0]
            self.notify(new_postings)
            self.save_state()

    def save_state(self):
        try:
            with open('state.json', 'r') as file:
                state = json.load(file)
        except FileNotFoundError:
            state = {}

        state[self.site_link] = {
            'datetime': datetime.now().isoformat(),
            'previous_postings': [posting.__dict__ for posting in self.previous_postings],
            'recent_posting': self.recent_posting.__dict__ if self.recent_posting else None
        }

        with open('state.json', 'w') as file:
            json.dump(state, file, indent=4)

    def notify(self, new_postings):
        send_message(new_postings)

def send_message(new_postings):
    print('New job postings:')
    for posting in new_postings:
        print(posting)

def create_companies_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    companies = [Company(company['site_link'], tuple(company['scrape_protocol'])) for company in data]
    return companies

def load_state(companies):
    try:
        with open('state.json', 'r') as file:
            state = json.load(file)
            for company in companies:
                if company.site_link in state:
                    company.previous_postings = [JobPosting(**posting) for posting in state[company.site_link]['previous_postings']]
                    company.recent_posting = JobPosting(**state[company.site_link]['recent_posting']) if state[company.site_link]['recent_posting'] else None
    except FileNotFoundError:
        pass

# Example usage:
if __name__ == "__main__":
    companies = create_companies_from_json('companies.json')
    load_state(companies)

    for company in companies:
        company.check_change()
