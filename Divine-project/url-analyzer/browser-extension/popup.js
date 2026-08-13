// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const REQUEST_TIMEOUT = 10000;

// DOM Elements
const currentUrlDisplay = document.getElementById('currentUrl');
const scanCurrentBtn = document.getElementById('scanCurrentBtn');
const customUrlInput = document.getElementById('customUrlInput');
const scanCustomBtn = document.getElementById('scanCustomBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const resultCard = document.getElementById('resultCard');
const riskIcon = document.getElementById('riskIcon');
const riskLevel = document.getElementById('riskLevel');
const riskScore = document.getElementById('riskScore');
const progressFill = document.getElementById('progressFill');
const featuresGrid = document.getElementById('featuresGrid');
const decisionSource = document.getElementById('decisionSource');
const statusIndicator = document.getElementById('statusIndicator');
const totalScans = document.getElementById('totalScans');
const threatsBlocked = document.getElementById('threatsBlocked');
const safeSites = document.getElementById('safeSites');
const openDashboardBtn = document.getElementById('openDashboardBtn');
const settingsBtn = document.getElementById('settingsBtn');

// State
let currentTabUrl = '';
let scanStats = {
    total: 0,
    threats: 0,
    safe: 0
};

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadCurrentTab();
    await loadStats();
    setupEventListeners();
});

// Load current tab URL
async function loadCurrentTab() {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tab && tab.url) {
            currentTabUrl = tab.url;
            currentUrlDisplay.textContent = truncateUrl(tab.url, 50);
        }
    } catch (error) {
        console.error('Error loading current tab:', error);
        currentUrlDisplay.textContent = 'Unable to load URL';
    }
}

// Load scan statistics
async function loadStats() {
    try {
        const result = await chrome.storage.local.get(['scanStats']);
        if (result.scanStats) {
            scanStats = result.scanStats;
            updateStatsDisplay();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    scanCurrentBtn.addEventListener('click', () => scanUrl(currentTabUrl));
    scanCustomBtn.addEventListener('click', () => {
        const customUrl = customUrlInput.value.trim();
        if (customUrl) {
            scanUrl(customUrl);
        } else {
            showInputError(customUrlInput);
        }
    });
    
    customUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            scanCustomBtn.click();
        }
    });
    
    openDashboardBtn.addEventListener('click', openDashboard);
    settingsBtn.addEventListener('click', openSettings);
}

// Scan URL
async function scanUrl(url) {
    if (!url) {
        showError('No URL to scan');
        return;
    }

    showLoading();
    updateStatus('Scanning...');

    try {
        const response = await fetch(`${API_BASE_URL}/analyze/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);
        updateStats(result);
        updateStatus('Complete');
        
    } catch (error) {
        console.error('Scan error:', error);
        showError('Failed to analyze URL. Make sure the backend is running.');
        updateStatus('Error');
    }
}

// Display results
function displayResults(result) {
    hideLoading();
    resultsSection.style.display = 'block';

    // Update risk level and score
    const risk = result.risk_level;
    const score = result.risk_score;
    
    riskLevel.textContent = risk;
    riskScore.textContent = `${score}%`;

    // Update risk icon
    riskIcon.className = 'risk-icon';
    if (risk === 'SAFE') {
        riskIcon.classList.add('safe');
    } else if (risk === 'MEDIUM RISK') {
        riskIcon.classList.add('medium');
    } else {
        riskIcon.classList.add('high');
    }

    // Update progress bar
    progressFill.className = 'progress-fill';
    progressFill.style.width = `${score}%`;
    if (risk === 'SAFE') {
        progressFill.classList.add('safe');
    } else if (risk === 'MEDIUM RISK') {
        progressFill.classList.add('medium');
    } else {
        progressFill.classList.add('high');
    }

    // Update features
    displayFeatures(result.features);

    // Update decision source
    const sourceValue = decisionSource.querySelector('.source-value');
    sourceValue.textContent = formatDecisionSource(result.decision_source);
}

// Display features
function displayFeatures(features) {
    featuresGrid.innerHTML = '';
    
    const importantFeatures = [
        { key: 'uses_https', label: 'HTTPS', format: (v) => v ? 'Yes' : 'No' },
        { key: 'has_ip', label: 'IP Address', format: (v) => v ? 'Yes' : 'No' },
        { key: 'suspicious_keyword_count', label: 'Suspicious Words', format: (v) => v },
        { key: 'suspicious_tld', label: 'Suspicious TLD', format: (v) => v ? 'Yes' : 'No' },
        { key: 'subdomain_count', label: 'Subdomains', format: (v) => v },
        { key: 'url_length', label: 'URL Length', format: (v) => v },
        { key: 'digit_count', label: 'Digits', format: (v) => v },
        { key: 'at_count', label: '@ Symbols', format: (v) => v },
    ];

    importantFeatures.forEach(({ key, label, format }) => {
        if (features[key] !== undefined) {
            const featureItem = document.createElement('div');
            featureItem.className = 'feature-item';
            featureItem.textContent = `${label}: ${format(features[key])}`;
            featuresGrid.appendChild(featureItem);
        }
    });
}

// Update statistics
function updateStats(result) {
    scanStats.total++;
    
    if (result.prediction === 1) {
        scanStats.threats++;
    } else {
        scanStats.safe++;
    }

    chrome.storage.local.set({ scanStats });
    updateStatsDisplay();
}

// Update stats display
function updateStatsDisplay() {
    totalScans.textContent = scanStats.total;
    threatsBlocked.textContent = scanStats.threats;
    safeSites.textContent = scanStats.safe;
}

// Show loading state
function showLoading() {
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
}

// Hide loading state
function hideLoading() {
    loadingSection.style.display = 'none';
}

// Show error
function showError(message) {
    hideLoading();
    resultsSection.style.display = 'block';
    
    riskLevel.textContent = 'Error';
    riskScore.textContent = '--%';
    riskIcon.className = 'risk-icon high';
    progressFill.style.width = '0%';
    featuresGrid.innerHTML = `<div class="feature-item" style="grid-column: span 2; color: var(--danger);">${message}</div>`;
    
    const sourceValue = decisionSource.querySelector('.source-value');
    sourceValue.textContent = 'N/A';
}

// Update status indicator
function updateStatus(status) {
    const statusText = statusIndicator.querySelector('.status-text');
    const statusDot = statusIndicator.querySelector('.status-dot');
    
    statusText.textContent = status;
    
    if (status === 'Complete') {
        statusDot.style.background = 'var(--success)';
    } else if (status === 'Error') {
        statusDot.style.background = 'var(--danger)';
    } else {
        statusDot.style.background = '#667eea';
    }
}

// Open dashboard
function openDashboard() {
    chrome.tabs.create({ url: 'http://localhost:8501' });
}

// Open settings
function openSettings() {
    // For now, just show an alert
    alert('Settings panel coming soon!');
}

// Show input error
function showInputError(input) {
    input.style.borderColor = 'var(--danger)';
    input.style.animation = 'shake 0.3s ease-in-out';
    
    setTimeout(() => {
        input.style.borderColor = 'var(--border-color)';
        input.style.animation = '';
    }, 1000);
}

// Truncate URL for display
function truncateUrl(url, maxLength) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Format decision source
function formatDecisionSource(source) {
    const sourceMap = {
        'local_ml': 'ML Model',
        'local_ml+whitelist': 'ML + Whitelist',
        'local_ml+heuristic': 'ML + Heuristic',
        'local_ml+reputation': 'ML + Reputation',
    };
    return sourceMap[source] || source;
}