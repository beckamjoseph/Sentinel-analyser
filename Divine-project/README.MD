# AI-Powered Malicious URL Detection System

## Final Year Project README Documentation

---

# 1. Project Overview

This project is an AI-powered cybersecurity system designed to detect malicious URLs such as:

* Phishing websites
* Fake login pages
* Scam links
* Suspicious domains
* Malicious redirects

The system uses:

* Machine Learning
* Feature Engineering
* Django REST API
* SQLite Database
* Streamlit Dashboard

The application analyzes URLs in real time and predicts whether a URL is:

* SAFE
* MEDIUM RISK
* HIGH RISK

---

# 2. Main Objectives of the Project

The aim of this project is to:

1. Detect malicious URLs using AI
2. Extract URL-based cybersecurity features
3. Train a machine learning model on malicious and benign datasets
4. Build a real-time scanning system
5. Store scan history in a database
6. Provide an interactive dashboard for users

---

# 3. Technologies Used

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Main programming language |
| Django                | Backend framework         |
| Django REST Framework | API creation              |
| Streamlit             | Frontend dashboard        |
| Scikit-learn          | Machine learning          |
| Pandas                | Dataset processing        |
| SQLite                | Database                  |
| Joblib                | Model saving/loading      |
| Requests              | API communication         |

---

# 4. System Architecture

The system works in the following flow:

```text
User enters URL
        ↓
Streamlit Dashboard
        ↓
Django REST API
        ↓
Feature Extraction
        ↓
Machine Learning Model
        ↓
Prediction + Risk Score
        ↓
Database Storage
        ↓
Results Displayed to User
```

---

# 5. Project Folder Structure

```text
url-analyzer/
│
├── backend/
│   ├── analyzer/
│   ├── config/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── model.pkl
│   └── venv/
│
├── dataset/
│   └── malicious_phish.csv
│
├── ml_model/
│   ├── clean_dataset.py
│   ├── feature_engineering.py
│   ├── preprocess.py
│   ├── train.py
│   ├── processed_data.csv
│   ├── sample_urls.csv
│   └── model.pkl
│
├── frontend/
│   └── app.py
│
└── README.md
```

---

# 6. Understanding Each Folder

## backend/

This contains the Django backend.

Responsibilities:

* Receives API requests
* Extracts features
* Loads machine learning model
* Predicts URL safety
* Stores scan history
* Returns JSON responses

---

## analyzer/

Main application inside Django.

Contains:

* views.py
* models.py
* urls.py
* features.py
* ml_model.py

This is the heart of the system.

---

## dataset/

Contains raw datasets used for training.

Example:

```text
malicious_phish.csv
```

This dataset contains:

* benign URLs
* phishing URLs
* malicious URLs

---

## ml_model/

Contains all machine learning scripts.

Responsibilities:

* Cleaning datasets
* Feature extraction
* Preprocessing
* Model training
* Saving trained model

---

## frontend/

Contains the Streamlit dashboard.

Responsibilities:

* User interface
* URL input
* Displaying predictions
* Viewing history
* Clearing history

---

# 7. Backend File Explanations

---

# backend/analyzer/models.py

Purpose:

Defines database tables.

Main model:

```python
class URLScan(models.Model)
```

This stores:

* scanned URL
* prediction
* risk score
* risk level
* timestamp

Important fields:

| Field      | Purpose        |
| ---------- | -------------- |
| url        | URL scanned    |
| prediction | 0 or 1         |
| risk_score | AI confidence  |
| risk_level | SAFE/HIGH RISK |
| scanned_at | Time scanned   |

---

# backend/analyzer/features.py

Purpose:

Extracts numerical features from URLs.

Machine learning models cannot understand raw text URLs directly.

Therefore:

```text
https://google.com
```

must be converted into numerical values.

Example extracted features:

| Feature                  | Meaning                    |
| ------------------------ | -------------------------- |
| url_length               | Total URL length           |
| dot_count                | Number of dots             |
| hyphen_count             | Number of hyphens          |
| uses_https               | Whether HTTPS is used      |
| suspicious_keyword_count | Number of suspicious words |
| suspicious_tld           | Suspicious domain endings  |

These features help the AI detect suspicious patterns.

---

# backend/analyzer/ml_model.py

Purpose:

Loads trained machine learning model.

Key functions:

```python
joblib.load()
```

Loads saved model.

