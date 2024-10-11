import requests
import json

credentials_path="/Users/jucampo/Desktop/Ideas/Podcast/credenciales/credentials.json"
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

class GoogleSearch:
    """
    A class to perform Google Custom Search API queries, rank the results, and extract specific URLs.
    
    Attributes
    ----------
    api_key : str
        The API key for accessing Google Custom Search.
    cx : str
        The Custom Search Engine ID for performing the search.
    
    Methods
    -------
    search(query, num_results=5):
        Performs a search query using the Google Custom Search API.
    
    rank_results(search_results, keyword):
        Ranks the search results based on the frequency of a keyword in the snippet.
    
    search_and_rank(query, keyword="", num_results=10):
        Performs a search and ranks the results based on the provided keyword.
    
    search_and_rank_various(l_queries, keyword=""):
        Executes and ranks results for multiple queries.
    
    get_web_url(l_l_results):
        Extracts the URLs from the ranked search results.
    """

    def __init__(self):
        """
        Initializes the GoogleSearch object with the necessary credentials for Google Custom Search.
        """
        self.api_key = credentials["google_search"]["apiKey"]
        self.cx = credentials["google_search"]["id_search"]

    def search(self, query, num_results=5):
        """
        Performs a Google Custom Search based on the query.

        Parameters
        ----------
        query : str
            The search term to query.
        num_results : int, optional
            The number of results to return (default is 5).
        
        Returns
        -------
        dict
            The search results in JSON format.
        """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.cx,
            'num': num_results
        }
        response = requests.get(url, params=params)
        return response.json()

    def rank_results(self, search_results, keyword):
        """
        Ranks the search results based on the occurrence of a keyword in the snippet.

        Parameters
        ----------
        search_results : dict
            The search results returned by the API.
        keyword : str
            The keyword used to rank the results.
        
        Returns
        -------
        list
            A list of ranked search results based on the keyword frequency.
        """
        def count_keyword_in_snippet(snippet):
            return snippet.lower().count(keyword.lower())

        items = search_results.get('items', [])
        ranked_items = sorted(items, key=lambda x: count_keyword_in_snippet(x.get('snippet', '')), reverse=True)
        return ranked_items

    def search_and_rank(self, query, keyword="", num_results=10):
        """
        Performs a search and ranks the results based on the keyword.

        Parameters
        ----------
        query : str
            The search term to query.
        keyword : str, optional
            The keyword to rank the results by (default is an empty string).
        num_results : int, optional
            The number of results to return (default is 10).
        
        Returns
        -------
        list
            A list of ranked search results.
        """
        search_results = self.search(query, num_results)
        ranked_results = self.rank_results(search_results, keyword)
        return ranked_results
    def search_and_rank_various(self, l_queries,keyword=""):
        """
        Executes search and ranking for a list of queries.

        Parameters
        ----------
        l_queries : list
            A list of search terms to query.
        keyword : str, optional
            The keyword to rank the results by (default is an empty string).
        
        Returns
        -------
        list
            A list of lists containing ranked search results for each query.
        """
        return [self.search_and_rank(query,keyword=keyword) for query in l_queries]
    def get_web_url(self, l_l_results):
        """
        Extracts the URLs from the ranked search results.

        Parameters
        ----------
        l_l_results : list
            A list of lists containing search result items.
        
        Returns
        -------
        list
            A list of lists with the URLs of the search results.
        """
        return [[result["link"] for result in l_results] for l_results in l_l_results]