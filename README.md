# 🔒 Brand Shield - Website Analyzer

Brand Shield is a simple web application that analyzes a website's trustworthiness by inspecting its content, images, WHOIS data, and detected keywords. It helps users quickly assess the risk level of a website.

---

## 🚀 Features

* Fetches and analyzes images from the target website.
* Detects potentially risky keywords.
* Retrieves WHOIS information for domain verification.
* Calculates a trust/risk score based on multiple indicators.
* User-friendly interface built with Flask.
* Displays a skeleton loading screen during analysis.
* Supports PDF report downloads for offline reference.

---

## 💠 Setup Instructions

### Prerequisites

* Python 3.7 or higher
* `pip` package manager

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/brand-shield.git
   cd brand-shield
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Open your browser and visit**:
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📌 Usage

* Enter the URL of the website you want to analyze.
* Click **Analyze**.
* View results including:

  * Trust score
  * WHOIS data
  * Detected keywords
  * Suspicious images
* Download a **PDF report** if needed.

---

## 📂 Project Structure

```text
brand-shield/
├── app.py                # Flask app entry point
├── site_inspector.py     # Core logic for website analysis
├── web_crawler.py        # Web crawling and content extraction
├── static/
│   └── style.css         # CSS styles for the frontend
├── templates/
│   ├── index.html        # URL input page
│   ├── results.html      # Results display page
│   └── error.html        # Error page template
├── requirements.txt      # Required Python packages
└── README.md             # This file
```

---

## ⚠️ Notes

* The app uses **basic heuristics** for risk scoring and is intended for informational purposes, not as a definitive security tool.
* Ensure **network access** for WHOIS lookups and web crawling.
* For large or complex sites, analysis may take several seconds.

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).
