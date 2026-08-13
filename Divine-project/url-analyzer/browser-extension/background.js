// Background service worker for Sentinel extension

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('Sentinel extension installed');
        // Initialize default settings
        chrome.storage.local.set({
            scanStats: {
                total: 0,
                threats: 0,
                safe: 0
            },
            settings: {
                autoScan: true,
                showNotifications: true,
                apiEndpoint: 'http://127.0.0.1:8000/api'
            }
        });
    } else if (details.reason === 'update') {
        console.log('Sentinel extension updated');
    }
});

// Listen for tab updates to auto-scan URLs
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // Check if auto-scan is enabled
        chrome.storage.local.get(['settings'], (result) => {
            if (result.settings && result.settings.autoScan) {
                // Send message to content script to scan the URL
                chrome.tabs.sendMessage(tabId, {
                    action: 'autoScan',
                    url: tab.url
                }).catch(() => {
                    // Content script might not be loaded yet, that's okay
                    console.log('Content script not ready for auto-scan');
                });
            }
        });
    }
});

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scanUrl') {
        scanUrl(request.url)
            .then(result => sendResponse({ success: true, data: result }))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // Keep message channel open for async response
    }
    
    if (request.action === 'getStats') {
        chrome.storage.local.get(['scanStats'], (result) => {
            sendResponse(result.scanStats || { total: 0, threats: 0, safe: 0 });
        });
        return true;
    }
    
    if (request.action === 'updateStats') {
        chrome.storage.local.get(['scanStats'], (result) => {
            const stats = result.scanStats || { total: 0, threats: 0, safe: 0 };
            stats.total++;
            if (request.isThreat) {
                stats.threats++;
            } else {
                stats.safe++;
            }
            chrome.storage.local.set({ scanStats: stats });
            sendResponse(stats);
        });
        return true;
    }
});

// Scan URL using the backend API
async function scanUrl(url) {
    const settings = await getSettings();
    const apiEndpoint = settings.apiEndpoint || 'http://127.0.0.1:8000/api';
    
    try {
        const response = await fetch(`${apiEndpoint}/analyze/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Scan error:', error);
        throw error;
    }
}

// Get extension settings
async function getSettings() {
    return new Promise((resolve) => {
        chrome.storage.local.get(['settings'], (result) => {
            resolve(result.settings || {
                autoScan: true,
                showNotifications: true,
                apiEndpoint: 'http://127.0.0.1:8000/api'
            });
        });
    });
}

// Show notification
function showNotification(title, message) {
    chrome.storage.local.get(['settings'], (result) => {
        if (result.settings && result.settings.showNotifications) {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icons/icon48.png',
                title: title,
                message: message,
                priority: 2
            });
        }
    });
}