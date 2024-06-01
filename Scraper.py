import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class JobPosting:

    def __init__(self, title, location, link):
        self.title = title  # Posting title 
        self.location = location    # Posting location
        self.link = link # Posting link
 
    def __eq__(self, other):
        if isinstance(other, JobPosting):
            return self.title == other.title and self.location == other.location and self.link == other.link
        return False
 
    def __repr__(self):
        return f"JobPosting(title='{self.title}', location='{self.location}', link='{self.link}')"

class Company:

    def __init__(self, site_link, scrape_protocol):
        self.site_link = site_link  # Link to job site
        self.scrape_protocol = scrape_protocol  # Tuple with tag type and className for parsing -- can vary by site
        self.previous_postings = self.fetch_current_postings()  # Initial state of previous postings
    
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
    google = Company(site_link="https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&location=United%20States&target_level=INTERN_AND_APPRENTICE", scrape_protocol=('div',"sMn82b"))
    amazon = Company(site_link="https://www.amazon.jobs/content/en/career-programs/student-programs?country%5B%5D=US", scrape_protocol=('div','job-card-module_root__QYXVA'))
    capitalOne = Company(site_link="https://capitalone.wd1.myworkdayjobs.com/Capital_One?workerSubType=a12c70bf789e10572aab83c4780919ad", scrape_protocol=('li','css-1q2dra3'))

    
    print(google.fetch_current_postings())
    print("\n\n\n\n")
    print(amazon.fetch_current_postings())
    print("\n\n\n\n")
    print(capitalOne.fetch_current_postings())