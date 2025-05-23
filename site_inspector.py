import requests
from bs4 import BeautifulSoup
import whois
from datetime import datetime
import logging
import time

# Configure logging to show INFO and above level messages
logging.basicConfig(level=logging.INFO)

def get_domain_age(creation_date):
    """
    Calculate the domain age in years from the creation date.
    Handles if creation_date is a list or None.
    """
    if isinstance(creation_date, list):
        creation_date = creation_date[0]  # Take first date if multiple present
    if creation_date is None:
        return 0  # Return 0 if no creation date available
    return (datetime.now() - creation_date).days // 365  # Approximate years

def safe_whois_lookup(domain, retries=3, delay=2):
    """
    Perform a WHOIS lookup with retry logic to handle transient errors.
    Args:
        domain (str): Domain name to lookup.
        retries (int): Number of retry attempts.
        delay (int): Seconds to wait between retries.
    Returns:
        whois.whois object or None if all attempts fail.
    """
    for attempt in range(retries):
        try:
            return whois.whois(domain)
        except Exception as e:
            logging.warning(f"Whois lookup failed ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    logging.error(f"Whois lookup ultimately failed for domain: {domain}")
    return None

def get_wayback_data(domain, retries=3, delay=2):
    """
    Fetch website snapshot and history info from the Wayback Machine.
    Args:
        domain (str): Domain to query.
        retries (int): Number of retry attempts.
        delay (int): Seconds between retries.
    Returns:
        dict: Contains number of snapshots, first/last snapshot dates, change period in days.
    """
    session = requests.Session()
    for attempt in range(retries):
        try:
            # API endpoint for availability
            api_url = f"https://archive.org/wayback/available?url={domain}"
            snapshots = session.get(api_url, timeout=10).json()

            # Fetch history of snapshots with timestamp and digest for changes
            history_url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json&fl=timestamp&collapse=digest"
            changes = session.get(history_url, timeout=10).json()

            if len(changes) > 1:
                first = changes[1][0]
                last = changes[-1][0]
                first_date = datetime.strptime(first, '%Y%m%d%H%M%S')
                last_date = datetime.strptime(last, '%Y%m%d%H%M%S')
                change_period = (last_date - first_date).days
            else:
                first_date = last_date = None
                change_period = 0

            return {
                "snapshots_found": len(changes) - 1,
                "first_snapshot": str(first_date) if first_date else "N/A",
                "last_snapshot": str(last_date) if last_date else "N/A",
                "change_period_days": change_period
            }
        except Exception as e:
            logging.warning(f"Wayback history API attempt {attempt+1} failed: {e}")
            time.sleep(delay)

    logging.error(f"Wayback history API ultimately failed for domain: {domain}")
    return {
        "snapshots_found": 0,
        "first_snapshot": "N/A",
        "last_snapshot": "N/A",
        "change_period_days": 0
    }

def inspect_website_content(url):
    """
    Inspect a website by analyzing its content, images, whois data, and archive history.
    Calculates a trust score based on findings.

    Args:
        url (str): Website URL to inspect.

    Returns:
        dict: Contains success status, trust score, detected keywords, images,
              whois data, wayback data, and possible error info.
    """
    result = {
        "success": True,
        "trust_score": 100,
        "keywords_detected": [],
        "images_found": [],
        "whois_data": {},
        "wayback_data": {}
    }

    try:
        # Fetch page HTML
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # List of suspicious/risky keywords that lower trustworthiness
        risky_keywords = [
            # (same list as before)
            "first copy", "replica", "copy product", "grade 1 copy", "mirror copy",
            "super clone", "AAA quality", "top quality copy", "premium replica",
            "1:1 replica", "exact copy", "look alike", "imported replica",
            "original brand look", "branded lookalike", "inspired by", 
            "designer inspired", "brand style", "just like", "same as original",
            "cheap branded", "lowest price", "unbelievable price", "steal deal",
            "flash sale", "buy 1 get 1", "limited stock", "exclusive deal",
            "clearance sale", "wholesale price", "direct factory rate",
            "no return", "no warranty", "non-refundable", "cash on delivery only",
            "DM for price", "WhatsApp to order", "no customer support",
            "delivered in plain packaging", "avoid customs",
            "Nike copy", "Adidas first copy", "Apple replica", "Gucci inspired",
            "Rolex super clone", "Louis Vuitton first copy", "Samsung duplicate"
        ]

        found_keywords = []
        page_text = soup.get_text().lower()

        # Detect keywords and reduce trust score accordingly
        for word in risky_keywords:
            if word in page_text:
                found_keywords.append(word)
                result["trust_score"] -= 5

        # Extract image URLs with absolute paths starting with http
        image_tags = soup.find_all("img")
        image_urls = []
        for img in image_tags:
            src = img.get("src")
            if src and src.startswith("http"):
                image_urls.append(src)

        # Extract domain from URL for whois lookup
        domain = url.split("//")[-1].split("/")[0]

        # Perform WHOIS lookup with retries
        w = safe_whois_lookup(domain)

        # Calculate domain age and extract country information
        if w:
            domain_age = get_domain_age(w.creation_date)
            whois_country = w.country if hasattr(w, "country") and w.country else "Unknown"
        else:
            domain_age = 0
            whois_country = "Unknown"

        # Penalize trust score if domain is very new
        if domain_age < 1:
            result["trust_score"] -= 10

        # Store WHOIS data in results dictionary
        result["whois_data"] = {
            "domain": domain,
            "domain_age": domain_age,
            "creation_date": str(w.creation_date) if w else "N/A",
            "country": whois_country,
            "registrar": w.registrar if w else "N/A",
            "name_servers": w.name_servers if w and w.name_servers else []
        }

        # Fetch Wayback Machine archival data
        wayback_info = get_wayback_data(domain)
        result["wayback_data"] = wayback_info

        # Adjust trust score based on archival history
        if wayback_info["snapshots_found"] == 0:
            result["trust_score"] -= 10  # New/suspicious site without archival records
        elif wayback_info["change_period_days"] < 30:
            result["trust_score"] -= 5  # Website content changes rapidly

        # Add detected keywords and images to results
        result["keywords_detected"] = found_keywords
        result["images_found"] = image_urls

    except Exception as e:
        # Log any unexpected errors and update result accordingly
        logging.error(f"Exception during analysis: {e}")
        result["success"] = False
        result["error"] = str(e)

    return result
