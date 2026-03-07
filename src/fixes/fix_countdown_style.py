#!/usr/bin/env python3
"""Fix countdown badge layout - put it on its own line below route badge."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fix the CSS - make it display:block, centered, smaller/subtler
old_css = """  .countdown-badge {{
    display: inline-block;
    margin-top: 12px;
    padding: 8px 20px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
    font-weight: 500;
    letter-spacing: 0.3px;
    animation: pulse-glow 3s ease-in-out infinite;
  }}"""

new_css = """  .countdown-badge {{
    display: block;
    margin: 14px auto 0;
    padding: 0;
    background: none;
    border: none;
    color: rgba(255,255,255,0.7);
    font-family: 'Outfit', sans-serif;
    font-size: 0.82em;
    font-weight: 400;
    letter-spacing: 0.3px;
    position: relative;
    z-index: 1;
  }}"""

code = code.replace(old_css, new_css)

# 2. Simplify the count-num style 
old_num = """  .countdown-badge .count-num {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.15em;
    color: #fbbf24;
  }}"""

new_num = """  .countdown-badge .count-num {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 1.1em;
    color: #fde68a;
  }}"""

code = code.replace(old_num, new_num)

# 3. Simplify trip-active style
old_active = """  .countdown-badge.trip-active {{
    background: rgba(34,197,94,0.25);
    border-color: rgba(34,197,94,0.4);
  }}
  .countdown-badge.trip-active .count-num {{
    color: #4ade80;
  }}"""

new_active = """  .countdown-badge.trip-active .count-num {{
    color: #86efac;
  }}"""

code = code.replace(old_active, new_active)

# 4. Remove the pulse-glow animation (too flashy)
old_glow = """  @keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 8px rgba(251,191,36,0.15); }}
    50% {{ box-shadow: 0 0 16px rgba(251,191,36,0.3); }}
  }}"""

code = code.replace(old_glow, "")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - countdown is now a clean text line below the route badge")
