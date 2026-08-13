// Content script for Sentinel extension

let currentUrl = window.location.href;
let safetyIndicator = null;

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeContentScript);
} else {
    initializeContentScript();
}

function initializeContentScript() {
    console.log('Sentinel content script initialized on:', currentUrl);
    
    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'autoScan') {
            scanCurrentPage(request.url)
                .then(result => {
                    sendResponse({ success: true, data: result });
                    if (result.prediction === 1) {
                        showSafetyIndicator(result);
                    }
                })
                .catch(error => {
                    console.error('Auto-scan error:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }
        
        if (request.action === 'showIndicator') {
            showSafetyIndicator(request.data);
            sendResponse({ success: true });
        }
        
        if (request.action === 'hideIndicator') {
            hideSafetyIndicator();
            sendResponse({ success: true });
        }
    });
}

// Scan current page URL
async function scanCurrentPage(url) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/analyze/', {
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
        console.error('Content script scan error:', error);
        throw error;
    }
}

// Show safety indicator on the page
function showSafetyIndicator(result) {
    // Remove existing indicator if any
    hideSafetyIndicator();
    
    // Create indicator element
    safetyIndicator = document.createElement('div');
    safetyIndicator.id = 'sentinel-safety-indicator';
    
    const isDangerous = result.prediction === 1;
    const riskLevel = result.risk_level;
    const riskScore = result.risk_score;
    
    // Set styling based on risk level
    let bgColor, borderColor, iconColor;
    if (riskLevel === 'HIGH RISK') {
        bgColor = 'rgba(255, 82, 82, 0.95)';
        borderColor = '#ff5252';
        iconColor = '#ffffff';
    } else if (riskLevel === 'MEDIUM RISK') {
        bgColor = 'rgba(255, 167, 38, 0.95)';
        borderColor = '#ffa726';
        iconColor = '#ffffff';
    } else {
        bgColor = 'rgba(0, 212, 170, 0.95)';
        borderColor = '#00d4aa';
        iconColor = '#ffffff';
    }
    
    safetyIndicator.innerHTML = `
        <div class="sentinel-indicator-content">
            <div class="sentinel-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="sentinel-info">
                <div class="sentinel-title">Sentinel</div>
                <div class="sentinel-risk">${riskLevel}</div>
                <div class="sentinel-score">${riskScore}% risk score</div>
            </div>
            <button class="sentinel-close" onclick="document.getElementById('sentinel-safety-indicator').remove()">×</button>
        </div>
    `;
    
    safetyIndicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: ${bgColor};
        border: 2px solid ${borderColor};
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        color: white;
        animation: slideIn 0.3s ease-out;
        backdrop-filter: blur(10px);
    `;
    
    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .sentinel-indicator-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .sentinel-icon {
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .sentinel-icon svg {
            width: 24px;
            height: 24px;
            color: ${iconColor};
        }
        
        .sentinel-info {
            flex: 1;
        }
        
        .sentinel-title {
            font-size: 12px;
            font-weight: 600;
            opacity: 0.8;
            margin-bottom: 2px;
        }
        
        .sentinel-risk {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        
        .sentinel-score {
            font-size: 12px;
            opacity: 0.8;
        }
        
        .sentinel-close {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        .sentinel-close:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(safetyIndicator);
    
    // Auto-hide after 10 seconds if not dangerous
    if (!isDangerous) {
        setTimeout(() => {
            if (safetyIndicator && safetyIndicator.parentNode) {
                safetyIndicator.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => hideSafetyIndicator(), 300);
            }
        }, 10000);
    }
}

// Hide safety indicator
function hideSafetyIndicator() {
    if (safetyIndicator && safetyIndicator.parentNode) {
        safetyIndicator.remove();
        safetyIndicator = null;
    }
}

// Monitor URL changes (for SPA applications)
let lastUrl = location.href;
new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        currentUrl = url;
        console.log('URL changed to:', currentUrl);
        // Optionally trigger auto-scan on URL change
    }
}).observe(document, { subtree: true, childList: true });