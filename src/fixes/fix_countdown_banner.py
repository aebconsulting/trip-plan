#!/usr/bin/env python3
"""Move countdown from hero to a sticky banner below the nav bar."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove countdown div from inside the hero
code = code.replace(
    '  <div class="countdown-badge" id="trip-countdown"></div>\n</div>\n\n{html_body}',
    '</div>\n\n{html_body}'
)

# 2. Add the countdown banner HTML right after the nav-bar closing </div>
# Find the nav-bar section end (after day 12 link, before hero)
old_nav_end = '''  <a href="#day-12">12</a>
</div>

<div class="hero">'''

new_nav_end = '''  <a href="#day-12">12</a>
</div>

<div class="countdown-banner" id="trip-countdown"></div>

<div class="hero">'''

code = code.replace(old_nav_end, new_nav_end)

# 3. Replace old countdown CSS with new banner CSS
old_css = """  .countdown-badge {{
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
  }}
  .countdown-badge .count-num {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 1.1em;
    color: #fde68a;
  }}
  .countdown-badge.trip-active .count-num {{
    color: #86efac;
  }}
  .countdown-badge.trip-over {{
    opacity: 0.6;
  }}"""

new_css = """  .countdown-banner {{
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
  }}
  .countdown-banner .count-num {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.2em;
    color: #fbbf24;
  }}
  .countdown-banner.trip-active {{
    background: linear-gradient(135deg, #14532d, #166534);
  }}
  .countdown-banner.trip-active .count-num {{
    color: #4ade80;
  }}
  .countdown-banner.trip-over {{
    background: linear-gradient(135deg, #44403c, #57534e);
    font-size: 0.95em;
  }}"""

code = code.replace(old_css, new_css)

# 4. Update JS references from countdown-badge to countdown-banner
code = code.replace(
    "el.className = 'countdown-badge trip-active';",
    "el.className = 'countdown-banner trip-active';"
)
code = code.replace(
    "el.className = 'countdown-badge trip-over';",
    "el.className = 'countdown-banner trip-over';"
)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - countdown is now a sticky banner below the nav bar")
