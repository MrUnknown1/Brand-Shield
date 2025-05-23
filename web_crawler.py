import requests
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter, Retry

# Set up logging to show info and error messages
logging.basicConfig(level=logging.INFO)

def crawl_target_page(url):
    """
    Fetches the raw HTML content of the target URL using requests with retry logic.
    Parses the content with BeautifulSoup and returns the parsed HTML (soup).
    """

    # Define a common User-Agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    # Create a requests Session object to persist settings across requests
    session = requests.Session()

    # Configure retries: total 3 retries with exponential backoff for specific HTTP status codes
    retries = Retry(
        total=3,                    # Max retry attempts
        backoff_factor=1,           # Delay factor between retries: 1s, 2s, 4s
        status_forcelist=[502, 503, 504]  # Retry on these HTTP status codes
    )

    # Mount the HTTPAdapter with retry config to HTTPS URLs
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # Make a GET request to the URL with headers and a 10-second timeout
        response = session.get(url, headers=headers, timeout=10)

        # Raise an HTTPError if the response was unsuccessful (e.g., 404, 500)
        response.raise_for_status()

        # Log success info
        logging.info(f"Successfully crawled: {url}")

        # Parse the HTML content using BeautifulSoup and return the soup object
        return BeautifulSoup(response.text, 'html.parser')

    except Exception as e:
        # Log the error if the request or parsing failed
        logging.error(f"Failed to crawl {url}: {str(e)}")

        # Re-raise the exception to be handled by caller
        raise
