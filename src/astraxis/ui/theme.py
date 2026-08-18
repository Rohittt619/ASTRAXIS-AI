"""
ASTRAXIS-AI Glassmorphism Custom CSS Theme Injector.

Key Concept — Streamlit CSS Styling:
    Streamlit allows custom CSS injection via `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
    We build a dark glassmorphism cybersecurity theme using linear gradients, backdrop blurs,
    glowing neon borders (#00F0FF / #FF007A), and custom typography.
"""
import streamlit as st

GLASS_THEME_CSS = """
<style>
/* Modern Cyberpunk / Glassmorphism Palette */
:root {
    --bg-dark: #0A0E17;
    --card-bg: rgba(16, 24, 40, 0.75);
    --border-glow: rgba(0, 240, 255, 0.3);
    --accent-cyan: #00F0FF;
    --accent-magenta: #FF007A;
    --accent-green: #00FF66;
    --text-primary: #F0F4F8;
    --text-muted: #8A99AD;
}

/* Global Container Dark Background */
.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(at 0% 0%, rgba(0, 240, 255, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(255, 0, 122, 0.08) 0px, transparent 50%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Glassmorphism Cards */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease-in-out;
}

.glass-card:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 8px 32px 0 rgba(0, 240, 255, 0.2);
}

/* Cyber Title Styling */
.cyber-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00F0FF, #FF007A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
    letter-spacing: -0.5px;
}

/* Metric Display Cards */
.metric-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 15px;
    text-align: center;
}

.metric-val {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent-cyan);
}

.metric-lbl {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Status Badges */
.badge-critical {
    background: rgba(255, 0, 122, 0.2);
    color: #FF007A;
    border: 1px solid #FF007A;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
}

.badge-success {
    background: rgba(0, 255, 102, 0.2);
    color: #00FF66;
    border: 1px solid #00FF66;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
"""


def inject_glass_theme():
    """Inject custom CSS rules into Streamlit app head."""
    st.markdown(GLASS_THEME_CSS, unsafe_allow_html=True)
