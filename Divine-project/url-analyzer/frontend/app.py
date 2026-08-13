"""Streamlit dashboard for the URL risk analysis API - Premium UI/UX Version."""

import os
from urllib.parse import urlparse
import time

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


API_BASE_URL = os.getenv("URL_ANALYZER_API_URL", "http://127.0.0.1:8000/api").rstrip("/")
REQUEST_TIMEOUT = 15


st.set_page_config(
    page_title="Sentinel | URL Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_premium_styles() -> None:
    """Apply premium UI/UX styling with modern design principles."""
    st.markdown(
        """
        <style>
            /* Premium Color Palette */
            :root {
                --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                --danger-gradient: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                --bg-dark: #0a0a0f;
                --bg-card: #12121a;
                --bg-card-hover: #1a1a25;
                --bg-input: #1e1e2a;
                --text-primary: #ffffff;
                --text-secondary: #a0a0b8;
                --text-muted: #6b6b80;
                --border-color: #2a2a3a;
                --border-hover: #3a3a4a;
                --accent: #667eea;
                --accent-light: #8b9ff7;
                --success: #00d4aa;
                --warning: #ffa726;
                --danger: #ff5252;
                --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
                --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
                --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.6);
                --glass: rgba(255, 255, 255, 0.05);
                --glass-hover: rgba(255, 255, 255, 0.08);
            }

            /* Global Styles */
            .stApp {
                background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%);
                color: var(--text-primary);
                min-height: 100vh;
            }

            .block-container {
                max-width: 1400px;
                padding-top: 2rem;
                padding-bottom: 4rem;
            }

            /* Hide default Streamlit elements */
            #MainMenu, footer, header { visibility: hidden; }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: var(--bg-dark);
            }
            ::-webkit-scrollbar-thumb {
                background: var(--border-color);
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: var(--accent);
            }

            /* Premium Card Styles */
            .premium-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                padding: 1.5rem;
                box-shadow: var(--shadow-md);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(10px);
            }

            .premium-card:hover {
                border-color: var(--border-hover);
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }

            /* Header Styles */
            .header-section {
                text-align: center;
                margin-bottom: 3rem;
                animation: fadeInDown 0.8s ease-out;
            }

            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .logo-container {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 1rem;
                margin-bottom: 1.5rem;
            }

            .logo-icon {
                width: 60px;
                height: 60px;
                background: var(--primary-gradient);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            .app-title {
                font-size: 3rem;
                font-weight: 800;
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                letter-spacing: -0.02em;
            }

            .app-subtitle {
                font-size: 1.2rem;
                color: var(--text-secondary);
                margin-top: 0.5rem;
                font-weight: 400;
            }

            /* Hero Section */
            .hero-section {
                text-align: center;
                margin-bottom: 3rem;
                padding: 2rem;
            }

            .hero-title {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-description {
                font-size: 1.1rem;
                color: var(--text-secondary);
                max-width: 600px;
                margin: 0 auto 2rem;
                line-height: 1.6;
            }

            /* Input Styles */
            .input-container {
                display: flex;
                gap: 1rem;
                max-width: 800px;
                margin: 0 auto;
            }

            div[data-testid="stTextInput"] input {
                background: var(--bg-input);
                border: 2px solid var(--border-color);
                border-radius: 12px;
                color: var(--text-primary);
                font-size: 1rem;
                padding: 1rem 1.5rem;
                transition: all 0.3s ease;
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: var(--accent);
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
                outline: none;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: var(--text-muted);
            }

            /* Button Styles */
            .premium-button {
                background: var(--primary-gradient);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                font-size: 1rem;
                padding: 1rem 2rem;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .premium-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            .premium-button:active {
                transform: translateY(0);
            }

            div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
                background: var(--primary-gradient);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                font-size: 1rem;
                padding: 1rem 2rem;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }

            div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            /* Result Card Styles */
            .result-container {
                animation: slideInUp 0.6s ease-out;
            }

            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .risk-card {
                background: var(--bg-card);
                border: 2px solid var(--border-color);
                border-radius: 24px;
                padding: 2rem;
                margin: 2rem 0;
                box-shadow: var(--shadow-lg);
                backdrop-filter: blur(20px);
            }

            .risk-card.safe {
                border-color: var(--success);
                box-shadow: 0 8px 32px rgba(0, 212, 170, 0.3);
            }

            .risk-card.medium {
                border-color: var(--warning);
                box-shadow: 0 8px 32px rgba(255, 167, 38, 0.3);
            }

            .risk-card.high {
                border-color: var(--danger);
                box-shadow: 0 8px 32px rgba(255, 82, 82, 0.3);
                animation: shake 0.5s ease-in-out;
            }

            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }

            .risk-header {
                display: flex;
                align-items: center;
                gap: 1.5rem;
                margin-bottom: 1.5rem;
            }

            .risk-icon {
                width: 80px;
                height: 80px;
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
            }

            .risk-icon.safe {
                background: var(--success-gradient);
            }

            .risk-icon.medium {
                background: var(--warning-gradient);
            }

            .risk-icon.high {
                background: var(--danger-gradient);
            }

            .risk-info h2 {
                margin: 0 0 0.5rem 0;
                font-size: 2rem;
                font-weight: 800;
            }

            .risk-info p {
                margin: 0;
                color: var(--text-secondary);
                font-size: 1.1rem;
            }

            .risk-score-display {
                font-size: 4rem;
                font-weight: 900;
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 1.5rem 0;
            }

            /* Progress Bar */
            .progress-container {
                height: 12px;
                background: var(--bg-input);
                border-radius: 6px;
                overflow: hidden;
                margin: 1.5rem 0;
            }

            .progress-bar {
                height: 100%;
                border-radius: 6px;
                transition: width 1s ease-out;
                background: var(--primary-gradient);
            }

            .progress-bar.safe {
                background: var(--success-gradient);
            }

            .progress-bar.medium {
                background: var(--warning-gradient);
            }

            .progress-bar.high {
                background: var(--danger-gradient);
            }

            /* Stats Cards */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin: 2rem 0;
            }

            .stat-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
            }

            .stat-card:hover {
                border-color: var(--accent);
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
            }

            .stat-value {
                font-size: 2.5rem;
                font-weight: 800;
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                font-size: 0.9rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            /* History Table */
            .history-section {
                margin-top: 3rem;
            }

            .section-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
            }

            .section-title {
                font-size: 1.5rem;
                font-weight: 700;
                margin: 0;
            }

            [data-testid="stDataFrame"] {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                overflow: hidden;
            }

            /* Sidebar Styles */
            .sidebar-content {
                padding: 1rem;
            }

            .sidebar-title {
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 1rem;
                color: var(--text-primary);
            }

            .sidebar-section {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
            }

            /* Loading Animation */
            .loading-container {
                text-align: center;
                padding: 3rem;
            }

            .loading-spinner {
                width: 60px;
                height: 60px;
                border: 4px solid var(--border-color);
                border-top-color: var(--accent);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            /* Metrics */
            div[data-testid="stMetric"] {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: var(--shadow-sm);
            }

            div[data-testid="stMetricLabel"] {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }

            div[data-testid="stMetricValue"] {
                color: var(--text-primary);
                font-size: 2rem;
                font-weight: 700;
            }

            /* Expander */
            .streamlit-expanderHeader {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
                margin-top: 1rem;
            }

            /* Info Messages */
            .stAlert {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .app-title {
                    font-size: 2rem;
                }
                
                .hero-title {
                    font-size: 1.8rem;
                }
                
                .input-container {
                    flex-direction: column;
                }
                
                .risk-header {
                    flex-direction: column;
                    text-align: center;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }

            /* Advanced Features Grid */
            .features-grid-advanced {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1.5rem;
                margin-top: 1.5rem;
            }

            .feature-item-advanced {
                background: var(--glass);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 1.5rem;
                transition: all 0.3s ease;
            }

            .feature-item-advanced:hover {
                background: var(--glass-hover);
                border-color: var(--accent);
                transform: translateY(-4px);
                box-shadow: var(--shadow-md);
            }

            .feature-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .feature-label-advanced {
                font-size: 0.9rem;
                color: var(--text-secondary);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .feature-value-advanced {
                font-size: 1.3rem;
                font-weight: 700;
                color: var(--text-primary);
            }

            .feature-progress-container {
                height: 8px;
                background: var(--bg-input);
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 0.75rem;
            }

            .feature-progress-bar {
                height: 100%;
                border-radius: 4px;
                transition: width 1s ease-out;
                animation: progressSlide 1s ease-out;
            }

            @keyframes progressSlide {
                from {
                    width: 0%;
                }
            }

            .feature-risk-indicator {
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                display: inline-block;
                text-align: center;
            }

            .feature-risk-indicator.safe {
                background: rgba(0, 212, 170, 0.2);
                color: var(--success);
                border: 1px solid var(--success);
            }

            .feature-risk-indicator.warning {
                background: rgba(255, 167, 38, 0.2);
                color: var(--warning);
                border: 1px solid var(--warning);
            }

            .feature-risk-indicator.danger {
                background: rgba(255, 82, 82, 0.2);
                color: var(--danger);
                border: 1px solid var(--danger);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def normalise_url(value: str) -> str:
    value = value.strip()
    if value and "://" not in value:
        value = f"https://{value}"
    return value


def is_valid_url(value: str) -> bool:
    candidate = (value or "").strip()
    if not candidate or len(candidate) > 2048 or any(ch.isspace() for ch in candidate):
        return False

    parsed = urlparse(candidate)
    hostname = parsed.hostname
    return parsed.scheme in {"http", "https"} and bool(hostname)


def api_request(method: str, endpoint: str, **kwargs):
    return requests.request(method, f"{API_BASE_URL}/{endpoint}", timeout=REQUEST_TIMEOUT, **kwargs)


def create_risk_gauge(score: float, risk_level: str) -> go.Figure:
    """Create a beautiful gauge chart for risk score."""
    colors = {
        "SAFE": "#00d4aa",
        "MEDIUM RISK": "#ffa726", 
        "HIGH RISK": "#ff5252"
    }
    
    color = colors.get(risk_level, "#667eea")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score", 'font': {'size': 24, 'color': '#ffffff'}},
        number = {'font': {'size': 48, 'color': color}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2a2a3a"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#2a2a3a",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(0, 212, 170, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(255, 167, 38, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(255, 82, 82, 0.3)'},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_features_radar(features: dict) -> go.Figure:
    """Create a radar chart for feature analysis."""
    # Select key features for visualization
    key_features = {
        'URL Length': features.get('url_length', 0) / 100,  # Normalized
        'Domain Length': features.get('domain_length', 0) / 50,
        'Path Length': features.get('path_length', 0) / 100,
        'Digit Count': features.get('digit_count', 0) / 20,
        'Special Chars': features.get('at_count', 0) + features.get('equal_count', 0),
        'Subdomains': features.get('subdomain_count', 0) / 5,
    }
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(key_features.values()),
        theta=list(key_features.keys()),
        fill='toself',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='#2a2a3a',
                linecolor='#2a2a3a'
            ),
            angularaxis=dict(
                gridcolor='#2a2a3a',
                linecolor='#2a2a3a'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig


def get_feature_risk_level(label: str, value) -> tuple[str, str, int]:
    """Determine risk level, color, and percentage for a feature."""
    # Convert value to numeric if possible
    try:
        if isinstance(value, str):
            if value.lower() in ['yes', 'true', '1']:
                numeric_value = 1
            elif value.lower() in ['no', 'false', '0']:
                numeric_value = 0
            else:
                numeric_value = 0
        else:
            numeric_value = float(value)
    except (ValueError, TypeError):
        numeric_value = 0
    
    # Determine risk based on feature type
    if label == "HTTPS Enabled":
        if numeric_value == 1:
            return "safe", "#00d4aa", 100  # Good
        else:
            return "danger", "#ff5252", 0  # Bad
    
    elif label == "IP Address":
        if numeric_value == 1:
            return "danger", "#ff5252", 100  # Bad
        else:
            return "safe", "#00d4aa", 100  # Good
    
    elif label == "Suspicious Keywords":
        if numeric_value == 0:
            return "safe", "#00d4aa", 100  # Good
        elif numeric_value <= 2:
            return "warning", "#ffa726", 50  # Medium
        else:
            return "danger", "#ff5252", 100  # Bad
    
    elif label == "Suspicious TLD":
        if numeric_value == 0:
            return "safe", "#00d4aa", 100  # Good
        else:
            return "danger", "#ff5252", 100  # Bad
    
    elif label == "Subdomains":
        if numeric_value <= 1:
            return "safe", "#00d4aa", 100  # Good
        elif numeric_value <= 3:
            return "warning", "#ffa726", 50  # Medium
        else:
            return "danger", "#ff5252", 100  # Bad
    
    elif label == "URL Length":
        if numeric_value <= 50:
            return "safe", "#00d4aa", 100  # Good
        elif numeric_value <= 100:
            return "warning", "#ffa726", 50  # Medium
        else:
            return "danger", "#ff5252", 100  # Bad
    
    elif label == "Special Characters":
        if numeric_value == 0:
            return "safe", "#00d4aa", 100  # Good
        elif numeric_value <= 2:
            return "warning", "#ffa726", 50  # Medium
        else:
            return "danger", "#ff5252", 100  # Bad
    
    elif label == "Digits":
        if numeric_value <= 5:
            return "safe", "#00d4aa", 100  # Good
        elif numeric_value <= 10:
            return "warning", "#ffa726", 50  # Medium
        else:
            return "danger", "#ff5252", 100  # Bad
    
    else:
        return "safe", "#00d4aa", 100  # Default safe


def format_time(value) -> str:
    try:
        return pd.to_datetime(value).strftime("%d %b %Y, %H:%M")
    except (TypeError, ValueError):
        return str(value or "-")


# Initialize session state
if "result" not in st.session_state:
    st.session_state.result = None
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "threats_detected" not in st.session_state:
    st.session_state.threats_detected = 0
if "safe_sites" not in st.session_state:
    st.session_state.safe_sites = 0


# Inject premium styles
inject_premium_styles()


# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">🛡️ Sentinel</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-secondary); margin-bottom: 1rem;">URL Risk Intelligence</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Statistics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Scans", st.session_state.total_scans)
    with col2:
        st.metric("Threats", st.session_state.threats_detected)
    
    st.metric("Safe Sites", st.session_state.safe_sites)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Settings</div>', unsafe_allow_html=True)
    
    api_url = st.text_input("API URL", value=API_BASE_URL, key="api_url_input")
    if api_url != API_BASE_URL:
        os.environ["URL_ANALYZER_API_URL"] = api_url
    
    auto_scan = st.checkbox("Auto-scan on page load", value=True)
    show_notifications = st.checkbox("Show notifications", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Main content
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.markdown('<div class="logo-icon">🛡️</div>', unsafe_allow_html=True)
st.markdown('<div>', unsafe_allow_html=True)
st.markdown('<h1 class="app-title">SENTINEL</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Advanced URL Risk Intelligence</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<h2 class="hero-title">Know Where Links Lead Before You Trust Them</h2>', unsafe_allow_html=True)
st.markdown('<p class="hero-description">Analyze web addresses against our advanced machine-learning risk model. Get instant threat detection with beautiful visualizations and detailed insights.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# URL Input Form
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form("scan_form", clear_on_submit=False):
    input_col, button_col = st.columns([4, 1])
    with input_col:
        submitted_url = st.text_input(
            "Enter URL to analyze",
            placeholder="https://example.com/account",
            label_visibility="collapsed",
        )
    with button_col:
        scan_clicked = st.form_submit_button("🔍 Scan", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Process URL scan
if scan_clicked:
    target_url = normalise_url(submitted_url)
    if not target_url:
        st.warning("⚠️ Please enter a web address to start a scan.")
    elif not is_valid_url(target_url):
        st.warning("⚠️ Please enter a valid HTTP or HTTPS URL.")
    else:
        with st.spinner("🔍 Analyzing URL patterns..."):
            try:
                response = api_request("POST", "analyze/", json={"url": target_url})
                if response.ok:
                    result = response.json()
                    st.session_state.result = result
                    
                    # Update statistics
                    st.session_state.total_scans += 1
                    if result.get("prediction") == 1:
                        st.session_state.threats_detected += 1
                    else:
                        st.session_state.safe_sites += 1
                    
                    # Add to history
                    st.session_state.scan_history.insert(0, {
                        "url": result.get("url"),
                        "risk_level": result.get("risk_level"),
                        "risk_score": result.get("risk_score"),
                        "scanned_at": result.get("scanned_at")
                    })
                    
                    # Keep only last 50 scans
                    st.session_state.scan_history = st.session_state.scan_history[:50]
                    
                    time.sleep(0.5)  # Small delay for animation effect
                else:
                    detail = response.json().get("error", "The analysis service rejected this request.")
                    st.error(f"❌ Could not analyze the URL: {detail}")
            except requests.RequestException:
                st.error("❌ The analysis service is unavailable. Please start the Django backend and try again.")

# Display results
result = st.session_state.result
if result:
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    risk_level = result.get("risk_level", "UNKNOWN")
    score = float(result.get("risk_score", 0))
    
    # Risk card
    risk_class = risk_level.lower().replace(" ", "-")
    risk_icon_emoji = "✅" if risk_level == "SAFE" else "⚠️" if risk_level == "MEDIUM RISK" else "🚨"
    
    st.markdown(f'<div class="risk-card {risk_class}">', unsafe_allow_html=True)
    
    # Risk header
    st.markdown('<div class="risk-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="risk-icon {risk_class}">{risk_icon_emoji}</div>', unsafe_allow_html=True)
    st.markdown('<div class="risk-info">', unsafe_allow_html=True)
    st.markdown(f'<h2>{risk_level}</h2>', unsafe_allow_html=True)
    
    guidance = {
        "SAFE": "No major risk signals detected. This URL appears to be safe.",
        "MEDIUM RISK": "Suspicious signals found. Proceed with caution and verify independently.",
        "HIGH RISK": "High risk detected! Avoid opening this link or entering any details."
    }
    st.markdown(f'<p>{guidance.get(risk_level, "Unknown risk level")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk score display
    st.markdown(f'<div class="risk-score-display">{score:.1f}%</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar {risk_class}" style="width: {score}%"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Risk Analysis</h3>', unsafe_allow_html=True)
        fig_gauge = create_risk_gauge(score, risk_level)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Feature Analysis</h3>', unsafe_allow_html=True)
        features = result.get("features", {})
        fig_radar = create_features_radar(features)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature details with color-coded progress bars
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 0;">Detailed Analysis</h3>', unsafe_allow_html=True)
    
    features = result.get("features", {})
    important_features = [
        ("HTTPS Enabled", "Yes" if features.get("uses_https") else "No"),
        ("IP Address", "Yes" if features.get("has_ip") else "No"),
        ("Suspicious Keywords", features.get("suspicious_keyword_count", 0)),
        ("Suspicious TLD", "Yes" if features.get("suspicious_tld") else "No"),
        ("Subdomains", features.get("subdomain_count", 0)),
        ("URL Length", features.get("url_length", 0)),
        ("Special Characters", features.get("at_count", 0) + features.get("equal_count", 0)),
        ("Digits", features.get("digit_count", 0)),
    ]
    
    st.markdown('<div class="features-grid-advanced">', unsafe_allow_html=True)
    for label, value in important_features:
        risk_level, color, percentage = get_feature_risk_level(label, value)
        
        st.markdown(f'<div class="feature-item-advanced">', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-header">', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-label-advanced">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-value-advanced" style="color: {color}">{value}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress bar
        st.markdown(f'<div class="feature-progress-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-progress-bar" style="width: {percentage}%; background: {color};"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Risk indicator
        risk_label = "SAFE" if risk_level == "safe" else "WARNING" if risk_level == "warning" else "DANGER"
        st.markdown(f'<div class="feature-risk-indicator {risk_level}">{risk_label}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Decision source
    decision_source = result.get("decision_source", "unknown")
    source_map = {
        "local_ml": "Machine Learning Model",
        "local_ml+whitelist": "ML Model + Domain Whitelist",
        "local_ml+heuristic": "ML Model + Heuristic Analysis",
        "local_ml+reputation": "ML Model + Reputation Database"
    }
    st.markdown(f'<p style="color: var(--text-secondary); margin-top: 1rem;"><strong>Analysis Method:</strong> {source_map.get(decision_source, decision_source)}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# History section
st.markdown('<div class="history-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Recent Scan Activity</h2>', unsafe_allow_html=True)

clear_col = st.columns([1])[0]
with clear_col:
    clear_history = st.button("🗑️ Clear History", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if clear_history:
    try:
        response = api_request("DELETE", "clear-history/")
        if response.ok:
            st.session_state.result = None
            st.session_state.scan_history = []
            st.success("✅ Scan history cleared successfully.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ The server could not clear the history.")
    except requests.RequestException:
        st.error("❌ The analysis service is unavailable.")

# Display history
if st.session_state.scan_history:
    history_df = pd.DataFrame(st.session_state.scan_history)
    history_df['Scanned'] = history_df['scanned_at'].apply(format_time)
    # Use the actual column names from the data
    history_df = history_df[['url', 'risk_level', 'risk_score', 'Scanned']]
    history_df.columns = ['URL', 'Risk Level', 'Risk Score', 'Scanned']
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.info("ℹ️ No scans yet. Your completed analyses will appear here.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div style="text-align: center; margin-top: 3rem; color: var(--text-muted);">', unsafe_allow_html=True)
st.markdown('<p>Built with ❤️ using Streamlit, Django, and Machine Learning</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)