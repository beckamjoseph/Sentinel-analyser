# 🚀 Sentinel - URL Risk Intelligence System

**Complete Setup Guide - Step by Step Instructions**

## 📋 Prerequisites

- **Python 3.8+** (Python 3.14+ recommended)
- **pip** (Python package manager)
- **Chrome/Edge browser** (for browser extension)
- **Git** (optional, for version control)

## 🎯 Quick Setup (5 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd Divine-project/url-analyzer
```

### Step 2: Install Dependencies
```bash
# Install frontend dependencies
.\venv\Scripts\pip install -r frontend\requirements.txt

# Install backend dependencies
.\venv\Scripts\pip install -r backend\requirements.txt
```

### Step 3: Start Backend Server
```bash
.\venv\Scripts\python backend\manage.py runserver
```
- Backend will start on: http://127.0.0.1:8000
- Keep this terminal window open

### Step 4: Start Frontend Dashboard (New Terminal)
```bash
.\venv\Scripts\streamlit run frontend\app.py
```
- Dashboard will open at: http://localhost:8501
- Browser should open automatically

### Step 5: Install Browser Extension (Optional)
1. Open Chrome: `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. Shield icon 🛡️ appears in toolbar

### Step 6: Start Using!
- **Web Dashboard**: http://localhost:8501
- **Browser Extension**: Click the shield icon
- **Scan URLs**: Enter any URL to analyze

## 📁 Project Structure

```
Divine-project/url-analyzer/
├── backend/                      # Django REST API
│   ├── analyzer/                # Main Django app
│   │   ├── views.py            # API endpoints
│   │   ├── features.py         # URL feature extraction
│   │   ├── ml_model.py         # ML model integration
│   │   ├── threat_intel.py     # Threat intelligence
│   │   └── models.py           # Database models
│   ├── config/                  # Django settings
│   ├── manage.py               # Django management
│   ├── model.pkl               # Trained ML model
│   ├── db.sqlite3              # Database
│   └── requirements.txt         # Backend dependencies
├── frontend/                     # Streamlit dashboard
│   ├── app.py                  # Premium dashboard
│   └── requirements.txt         # Frontend dependencies
├── browser-extension/            # Chrome extension
│   ├── manifest.json            # Extension config
│   ├── popup.html/js/css        # Extension UI
│   ├── background.js            # Service worker
│   ├── content.js/css           # Page script
│   ├── icons/                   # Extension icons
│   └── README.md                # Extension docs
├── dataset/                      # Training data (optional)
├── .venv/                        # Virtual environment
└── Documentation/                # Setup guides
    ├── SETUP.md                 # This file
    ├── QUICK_START.md           # Quick start guide
    ├── SETUP_GUIDE.md           # Detailed setup
    ├── PROJECT_SUMMARY.md       # Project overview
    └── FIXES_SUMMARY.md         # Recent fixes
```

## 🔧 Detailed Setup Instructions

### 1. Environment Setup

#### Option A: Using Existing Virtual Environment (Recommended)
```bash
# Navigate to project
cd Divine-project/url-analyzer

# The virtual environment is already set up in .venv/
# Activate it (Windows)
.\venv\Scripts\activate

# Install dependencies
.\venv\Scripts\pip install -r frontend\requirements.txt
.\venv\Scripts\pip install -r backend\requirements.txt
```

#### Option B: Create New Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r frontend\requirements.txt
pip install -r backend\requirements.txt
```

### 2. Backend Setup

#### Django Database Initialization
```bash
cd backend
..\venv\Scripts\python manage.py migrate
```

#### Start Django Server
```bash
# From project root
.\venv\Scripts\python backend\manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 13, 2026 - 18:00:00
Django version 6.0.5, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Verify Backend:**
- Open http://127.0.0.1:8000/api/history/ in browser
- Should return JSON array (empty or with history)

### 3. Frontend Setup

#### Start Streamlit Dashboard
```bash
# From project root
.\venv\Scripts\streamlit run frontend\app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.197:8501
```

**Verify Frontend:**
- Browser should open automatically to http://localhost:8501
- You should see the premium dark theme dashboard
- Try scanning a URL to test functionality

### 4. Browser Extension Installation

#### Manual Installation (Developer Mode)
1. **Open Chrome Extensions Page**
   - Type `chrome://extensions/` in address bar
   - Press Enter

2. **Enable Developer Mode**
   - Toggle the switch in the top-right corner
   - "Developer mode" should appear at the top

3. **Load Extension**
   - Click "Load unpacked" button
   - Navigate to: `Divine-project/url-analyzer/browser-extension`
   - Select the folder
   - Click "Select Folder"

4. **Verify Installation**
   - You should see "Sentinel - URL Risk Intelligence" in extensions list
   - A shield icon 🛡️ appears in browser toolbar
   - Click the icon to open the extension popup

#### Extension Features
- **Current Page Scan**: Click to scan the webpage you're viewing
- **Custom URL Scan**: Enter any URL to analyze
- **Auto-scan Mode**: Automatically scans pages as you browse
- **Statistics**: Track total scans, threats blocked, safe sites
- **Settings**: Configure API endpoint and preferences

## 🌐 Access Points

### Web Dashboard
- **URL**: http://localhost:8501
- **Features**: Premium UI, interactive charts, color-coded analysis
- **Best for**: Detailed analysis, visualizations, history management

### Backend API
- **URL**: http://127.0.0.1:8000/api
- **Endpoints**:
  - `POST /api/analyze/` - Analyze a URL
  - `GET /api/history/` - Get scan history
  - `DELETE /api/clear-history/` - Clear history
- **Best for**: API integration, custom applications

### Browser Extension
- **Installation**: Load from `browser-extension` folder
- **Features**: Real-time scanning, safety indicators, statistics
- **Best for**: Everyday browsing protection, quick scans

