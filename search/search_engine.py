from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from typing import List

class SearchEngine:
    def __init__(self, logger, cse_id: str):
        self.logger = logger
        self.cse_id = cse_id

    def fetch_urls(self, person_name: str, affiliation: str) -> List[str]:
        """Fetch URLs from Google CSE for the given person and affiliation.

        Args:
            person_name (str): Name of the person.
            affiliation (str): Affiliation of the person.

        Returns:
            List[str]: List of URLs found.
        """
        query = f"{person_name} {affiliation}"
        encoded_query = quote_plus(query)
        cse_url = f"https://cse.google.com/cse?cx={self.cse_id}&q={encoded_query}"
        self.logger.info(f"Scraping CSE results page: {cse_url}")

        # Set up Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(cse_url)
            time.sleep(3)  # Wait for JavaScript to load content

            # Parse the page source
            soup = BeautifulSoup(driver.page_source, "html.parser")
            search_results = soup.find_all("a", href=True)

            urls = []
            for link in search_results:
                href = link['href']
                # Filter for actual search result links
                if (href.startswith("http") and 
                    not href.startswith("https://cse.google.com") and 
                    not href.startswith("https://www.google.com")):
                    if not any(ext in href.lower() for ext in [".pdf", ".jpg", ".png", ".docx", ".xlsx", ".pptx", ".zip", ".jpeg"]):
                        urls.append(href)

            urls = list(set(urls))  # Ensure uniqueness
            self.logger.info(f"Found {len(urls)} URLs on CSE results page: {urls}")
            return sorted(urls)

        except Exception as err:
            self.logger.error(f"Error scraping CSE page: {err}")
            return []
        finally:
            driver.quit()