```python
predict_url()
```

Makes predictions using extracted features.

Returns:

* prediction
* probability score

---

# backend/analyzer/views.py

Purpose:

Handles API requests.

Main functions:

## analyze_url()

This function:

1. Receives URL from frontend
2. Extracts features
3. Sends features to AI model
4. Gets prediction
5. Determines risk level
6. Saves scan to database
7. Returns response

---

## scan_history()

Returns previous scan history.

Used by Streamlit dashboard.

---

## clear_history()

Deletes all scan records.

Used by clear history button.

---

# backend/analyzer/urls.py

Purpose:

Defines API routes.

Example:

```python
path('analyze/', analyze_url)
```

This means:

```text
/api/analyze/
```

will trigger:

```python
analyze_url()
```

---

# backend/config/settings.py

Purpose:

Main Django configuration.

Contains:

* installed apps
* middleware
* database settings
* REST framework settings

Important addition:

```python
'rest_framework'
```

This enables API functionality.

---

# backend/manage.py

Purpose:

Main Django management file.

Used for commands like:

```bash
python manage.py runserver
python manage.py migrate
python manage.py makemigrations
```

---

# 8. Machine Learning File Explanations

---

# ml_model/clean_dataset.py

Purpose:

Cleans raw dataset.

Responsibilities:

* removes duplicates
* converts labels
* balances dataset
* creates smaller training sample

This improves model quality.

---

# ml_model/feature_engineering.py

Purpose:

Converts URLs into machine-learning features.

Example:

```text
http://paypal-login.xyz
```

becomes:

```text
url_length = 25
hyphen_count = 1
suspicious_keyword_count = 2
```

---

# ml_model/preprocess.py

Purpose:

Applies feature extraction to entire dataset.

Creates:

```text
processed_data.csv
```

This file contains machine-learning-ready data.

---

# ml_model/train.py

Purpose:

Trains machine learning model.

Steps:

1. Loads processed dataset
2. Splits train/test data
3. Trains Random Forest model
4. Evaluates performance
5. Saves trained model

Metrics produced:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

---

# 9. Frontend File Explanation

---

# frontend/app.py

Purpose:

Main Streamlit dashboard.

Responsibilities:

* Accept URL input
* Send requests to Django API
* Display predictions
* Show risk score
* Display scan history
* Clear history

---

# 10. How Machine Learning Works in This Project

Machine learning follows these steps:

---

## Step 1 — Dataset Collection

Dataset contains:

* safe URLs
* malicious URLs

---

## Step 2 — Feature Engineering

URLs converted into numerical values.

Example:

```text
https://google.com
```

becomes:

```text
url_length = 18
uses_https = 1
```

---

## Step 3 — Model Training

Random Forest algorithm learns patterns.

It studies:

* suspicious keywords
* URL structure
* dangerous domain patterns

---

## Step 4 — Prediction

When new URL is entered:

1. Features extracted
2. Model predicts probability
3. Risk level returned

---

# 11. Risk Levels

The system classifies URLs into:

| Risk Score | Level       |
| ---------- | ----------- |
| 0% - 49%   | SAFE        |
| 50% - 79%  | MEDIUM RISK |
| 80% - 100% | HIGH RISK   |

---

# 12. Database Explanation

The project uses SQLite.

Database file:

```text
db.sqlite3
```

Stores:

* scan history
* timestamps
* predictions

---

# 13. How to Set Up the Project

---

# Step 1 — Clone Project

```bash
git clone <repository-url>
```

---

# Step 2 — Open Project

From the repository root, change into the `url-analyzer` project folder:

```bash
cd url-analyzer
```

If your current folder is the parent `Divine-project`, use:

```bash
cd Divine-project\url-analyzer
```

---

# Step 3 — Create Virtual Environment

```bash
python -m venv venv
```

---

# Step 4 — Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

# Step 5 — Install Dependencies

```bash
pip install django djangorestframework pandas numpy scikit-learn matplotlib joblib streamlit requests
```

---

# Step 6 — Run Migrations

Inside backend folder:

```bash
cd backend
```

Then:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Step 7 — Start Django Backend

Open a new terminal and go to the backend folder:

```bash
cd backend
```

Then run the backend with the project virtual environment:

```bash
..\venv\Scripts\python.exe manage.py runserver 8000
```

If the venv is already activated, this also works:

```bash
python manage.py runserver 8000
```

