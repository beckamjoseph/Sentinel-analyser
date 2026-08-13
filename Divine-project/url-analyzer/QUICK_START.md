# 🚀 Quick Start Guide

**Get Sentinel running in 5 minutes!**

## ⚡ Fast Installation

### 1. Install Dependencies (Important!)

**Using the project virtual environment (RECOMMENDED):**
```bash
cd url-analyzer

# Install all dependencies at once
.\venv\Scripts\pip install -r frontend\requirements.txt
.\venv\Scripts\pip install -r backend\requirements.txt
```

**Why use the virtual environment?**
- ✅ Keeps dependencies isolated
- ✅ Prevents version conflicts
- ✅ Uses the correct Python environment
- ✅ Solves the "ModuleNotFoundError: No module named 'plotly'" issue

### 2. Start the Backend

```bash
# Using virtual environment (Recommended)
.\venv\Scripts\python backend\manage.py runserver
```

Backend will run on: `http://127.0.0.1:8000`

### 3. Start the Frontend

```bash
# Using virtual environment (Recommended)
.\venv\Scripts\streamlit run frontend\app.py
```

Dashboard will open at: `http://localhost:8501`

### 4. Install Browser Extension

1. Open Chrome: `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. Shield icon 🛡️ appears in toolbar

## 🎯 That's It!

- **Web Dashboard**: Open http://localhost:8501
- **Browser Extension**: Click the shield icon
- **Start Scanning**: Enter URLs and analyze!

## 🔧 Common Issues

### "ModuleNotFoundError: No module named 'plotly'"
**Solution:** Use the virtual environment
```bash
.\venv\Scripts\pip install plotly
```

### Backend won't start
**Solution:** Check if port 8000 is available
```bash
netstat -ano | findstr :8000
```

### Extension not loading
**Solution:** Make sure Developer Mode is enabled in Chrome extensions

## 📚 Full Documentation

- **SETUP_GUIDE.md** - Complete setup and configuration
- **PROJECT_SUMMARY.md** - Detailed project overview
- **browser-extension/README.md** - Extension documentation
- **FIXES_SUMMARY.md** - Recent improvements

---

**Need help?** Check the documentation files above!