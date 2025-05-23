import logging

# Set logging level to INFO to track function activity
logging.basicConfig(level=logging.INFO)

# Risk thresholds (can be used elsewhere in app for categorization)
RISK_THRESHOLD_LOW = 40
RISK_THRESHOLD_HIGH = 80

def evaluate_risk_score(images, keywords):
    """
    Calculate a trust/risk score based on number of images and red-flag keywords found.

    Args:
        images (list): List of image URLs or filenames extracted from the website.
        keywords (list): List of detected risky keywords on the webpage.

    Returns:
        int: A score between 0 and 100 where higher means more trustworthy.
    """
    # Penalize sites with fewer images, up to a max penalty of 50 points
    image_factor = 100 - min(len(images) * 5, 50)

    # Penalize sites with more risky keywords, max penalty 50 points
    keyword_factor = min(len(keywords) * 4, 50)

    # Combine factors into a final trust score; higher is better (max 100)
    score = max(0, 100 - (keyword_factor + (100 - image_factor)) // 2)

    logging.info(f"Calculated trust score: {score}")

    return score