Backend runs at:

```text
http://127.0.0.1:8000/
```

---

# Step 8 — Start Streamlit Frontend

Open another terminal and make sure you are in the project root `url-analyzer` folder (not the parent repository folder):

```bash
cd url-analyzer
```

Run Streamlit through the project virtual environment:

```bash
.\venv\Scripts\streamlit.exe run frontend\app.py
```

If you are already inside `frontend`, run the command with the relative parent venv path instead:

```bash
..\venv\Scripts\streamlit.exe run app.py
```

If the venv is activated, this also works from the project root or from `frontend`:

```bash
streamlit run frontend\app.py
```

---

# 14. Important Commands

---

## Run Backend

```bash
python manage.py runserver
```

---

## Run Streamlit

From the project root (`url-analyzer`):

```bash
.\venv\Scripts\streamlit.exe run frontend\app.py
```

If the virtual environment is activated, you can also use:

```bash
streamlit run frontend\app.py
```

---

## Create Database Migrations

```bash
python manage.py makemigrations
```

---

## Apply Database Changes

```bash
python manage.py migrate
```

---

## Create Admin User

```bash
python manage.py createsuperuser
```

---

# 15. API Endpoints

| Endpoint            | Method | Purpose          |
| ------------------- | ------ | ---------------- |
| /api/analyze/       | POST   | Analyze URL      |
| /api/history/       | GET    | Get scan history |
| /api/clear-history/ | DELETE | Clear history    |

---

# 16. Example API Request

```json
{
  "url": "https://google.com"
}
```

---

# 17. Example API Response

```json
{
  "url": "https://google.com",
  "prediction": 0,
  "risk_score": 4.2,
  "risk_level": "SAFE"
}
```

---

# 18. Important Concepts to Understand

---

## What is Feature Engineering?

Feature engineering means converting raw data into useful numerical information for AI.

---

## What is Random Forest?

Random Forest is a machine learning algorithm.

It uses many decision trees to make predictions.

Benefits:

* good accuracy
* handles complex patterns
* suitable for cybersecurity tasks

---

## What is REST API?

An API allows frontend and backend communication.

Frontend sends requests.

Backend returns responses.

---

## What is Streamlit?

Streamlit is a Python framework for creating dashboards.

Advantages:

* simple
* fast
* ideal for machine learning projects

---

# 19. Common Errors and Fixes

---

## Error:

```text
Connection refused
```

Fix:

Django backend is not running.

Run:

```bash
python manage.py runserver
```

---

## Error:

```text
No module named ...
```

Fix:

Install missing package:

```bash
pip install package-name
```

---

## Error:

```text
No such table
```

Fix:

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Error:

```text
X does not have valid feature names
```

Fix:

Convert prediction features into DataFrame before prediction.

---

# 20. Future Improvements

Possible future enhancements:

* VirusTotal API integration
* WHOIS analysis
* SSL certificate validation
* Real-time threat intelligence
* User authentication
* PDF report export
* Explainable AI
* Dark cybersecurity theme
* Deployment to cloud

---

# 20.1 Improving real-world detection

The local machine-learning model examines URL text only. It cannot know whether a
new domain is currently hosting malware, so its risk score must not be treated as
a guarantee. The training script now produces a domain-separated holdout report
at `backend/model_metrics.json`; inspect that report after every retraining run.

For reputation-confirmed decisions, you can optionally enable VirusTotal lookup:

```powershell
$env:VIRUSTOTAL_API_KEY = "your_api_key"
```

Then start Django from the same terminal. A result with known malicious or
suspicious engines is promoted to high risk; a URL confirmed harmless by at
least five engines can correct a local false positive. The lookup is disabled by
default because submitted URLs are shared with the provider.

---

# 21. Academic Relevance

This project demonstrates:

* Machine Learning
* Cybersecurity
* AI-based threat detection
* Web development
* API development
* Database management
* Feature engineering
* Data preprocessing

It aligns with modern phishing detection methodologies.

---

# 22. Final Notes

This system was designed as an educational cybersecurity project focused on malicious URL detection using machine learning.

The project demonstrates:

* practical AI implementation
* cybersecurity analysis
* full-stack system integration
* real-time prediction architecture

The project can serve as:

* a final year project
* a machine learning portfolio project
* a cybersecurity research prototype
* a foundation for future commercial systems

---

# END OF README
