# Quick Installation Steps

## 0. Install Dependencies

**Using the project virtual environment (Recommended):**
```bash
cd url-analyzer

# Install frontend dependencies
.\venv\Scripts\pip install -r frontend\requirements.txt

# Install backend dependencies  
.\venv\Scripts\pip install -r backend\requirements.txt
```

**Or install globally:**
```bash
pip install streamlit plotly pandas requests
pip install django djangorestframework joblib pandas numpy scipy requests
```

## 1. Install the Browser Extension

### Option A: Chrome/Edge (Recommended)

1. **Download/Clone the Project**
   - Ensure you have the `browser-extension` folder

2. **Open Browser Extensions**
   - Chrome: Go to `chrome://extensions/`
   - Edge: Go to `edge://extensions/`

3. **Enable Developer Mode**
   - Toggle the switch in the top-right corner

4. **Load the Extension**
   - Click "Load unpacked" button
   - Navigate to and select the `browser-extension` folder
   - Click "Select Folder"

5. **Verify Installation**
   - You should see "Sentinel - URL Risk Intelligence" in your extensions list
   - A shield icon 🛡️ will appear in your browser toolbar

### Option B: Firefox (Coming Soon)

Firefox support requires manifest V2 compatibility. This will be added in a future update.

## 2. Start the Backend

```bash
# Using virtual environment (Recommended)
.\venv\Scripts\python backend\manage.py runserver

# Or directly
cd backend
python manage.py runserver
```

The backend will start on `http://127.0.0.1:8000`

## 3. Start the Frontend

```bash
# Using virtual environment (Recommended)
.\venv\Scripts\streamlit run frontend\app.py

# Or directly
cd frontend
python -m streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 4. Test the Extension

1. **Open any webpage** (e.g., https://google.com)
2. **Click the Sentinel shield icon** in your toolbar
3. **Click "Scan Current URL"** to analyze the page
4. **View the results** with the beautiful UI

## 5. Test the Web Dashboard

1. **Open** `http://localhost:8501` in your browser
2. **Enter a URL** in the input field
3. **Click "🔍 Scan"** to analyze
4. **Explore the premium visualizations** and features

## Troubleshooting

### Extension not loading?
- Make sure Developer Mode is enabled
- Check that you selected the correct folder
- Look for error messages in the extensions page

### Scans failing?
- Ensure the Django backend is running
- Check that it's on port 8000
- Verify the API endpoint in extension settings

### Dashboard not loading?
- **IMPORTANT**: Use the project virtual environment
  ```bash
  .\venv\Scripts\streamlit run frontend\app.py
  ```
- Or install dependencies in the venv:
  ```bash
  .\venv\Scripts\pip install -r frontend\requirements.txt
  ```
- Ensure the backend is running
- Try clearing your browser cache

### Plotly import error?
- The frontend needs plotly installed in the virtual environment
- Run: `.\venv\Scripts\pip install plotly`
- Or use the requirements file: `.\venv\Scripts\pip install -r frontend\requirements.txt`

## Next Steps

- Read the full SETUP_GUIDE.md for detailed configuration
- Check browser-extension/README.md for extension features
- Review FIXES_SUMMARY.md for recent improvements

Enjoy your premium URL risk intelligence system! 🛡️