from web_crawler import crawl_target_page
import logging

# Set up logging to capture info and error messages
logging.basicConfig(level=logging.INFO)

# List of suspicious keywords that might indicate risk or fraud on a website
RED_FLAG_KEYWORDS = [
    "guaranteed", "original copy", "no return", "discount", "authentic", "replica"
]

def scan_for_red_flags(url, keywords=RED_FLAG_KEYWORDS):
    """
    Scans the webpage at the given URL for the presence of red-flag keywords.

    Args:
        url (str): The URL of the webpage to scan.
        keywords (list): List of suspicious keywords to search for.

    Returns:
        list: Keywords detected on the page. Empty list if none found or on error.
    """
    try:
        # Use the web_crawler module to fetch and parse the page HTML
        soup = crawl_target_page(url)

        # Extract all text content from the page and convert to lowercase for case-insensitive matching
        body_text = soup.get_text().lower()

        # Check each red-flag keyword to see if it appears in the text
        detected = [word for word in keywords if word in body_text]

        # Log which suspicious keywords were found (if any)
        logging.info(f"Detected red-flag terms: {detected}")

        # Return the list of detected keywords
        return detected
    except Exception as e:
        # Log any errors during crawling or scanning
        logging.error(f"Keyword scan failed: {str(e)}")

        # Return empty list if an error occurs
        return []
