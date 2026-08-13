# Sentinel - Browser Extension

A beautiful, feature-rich Chrome extension for real-time URL risk analysis.

## Features

- 🛡️ **Real-time URL Scanning**: Instant analysis of any URL with advanced ML detection
- 🎨 **Beautiful UI**: Premium dark mode design with smooth animations
- 📊 **Visual Results**: Color-coded risk indicators with detailed feature analysis
- 🔔 **Smart Notifications**: Automatic alerts for high-risk URLs
- 📈 **Statistics Tracking**: Monitor your scanning activity and threat detection
- ⚡ **Fast Performance**: Optimized for minimal impact on browsing experience
- 🔗 **Seamless Integration**: Works with the Sentinel backend API

## Installation

### Manual Installation (Developer Mode)

1. **Clone or download this extension folder**

2. **Open Chrome Extension Management**:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right corner)

3. **Load the Extension**:
   - Click "Load unpacked"
   - Select the `browser-extension` folder
   - The extension will appear in your extensions list

4. **Verify Installation**:
   - You should see the Sentinel shield icon in your browser toolbar
   - Click the icon to open the popup interface

## Configuration

### API Endpoint

By default, the extension connects to `http://127.0.0.1:8000/api`. To change this:

1. Open the extension popup
2. Click the "Settings" button
3. Modify the API endpoint URL
4. Settings are automatically saved

### Auto-Scan Feature

The extension can automatically scan URLs when you navigate to new pages:

1. Open extension popup
2. Go to Settings
3. Toggle "Auto-scan on page load"
4. Enable/disable as needed

## Usage

### Popup Interface

1. **Current Page Scan**: Click "Scan Current URL" to analyze the page you're viewing
2. **Custom URL Scan**: Enter any URL in the input field and click the scan button
3. **View Results**: See detailed risk analysis with visual indicators
4. **Statistics**: Track your total scans, threats blocked, and safe sites

### Content Script Integration

When auto-scan is enabled:
- The extension automatically analyzes new pages as you navigate
- A safety indicator appears in the top-right corner for scanned pages
- High-risk pages show prominent warnings
- Safe pages show a brief indicator that auto-hides after 10 seconds

### Keyboard Shortcuts

Currently, the extension supports clicking the toolbar icon to open the popup. More shortcuts coming soon!

## Features Breakdown

### Risk Analysis

The extension provides three risk levels:

- **🟢 SAFE** (0-60%): No major risk signals detected
- **🟡 MEDIUM RISK** (60-80%): Suspicious patterns found, proceed with caution
- **🔴 HIGH RISK** (80-100%): High probability of phishing or malicious content

### Feature Analysis

Each scan analyzes 31+ URL features including:
- HTTPS usage
- IP address detection
- Suspicious keywords
- TLD analysis
- Subdomain structure
- URL length and complexity
- Special character patterns
- Entropy calculations

### Decision Sources

The extension uses multiple analysis methods:
- **ML Model**: Pure machine learning prediction
- **ML + Whitelist**: ML with domain whitelisting for known safe sites
- **ML + Heuristic**: ML enhanced with rule-based pattern detection
- **ML + Reputation**: ML combined with threat intelligence (when configured)

## Development

### Project Structure

```
browser-extension/
├── manifest.json          # Extension configuration
├── popup.html            # Main popup interface
├── popup.css             # Popup styling
├── popup.js              # Popup logic
├── background.js         # Service worker
├── content.js            # Page content script
├── content.css           # Content script styling
├── icons/                # Extension icons
│   ├── icon.svg
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── generate_icons.py     # Icon generation script
└── README.md             # This file
```

### Building Icons

To regenerate the extension icons:

```bash
cd browser-extension
python generate_icons.py
```

Or use the placeholder generator:
```bash
python create_placeholder_icons.py
```

### Testing the Extension

1. Make sure the Django backend is running:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Load the extension in Chrome (see Installation above)

3. Test functionality:
   - Open any webpage
   - Click the extension icon
   - Try scanning the current URL
   - Enter a custom URL to scan
   - Check the statistics update

### Debugging

1. **Popup Debugging**:
   - Right-click the extension popup
   - Select "Inspect"
   - Use Chrome DevTools

2. **Background Script Debugging**:
   - Go to `chrome://extensions/`
   - Find "Sentinel" extension
   - Click "Service worker" link
   - Use DevTools console

3. **Content Script Debugging**:
   - Open any webpage
   - Open DevTools (F12)
   - Check Console tab for content script logs

## API Integration

The extension communicates with the backend API:

### Endpoints Used

- `POST /api/analyze/` - Analyze a URL
- `GET /api/history/` - Get scan history
- `DELETE /api/clear-history/` - Clear scan history

### Request Format

```javascript
POST /api/analyze/
{
  "url": "https://example.com"
}
```

### Response Format

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
    ...
  },
  "decision_source": "local_ml+whitelist",
  "reputation": {
    "enabled": false,
    "status": "not_configured"
  },
  "scanned_at": "2026-08-13T15:30:00Z"
}
```

## Privacy & Security

- All URL analysis happens locally (when backend is running locally)
- No URLs are sent to external servers (except configured threat intelligence)
- Extension stores only scan statistics locally
- No personal data is collected or transmitted

## Troubleshooting

### Extension won't load

- Ensure you're in Developer mode
- Check that the folder path is correct
- Verify manifest.json syntax

### Scans failing

- Confirm Django backend is running on port 8000
- Check API endpoint settings in extension popup
- Look for error messages in DevTools console

### Auto-scan not working

- Verify auto-scan is enabled in settings
- Check content script permissions
- Ensure page has fully loaded

### Icons not displaying

- Regenerate icons using the provided scripts
- Check icon file paths in manifest.json
- Verify icon files exist in the icons/ folder

## Future Enhancements

- [ ] Keyboard shortcuts for quick scanning
- [ ]右-click context menu integration
- [ ] Bulk URL scanning
- [ ] Export scan reports
- [ ] Custom risk threshold settings
- [ ] Integration with more threat intelligence sources
- [ ] Multi-language support
- [ ] Dark/light theme toggle
- [ ] Advanced filtering and search in history

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Test thoroughly before submitting changes
2. Follow the existing code style
3. Update documentation as needed
4. Test on multiple Chrome versions

## License

This extension is part of the Sentinel URL Analyzer project.

## Support

For issues or questions:
- Check the main project README
- Review the backend API documentation
- Open an issue on the project repository

---

**Made with ❤️ for safer browsing**