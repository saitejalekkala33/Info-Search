from typing import Dict, List
from openai import OpenAI

class Extractor:
    def __init__(self, logger, person_name: str, affiliation: str, openai_api_key: str):
        self.logger = logger
        self.person_name = person_name
        self.affiliation = affiliation
        self.openai_client = OpenAI(api_key=openai_api_key)

    def extract_with_openai(self, content: str) -> List[str]:
        """Extract relevant information using the OpenAI API.

        Args:
            content (str): The scraped content.

        Returns:
            List[str]: List of relevant text snippets.
        """
        try:
            prompt = (
                f"Extract all relevant information about {self.person_name} "
                f"who is affiliated with {self.affiliation} from the following text:\n\n{content}\n\n"
                "Return the information as concise sentences, one per line."
            )
            response = self.openai_client.chat.completions.create(
                model="gpt-4.1-nano-2025-04-14",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts relevant information from text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.3
            )
            snippets = response.choices[0].message.content.strip().split("\n")
            snippets = [snippet.strip() for snippet in snippets if snippet.strip()]
            return snippets
        except Exception as err:
            self.logger.error(f"Error using OpenAI API: {err}")
            return ["Error occurred while extracting information with OpenAI API."]

    def extract_relevant_info(self, content_dict: Dict[str, str]) -> Dict[str, List[str]]:
        """Extract relevant information about the target person from scraped content using OpenAI API.

        Args:
            content_dict (Dict[str, str]): Dictionary mapping URLs to their scraped content.

        Returns:
            Dict[str, List[str]]: Dictionary mapping each URL to a list of relevant text snippets.
        """
        relevant_info = {}
        for url, content in content_dict.items():
            if not content:
                relevant_info[url] = ["No content available due to scraping failure."]
                continue

            snippets = self.extract_with_openai(content)
            if snippets and not snippets[0].startswith("Error occurred"):
                relevant_info[url] = snippets
                self.logger.info(f"Found {len(snippets)} relevant snippets for {self.person_name} at {url}")
            else:
                relevant_info[url] = ["No relevant information found."] if not snippets else snippets
                self.logger.info(f"No relevant information found for {self.person_name} at {url}")

        return relevant_info