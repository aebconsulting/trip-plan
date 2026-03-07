#!/usr/bin/env python3
"""Fix scroll offset to account for nav + banner, and remove gap between them."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add scroll-padding-top to html to account for nav (~44px) + banner (~42px)
code = code.replace(
    "  html {{ scroll-behavior: smooth; }}",
    "  html {{ scroll-behavior: smooth; scroll-padding-top: 90px; }}"
)

# 2. Remove the gap between nav-bar and countdown banner
# The banner border-bottom on nav-bar creates visual separation already
# Make the banner flush with nav by removing nav-bar's border-bottom
# and adding margin:0 to banner
code = code.replace(
    """  .countdown-banner {{
    position: sticky;
    top: 44px;
    z-index: 999;
    text-align: center;
    padding: 10px 20px;
    background: linear-gradient(135deg, #1a3a2a, #2d5a3d);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 1.05em;
    font-weight: 500;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }}""",
    """  .countdown-banner {{
    position: sticky;
    top: 44px;
    z-index: 999;
    text-align: center;
    padding: 10px 20px;
    margin: 0;
    background: linear-gradient(135deg, #1a3a2a, #2d5a3d);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 1.05em;
    font-weight: 500;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }}"""
)

# 3. Fix the JS menu scroll offset to include banner height
code = code.replace(
    "var navH = document.querySelector('.nav-bar') ? document.querySelector('.nav-bar').offsetHeight : 40;",
    "var navH = (document.querySelector('.nav-bar') ? document.querySelector('.nav-bar').offsetHeight : 40) + (document.querySelector('.countdown-banner') ? document.querySelector('.countdown-banner').offsetHeight : 0);"
)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - fixed scroll offset and nav/banner gap")