## 🧪 Testing the Installation

### Test Backend API
```bash
# From project root
cd backend
..\venv\Scripts\python -c "import requests; response = requests.get('http://127.0.0.1:8000/api/history/'); print('Backend Status:', 'OK' if response.status_code == 200 else 'ERROR')"
```

### Test URL Scan
```bash
cd backend
..\venv\Scripts\python -c "import requests; response = requests.post('http://127.0.0.1:8000/api/analyze/', json={'url': 'https://google.com'}); result = response.json(); print('Test Scan:', result['risk_level'], '-', result['risk_score'], '%')"
```

### Test Frontend
1. Open http://localhost:8501
2. Enter a URL (e.g., https://google.com)
3. Click "🔍 Scan"
4. View the color-coded feature analysis
5. Check the interactive visualizations

### Test Extension
1. Click the shield icon in toolbar
2. Click "Scan Current URL"
3. View the results in the popup
4. Try entering a custom URL

## 🔍 Troubleshooting

### Backend Issues

**Server won't start:**
```bash
# Check if port 8000 is available
netstat -ano | findstr :8000

# Try different port
.\venv\Scripts\python backend\manage.py runserver 8001
```

**Database errors:**
```bash
# Reset database
cd backend
del db.sqlite3
..\venv\Scripts\python manage.py migrate
```

**Model loading errors:**
```bash
# Verify model file exists
dir backend\model.pkl

# Reinstall dependencies
.\venv\Scripts\pip install --upgrade -r backend\requirements.txt
```

### Frontend Issues

**Dashboard won't load:**
```bash
# Clear Streamlit cache
.\venv\Scripts\streamlit cache clear

# Restart with fresh config
.\venv\Scripts\streamlit run frontend\app.py --server.port 8501
```

**Plotly not working:**
```bash
# Ensure plotly is installed in venv
.\venv\Scripts\pip install plotly
```

**API connection errors:**
- Verify backend is running on port 8000
- Check API endpoint in sidebar settings
- Look for errors in browser console (F12)

### Extension Issues

**Extension won't load:**
- Verify Developer Mode is enabled
- Check that you selected the correct folder
- Look for error messages in extensions page

**Scans failing:**
- Confirm Django backend is running
- Check API endpoint in extension settings
- Review browser console for errors

**Auto-scan not working:**
- Enable auto-scan in extension settings
- Check content script permissions
- Ensure page has fully loaded

**Icons not displaying:**
```bash
cd browser-extension
python create_placeholder_icons.py
```

## 📚 Additional Resources

### Documentation Files
- **QUICK_START.md** - 5-minute quick start
- **SETUP_GUIDE.md** - Comprehensive setup guide
- **PROJECT_SUMMARY.md** - Complete project overview
- **browser-extension/README.md** - Extension documentation
- **FIXES_SUMMARY.md** - Recent improvements and fixes

### API Documentation
- **Backend API**: http://127.0.0.1:8000/api
- **API Endpoints**: See SETUP_GUIDE.md for details

### Configuration Files
- **backend/config/settings.py** - Django settings
- **frontend/app.py** - Streamlit configuration
- **browser-extension/manifest.json** - Extension config

## 🎯 Common Use Cases

### For Developers
- **API Integration**: Use backend endpoints for custom apps
- **Testing**: Use provided test scripts in backend/
- **Customization**: Modify frontend/app.py for UI changes
- **Extension Development**: Edit browser-extension files

### For Security Professionals
- **URL Analysis**: Use web dashboard for detailed analysis
- **Browsing Protection**: Install extension for real-time safety
- **Threat Research**: Use API for batch analysis
- **Education**: Demonstrate phishing patterns

### For Everyday Users
- **Safe Browsing**: Install browser extension
- **Link Verification**: Use web dashboard to check suspicious links
- **Email Safety**: Scan URLs from emails before clicking
- **Online Shopping**: Verify e-commerce URLs

## 🔐 Security Notes

- **Local Analysis**: All URL analysis happens locally when backend runs locally
- **No Data Collection**: No URLs are sent to external servers by default
- **Privacy First**: Extension stores only statistics locally
- **Domain Whitelist**: Known safe domains are automatically trusted

## 🚀 Production Deployment

### Backend Deployment
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend Deployment
```bash
# Deploy to Streamlit Cloud
streamlit run frontend\app.py

# Or use configuration file
# .streamlit/config.toml
[server]
port = 8501
baseUrlPath = "sentinel"
```

### Extension Distribution
- **Chrome Web Store**: Submit for review
- **Manual Distribution**: Zip the browser-extension folder
- **Enterprise**: Use group policy for deployment

## 📈 Performance Tips

- **Use Virtual Environment**: Ensures consistent dependencies
- **Keep Backend Running**: Prevents startup delays
- **Clear Cache Periodically**: Streamlit cache clear
- **Monitor Resources**: Check CPU/memory usage during scans

## 🆘 Getting Help

### Documentation
- Check this SETUP.md file first
- Review QUICK_START.md for quick reference
- Read browser-extension/README.md for extension help

### Common Issues
- See Troubleshooting section above
- Check FIX_LOG.md for recent fixes
- Review error messages carefully

### Support
- Open an issue on the project repository
- Check existing issues for solutions
- Contact development team if needed

## 🎉 Next Steps

1. **Test the System**: Scan a few URLs to verify functionality
2. **Explore Features**: Try the color-coded feature analysis
3. **Install Extension**: Add real-time browsing protection
4. **Customize Settings**: Adjust risk thresholds and preferences
5. **Review Documentation**: Learn about advanced features

---

**Enjoy your premium URL risk intelligence system!** 🛡️

*For questions or issues, refer to the documentation files in the project root.*