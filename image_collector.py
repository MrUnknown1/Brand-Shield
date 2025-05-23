import os
import requests
import hashlib
from urllib.parse import urljoin
from web_crawler import crawl_target_page
import logging

# Set logging level to INFO to capture key events
logging.basicConfig(level=logging.INFO)

# Directory where downloaded images will be saved
DOWNLOAD_DIR = "downloaded_images"

def hash_filename(url):
    """
    Generate a consistent filename for an image based on its URL.
    Uses SHA-256 hash of the URL and truncates to first 16 chars.
    This avoids filename collisions and ensures safe file naming.
    """
    return hashlib.sha256(url.encode()).hexdigest()[:16] + ".jpg"

def collect_visual_content(base_url):
    """
    Crawl the target webpage, find all images, download them locally.
    
    Args:
        base_url (str): The webpage URL to crawl.
    
    Returns:
        list: Filenames of successfully downloaded images.
    """
    # Create directory for downloads if it doesn't exist
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Crawl the page and get parsed HTML content
    soup = crawl_target_page(base_url)

    # Find all <img> tags in the HTML
    img_tags = soup.find_all("img")

    # List to hold filenames of downloaded images
    saved_images = []

    for tag in img_tags:
        # Extract 'src' attribute (image URL)
        src = tag.get("src")
        if not src:
            continue  # Skip if no src attribute
        
        # Convert relative URLs to absolute URLs using base URL
        img_url = urljoin(base_url, src)

        # Generate a hashed filename for saving the image
        filename = hash_filename(img_url)

        # Full file path for saving the image locally
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        try:
            # Download the image content with a short timeout
            response = requests.get(img_url, timeout=5)
            if response.status_code == 200:
                # Write the image binary data to file
                with open(filepath, "wb") as f:
                    f.write(response.content)
                saved_images.append(filename)  # Track successful downloads
                logging.info(f"Downloaded: {filename}")
        except Exception as e:
            # Log any failures but continue processing other images
            logging.warning(f"Failed to download image: {img_url} - {str(e)}")
    
    # Return list of saved image filenames
    return saved_images
