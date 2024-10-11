import trafilatura
import json
import os

class TextExtractor:
    def __init__(self):
        """
        Initialize the TextExtractor class.
        """
    def extract_text(self,url:str) -> str:
        """
        Extract text from a single URL using trafilatura.

        Args:
            url (str): The URL to extract text from.

        Returns:
            str or None: The extracted text, or None if extraction fails.
        """
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded, include_comments=False)
        return None
    def extract_multiple_text(self,urls:list) -> list:
        """
        Extract text from multiple URLs using trafilatura.

        Args:
            urls (list): A list of URLs to extract text from.

        Returns:
            list: A list of extracted texts. If extraction fails for any URL, the corresponding
                  entry in the list will be None.
        """
        return [self.extract_text(url) for url in urls]