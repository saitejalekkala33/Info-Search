import requests
from bs4 import BeautifulSoup
from typing import Dict

class Scraper:
    def __init__(self, logger):
        self.logger = logger
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
        }

    def scrape_url(self, url: str) -> str:
        """Scrape text content from a given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            str: The extracted text content, or an empty string if scraping fails.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Remove script and style tags
                for script in soup(["script", "style"]):
                    script.decompose()
                # Extract text
                text = soup.get_text(separator=" ", strip=True)
                self.logger.info(f"Successfully scraped content from {url}")
                return text
            else:
                self.logger.error(f"Failed to retrieve page {url}, status code: {response.status_code}")
                return ""
        except Exception as err:
            self.logger.error(f"Failed to scrape {url}: {err}")
            return ""

    def scrape_multiple_urls(self, urls: list) -> Dict[str, str]:
        """Scrape multiple URLs and return their content.

        Args:
            urls (list): List of URLs to scrape.

        Returns:
            Dict[str, str]: Dictionary mapping each URL to its scraped content.
        """
        content_dict = {}
        for url in urls:
            content = self.scrape_url(url)
            content_dict[url] = content
        return content_dict