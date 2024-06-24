import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class JobPosting:

    def __init__(self, name, title, location, link):
        self.name = name
        self.title = title  # Posting title
        self.location = location    # Posting location
        self.link = link  # Posting link

    def __eq__(self, other):
        if isinstance(other, JobPosting):
            return self.title == other.title and self.location == other.location and self.link == other.link
        return False

    def __repr__(self):
        return f"JobPosting(name='{self.name}, title='{self.title}', location='{self.location}', link='{self.link}')"

    def __hash__(self):
        return hash((self.name, self.title, self.location, self.link))


class Company:

    def __init__(self, name, site_link, scrape_protocol):
        self.name = name
        self.site_link = site_link  # Link to job site
        # Tuple with tag type and className for parsing -- can vary by site
        self.scrape_protocol = scrape_protocol
        # Initial state of previous postings
        self.previous_postings = self.fetch_current_postings()

    def fetch_current_postings(self):
        response = requests.get(self.site_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_elements = soup.find_all(
            self.scrape_protocol[0], class_=self.scrape_protocol[1])

        if not job_elements:
            job_elements = self.fetch_dynamic_content()

        current_postings = []
        for job_element in job_elements:
            title_tag = job_element.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'

            company_tag = job_element.find('span', class_='RP7SMd')
            company = company_tag.find('span').get_text(
                strip=True) if company_tag else 'N/A'

            location_tag = job_element.find('span', class_='r0wTof')
            location = location_tag.get_text(
                strip=True) if location_tag else 'N/A'

            link_tag = job_element.find('a', href=True)
            link = link_tag['href'] if link_tag else 'N/A'

            current_postings.append(JobPosting(self.name,
                                               title, f"{company} - {location}", link))

        return current_postings

    def fetch_dynamic_content(self):
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)
        driver.get(self.site_link)
        time.sleep(5)  # Wait for JavaScript to load content

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all(
            self.scrape_protocol[0], class_=self.scrape_protocol[1])

        driver.quit()

        return job_elements

    def check_change(self):
        current_postings = self.fetch_current_postings()
        if current_postings != self.previous_postings:
            new_postings = [
                new_post for new_post in current_postings if new_post not in self.previous_postings
            ]

            self.notify()
            # Update the previous postings with the current
            self.previous_postings = current_postings[-20:]


class Driver:

    def __init__(self, companies):
        self.companies = companies  # Array of companies for driving protocol

    def start_checking(self, interval=1800):
        while True:
            for company in self.companies:
                company.check_change()
            time.sleep(interval)

    def notify(self):
        print('New job posted!')

# Example usage:


if __name__ == "__main__":
    # google = Company("google", site_link="https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&location=United%20States&target_level=INTERN_AND_APPRENTICE", scrape_protocol=('div', "sMn82b"))
    # amazon = Company(site_link="https://www.amazon.jobs/content/en/career-programs/student-programs?country%5B%5D=US",
    # scrape_protocol=('div', 'job-card-module_root__QYXVA'))
    capitalOne = Company(name="capital one", site_link="https://capitalone.wd1.myworkdayjobs.com/Capital_One?workerSubType=a12c70bf789e10572aab83c4780919ad",
                         scrape_protocol=('li', 'css-1q2dra3'))

    print(capitalOne.fetch_current_postings())
