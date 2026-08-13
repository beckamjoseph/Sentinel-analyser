# Sentinel - Complete Setup Guide

Complete setup instructions for the Sentinel URL Risk Intelligence system, including the backend API, premium web dashboard, and browser extension.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Chrome/Edge browser (for extension)
- Git (optional, for cloning)

### Installation Steps

1. **Navigate to the project directory**
   ```bash
   cd Divine-project/url-analyzer
   ```

2. **Install Python dependencies**
   ```bash
   # Option 1: Using project virtual environment (Recommended)
   .\venv\Scripts\pip install -r frontend\requirements.txt
   .\venv\Scripts\pip install -r backend\requirements.txt
   
   # Option 2: Install globally
   pip install streamlit plotly pandas requests
   pip install django djangorestframework joblib pandas numpy scipy requests
   ```

3. **Start the Backend Server**
   ```bash
   # Using virtual environment (Recommended)
   .\venv\Scripts\python backend\manage.py runserver
   
   # Or directly
   cd backend
   python manage.py runserver
   ```
   The backend will start on `http://127.0.0.1:8000`

4. **Start the Frontend Dashboard** (in a new terminal)
   ```bash
   # Using virtual environment (Recommended)
   .\venv\Scripts\streamlit run frontend\app.py
   
   # Or directly
   cd frontend
   python -m streamlit run app.py
   ```
   The dashboard will open at `http://localhost:8501`

5. **Install the Browser Extension**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (top right toggle)
   - Click "Load unpacked"
   - Select the `browser-extension` folder
   - The Sentinel shield icon will appear in your toolbar

## 📁 Project Structure

```
url-analyzer/
├── backend/                 # Django REST API backend
│   ├── analyzer/           # Main Django app
│   │   ├── views.py        # API endpoints
│   │   ├── features.py     # URL feature extraction
│   │   ├── ml_model.py     # ML model integration
│   │   ├── threat_intel.py # Threat intelligence
│   │   └── models.py       # Database models
│   ├── config/             # Django settings
│   ├── manage.py           # Django management
│   ├── model.pkl           # Trained ML model
│   └── db.sqlite3          # Database
├── frontend/               # Streamlit web dashboard
│   └── app.py              # Main dashboard application
├── browser-extension/      # Chrome browser extension
│   ├── manifest.json       # Extension configuration
│   ├── popup.html/js/css   # Extension popup interface
│   ├── background.js       # Service worker
│   ├── content.js/css      # Page content script
│   └── icons/             # Extension icons
└── dataset/                # Training data (optional)
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/config/settings.py` for custom settings:

```python
# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings (if needed)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "chrome-extension://*"
]
```

### Frontend Configuration

Set environment variables or modify in `frontend/app.py`:

```python
# API endpoint
API_BASE_URL = os.getenv("URL_ANALYZER_API_URL", "http://127.0.0.1:8000/api")
```

### Extension Configuration

Configure via the extension popup Settings:
- API Endpoint: Default `http://127.0.0.1:8000/api`
- Auto-scan: Enable/disable automatic URL scanning
- Notifications: Enable/disable threat notifications

## 🎯 Usage Guide

### Web Dashboard

1. **Access the Dashboard**: Open `http://localhost:8501` in your browser

2. **Scan a URL**:
   - Enter any URL in the input field
   - Click "🔍 Scan" button
   - View detailed risk analysis with visualizations

3. **Explore Features**:
   - **Risk Gauge**: Visual risk score indicator
   - **Feature Radar**: Detailed feature analysis chart
   - **Statistics**: Track your scanning activity
   - **History**: View recent scan results

4. **Sidebar Settings**:
   - Configure API endpoint
   - Toggle auto-scan options
   - View scan statistics

### Browser Extension

1. **Scan Current Page**:
   - Navigate to any webpage
   - Click the Sentinel shield icon
   - Click "Scan Current URL"

2. **Scan Custom URL**:
   - Open extension popup
   - Enter URL in the input field
   - Click the scan button

3. **Auto-Scan Mode**:
   - Enable in Settings
   - Automatically scans pages as you browse
   - Shows safety indicator on each page

4. **View Statistics**:
   - Total scans performed
   - Threats blocked
   - Safe sites verified

## 🔍 API Documentation

### Endpoints

#### Analyze URL
```http
POST /api/analyze/
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://example.com",
  "prediction": 0,
  "risk_score": 25.5,
  "risk_level": "SAFE",
  "features": {
    "url_length": 18,
    "uses_https": 1,
    "has_ip": 0,
    "suspicious_keyword_count": 0,
    "subdomain_count": 0
  },
  "decision_source": "local_ml+whitelist",
  "reputation": {
    "enabled": false,
    "status": "not_configured"
  },
  "scanned_at": "2026-08-13T15:30:00Z"
}
```

#### Get Scan History
```http
GET /api/history/
```

#### Clear History
```http
DELETE /api/clear-history/
```

## 🛡️ Security Features

### URL Analysis

The system analyzes 31+ URL features:

