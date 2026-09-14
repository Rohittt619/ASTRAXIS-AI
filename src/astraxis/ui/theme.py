"""
ASTRAXIS-AI Glassmorphism Custom CSS Theme Injector.

Defines a futuristic cyberpunk dark theme with glowing neon accents,
glassmorphism backdrop blur cards, animated progress bars, and custom typography.
"""
import streamlit as st

GLASS_THEME_CSS = """
<style>
/* Modern Cyberpunk / Glassmorphism Palette */
:root {
    --bg-dark: #070A10;
    --card-bg: rgba(13, 20, 36, 0.75);
    --border-glow: rgba(0, 240, 255, 0.25);
    --accent-cyan: #00F0FF;
    --accent-magenta: #FF007A;
    --accent-green: #00FF66;
    --accent-gold: #FFB800;
    --text-primary: #F0F4F8;
    --text-muted: #8A99AD;
}

/* Global Container Dark Background */
.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 10% 10%, rgba(0, 240, 255, 0.12) 0px, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(255, 0, 122, 0.12) 0px, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(0, 255, 102, 0.05) 0px, transparent 60%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Glassmorphism Cards */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease-in-out;
}

.glass-card:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 10px 40px 0 rgba(0, 240, 255, 0.25);
}

/* Cyber Title Styling */
.cyber-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00F0FF, #FF007A, #00FF66);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -1px;
}

/* Metric Display Cards */
.metric-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.metric-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--accent-cyan);
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
}

.metric-lbl {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 4px;
}

/* Threat Badges */
.badge-critical {
    background: rgba(255, 0, 122, 0.2);
    color: #FF007A;
    border: 1px solid #FF007A;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 700;
    display: inline-block;
}

.badge-high {
    background: rgba(255, 184, 0, 0.2);
    color: #FFB800;
    border: 1px solid #FFB800;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 700;
    display: inline-block;
}

.badge-success {
    background: rgba(0, 255, 102, 0.2);
    color: #00FF66;
    border: 1px solid #00FF66;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 700;
    display: inline-block;
}

/* Custom Sample Button Badges */
.sample-cmd {
    background: rgba(0, 240, 255, 0.1);
    border: 1px solid rgba(0, 240, 255, 0.3);
    color: #00F0FF;
    border-radius: 6px;
    padding: 6px 12px;
    font-family: monospace;
    font-size: 0.85rem;
    margin-right: 8px;
    display: inline-block;
}
</style>
"""


def inject_glass_theme():
    """Inject custom CSS rules into Streamlit app head."""
    st.markdown(GLASS_THEME_CSS, unsafe_allow_html=True)
