#!/usr/bin/env python3
"""Fix gap between nav bar and countdown banner."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove the nav-bar border-bottom (banner provides the edge now)
code = code.replace(
    "    border-bottom: 1.5px solid var(--border);\n    display: flex;\n    flex-wrap: wrap;\n    align-items: center;\n    justify-content: center;\n    gap: 5px;\n  }}",
    "    border-bottom: none;\n    display: flex;\n    flex-wrap: wrap;\n    align-items: center;\n    justify-content: center;\n    gap: 5px;\n  }}"
)

# 2. Fix banner: use JS-driven top instead of hardcoded 44px, and raise z-index to match nav
code = code.replace(
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
  }}""",
    """  .countdown-banner {{
    position: sticky;
    top: 44px;
    z-index: 99;
    text-align: center;
    padding: 10px 20px;
    margin: 0;
    background: linear-gradient(135deg, #1a3a2a, #2d5a3d);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    border-top: none;
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 1.05em;
    font-weight: 500;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }}"""
)

# 3. Add JS to dynamically set the banner top to match actual nav height
# Find the countdown JS block and add the top-sync logic
sync_js = """
  // Sync banner top position with actual nav height
  var nav = document.querySelector('.nav-bar');
  if (nav && el) {{
    function syncTop() {{
      el.style.top = nav.offsetHeight + 'px';
    }}
    syncTop();
    window.addEventListener('resize', syncTop);
  }}
"""

# Insert after the setInterval line in the countdown JS
code = code.replace(
    "  update();\n  setInterval(update, 60000);",
    "  update();\n  setInterval(update, 60000);\n" + sync_js
)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - fixed banner gap with dynamic top sync")
