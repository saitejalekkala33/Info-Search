import os
from dotenv import load_dotenv
from search.utils import setup_logging
from search.search_engine import SearchEngine
from search.scraper import Scraper
from search.extractor import Extractor

def main():
    load_dotenv()
    logger = setup_logging()
    cse_id = os.getenv("GOOGLE_CSE_ID")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not all([cse_id, openai_api_key]):
        logger.error("Missing required environment variables. Please set GOOGLE_CSE_ID, OPENAI_API_KEY in your .env file.")
        return

    person_name = "Sai Teja Lekkala" 
    affiliation = "National Institute of Technology, Silchar"

    search_engine = SearchEngine(logger, cse_id)
    scraper = Scraper(logger)
    extractor = Extractor(logger, person_name, affiliation, openai_api_key)

    logger.info("Fetching URLs from Google CSE...")
    urls = search_engine.fetch_urls(person_name, affiliation)
    if not urls:
        logger.error("No URLs found. Exiting.")
        return    
    logger.info("Starting scraping process...")
    content_dict = scraper.scrape_multiple_urls(urls)

    logger.info("Extracting relevant information...")
    relevant_info = extractor.extract_relevant_info(content_dict)

    print(f"Information for {person_name} at {affiliation}:\n")
    for url, snippets in relevant_info.items():
        print(f"From URL: {url}")
        for snippet in snippets:
            print(f"  - {snippet}")
        print()

if __name__ == "__main__":
    main()