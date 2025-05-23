from flask import Flask, render_template, request
import logging
import time
from site_inspector import inspect_website_content

app = Flask(__name__)

@app.route('/')
def index():
    """
    Route for the home page.
    Renders the main input form where users enter a website URL.
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def process():
    """
    Route to handle form submission for website analysis.
    Processes the submitted URL, runs inspection, and renders results or error page.
    """
    try:
        # Get URL from the submitted form data
        url = request.form["url"]

        # Simulate a delay to allow skeleton loader animation to show (optional)
        time.sleep(2)

        # Call the main inspection function from site_inspector.py
        results = inspect_website_content(url)

        # If inspection fails, show error page with the error message
        if not results["success"]:
            return render_template("error.html", error=results["error"])

        # Render results page with all analysis data passed as template variables
        return render_template(
            "results.html",
            url=url,
            trust_score=results.get("trust_score", 0),
            keywords=results.get("keywords_detected", []),
            images=results.get("images_found", []),
            whois_data=results.get("whois_data", {}),
            location_match=results.get("location_match", False),
            wayback_data=results.get("wayback_data", {}),
            complaint_links=results.get("complaint_links", [])
        )

    except Exception as e:
        # Log detailed exception info for debugging
        logging.error("Exception during analysis", exc_info=True)
        # Render error page with the error message
        return render_template("error.html", error=str(e))

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    app.run(debug=True)