- **Protocol Security**: HTTPS detection
- **Domain Analysis**: IP addresses, subdomains, TLDs
- **Content Patterns**: Suspicious keywords, redirects
- **Structural Analysis**: URL length, character distribution
- **Entropy Calculations**: Randomness detection
- **Heuristic Rules**: Brand impersonation detection

### Risk Levels

- **SAFE (0-60%)**: No major risk signals
- **MEDIUM RISK (60-80%)**: Suspicious patterns detected
- **HIGH RISK (80-100%)**: High probability of malicious content

### Protection Mechanisms

- **Domain Whitelist**: Known safe domains automatically trusted
- **Heuristic Enhancement**: Rule-based pattern detection
- **ML Model**: Machine learning prediction
- **Threat Intelligence**: Optional VirusTotal integration

## 🎨 Customization

### Branding

Modify the branding in:

**Frontend** (`frontend/app.py`):
```python
st.markdown('<h1 class="app-title">YOUR BRAND</h1>', unsafe_allow_html=True)
```

**Extension** (`browser-extension/popup.html`):
```html
<span class="logo-text">Your Brand</span>
```

### Color Themes

**Frontend CSS Variables** (`frontend/app.py`):
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    --danger-gradient: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
}
```

**Extension CSS Variables** (`browser-extension/popup.css`):
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --bg-dark: #0f0f1a;
    --accent: #667eea;
}
```

### Risk Thresholds

**Backend** (`backend/analyzer/views.py`):
```python
# Adjust these thresholds
if probability >= 0.8:
    risk_level = "HIGH RISK"
elif probability >= 0.6:
    risk_level = "MEDIUM RISK"
else:
    risk_level = "SAFE"
```

## 🐛 Troubleshooting

### Backend Issues

**Server won't start:**
```bash
# Check port availability
netstat -ano | findstr :8000

# Use different port
python manage.py runserver 8001
```

**Database errors:**
```bash
# Reset database
cd backend
rm db.sqlite3
python manage.py migrate
```

**Model loading errors:**
```bash
# Verify model file exists
ls backend/model.pkl

# Check dependencies
pip install joblib pandas numpy scipy
```

### Frontend Issues

**Dashboard won't load:**
```bash
# Check Streamlit installation
pip install --upgrade streamlit

# Clear cache
streamlit cache clear

# Restart with fresh config
streamlit run app.py --server.port 8501
```

**Plotly charts not showing:**
```bash
pip install plotly
```

**API connection errors:**
- Verify backend is running
- Check API endpoint in sidebar settings
- Look for CORS issues in browser console

### Extension Issues

**Extension won't load:**
- Verify Developer mode is enabled
- Check manifest.json syntax
- Ensure all files are present

**Scans failing:**
- Confirm backend is accessible
- Check API endpoint in extension settings
- Review browser console for errors

**Auto-scan not working:**
- Enable auto-scan in settings
- Check content script permissions
- Verify page has fully loaded

**Icons not displaying:**
```bash
cd browser-extension
python create_placeholder_icons.py
```

## 📊 Performance Optimization

### Backend

- Use a production database (PostgreSQL) for deployment
- Implement caching for frequently scanned URLs
- Add rate limiting to prevent abuse
- Use gunicorn for production serving

### Frontend

- Enable Streamlit caching for expensive operations
- Optimize data visualization complexity
- Implement lazy loading for history
- Use connection pooling for API requests

### Extension

- Implement local caching for scan results
- Batch multiple URL scans
- Debounce auto-scan triggers
- Optimize content script injection

## 🚀 Deployment

### Backend Deployment

**Using Docker:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

**Using Traditional Hosting:**
```bash
# Collect static files
python manage.py collectstatic

# Use gunicorn
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend Deployment

**Streamlit Sharing:**
```bash
# Deploy to Streamlit Cloud
streamlit run app.py

# Or use configuration file
# .streamlit/config.toml
[server]
port = 8501
baseUrlPath = "sentinel"
enableCORS = false
enableXsrfProtection = false
```

### Extension Deployment

**Chrome Web Store:**
1. Create developer account
2. Prepare extension package
3. Submit for review
4. Wait for approval

**Manual Distribution:**
- Zip the browser-extension folder
- Share with users
- Provide installation instructions

## 📈 Monitoring & Analytics

### Backend Monitoring

- Add logging to views.py
- Monitor API response times
- Track scan success rates
- Database query optimization

### Frontend Analytics

- Integrate Google Analytics
- Track user interactions
- Monitor feature usage
- A/B test different UI elements

### Extension Analytics

- Track installation rates
- Monitor scan frequency
- Analyze threat detection rates
- User behavior patterns

## 🔐 Security Best Practices

1. **API Security**: Add authentication for production
2. **Rate Limiting**: Prevent API abuse
3. **Input Validation**: Sanitize all user inputs
4. **HTTPS**: Use HTTPS in production
5. **CORS**: Configure proper CORS settings
6. **Secrets Management**: Never commit sensitive data
7. **Regular Updates**: Keep dependencies updated

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is part of the Sentinel URL Risk Intelligence system.

## 🆘 Support

For issues and questions:
- Check this documentation
- Review the FIXES_SUMMARY.md for recent changes
- Open an issue on the project repository
- Contact the development team

---

**Built with ❤️ for a safer internet**