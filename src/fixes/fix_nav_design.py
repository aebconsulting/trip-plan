"""
fix_nav_design.py
Modifies create_html.py with 4 nav-bar design replacements for a tight,
centered, elegant nav that works on all screen sizes.
"""

import sys

FILE = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

original = content  # keep a copy for final verification

# -- Change 1: Replace ALL nav-bar related CSS --

OLD_1 = """\
  .nav-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(246,241,233,0.88);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    padding: 8px 10px;
    border-bottom: 2px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px 2px;
  }}

  .nav-bar a {{
    display: inline-block;
    padding: 5px 14px;
    margin: 2px 3px;
    border-radius: 100px;
    background: var(--card-bg);
    color: var(--forest);
    font-family: 'Outfit', sans-serif;
    font-size: 0.78em;
    font-weight: 600;
    text-decoration: none;
    border: 1.5px solid var(--border);
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
    letter-spacing: 0.02em;
  }}
  .nav-bar a:hover, .nav-bar a:active {{
    background: var(--forest);
    color: var(--cream);
    border-color: var(--forest);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }}
  .nav-group {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 3px;
  }}

  /* Dropdown menu */
  .menu-btn {{
    display: inline-block;
    padding: 5px 14px;
    margin: 2px 3px;
    border-radius: 100px;
    background: var(--forest);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 0.78em;
    font-weight: 600;
    border: 1.5px solid var(--forest);
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
  }}
  .menu-btn:hover {{
    background: var(--forest-mid);
    border-color: var(--forest-mid);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }}"""

NEW_1 = """\
  .nav-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(246,241,233,0.92);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    padding: 6px 12px;
    border-bottom: 1.5px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 5px;
  }}

  .nav-bar a {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 11px;
    border-radius: 6px;
    background: transparent;
    color: var(--forest);
    font-family: 'Outfit', sans-serif;
    font-size: 0.74em;
    font-weight: 600;
    text-decoration: none;
    border: none;
    transition: all 0.2s ease;
    letter-spacing: 0.01em;
    white-space: nowrap;
  }}
  .nav-bar a:hover, .nav-bar a:active {{
    background: var(--forest);
    color: var(--cream);
    transform: none;
    box-shadow: none;
  }}
  .nav-group {{
    display: contents;
  }}

  /* Dropdown menu */
  .menu-btn {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    background: var(--forest);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 0.74em;
    font-weight: 600;
    border: none;
    cursor: pointer;
    letter-spacing: 0.01em;
    transition: all 0.2s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .menu-btn:hover {{
    background: var(--forest-mid);
    transform: none;
    box-shadow: none;
  }}"""

# -- Change 2: Replace the menu-panel CSS --

OLD_2 = """\
  .menu-panel {{
    position: fixed;
    top: 52px;
    left: 12px;
    min-width: 280px;
    max-width: 320px;
    max-height: 70vh;
    overflow-y: auto;
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15), 0 4px 12px rgba(0,0,0,0.08);
    z-index: 9999;
    border: 1px solid var(--border);
    padding: 6px 0;
    animation: menuFadeIn 0.2s ease-out;
  }}"""

NEW_2 = """\
  .menu-panel {{
    position: fixed;
    top: 42px;
    left: 12px;
    min-width: 260px;
    max-width: 300px;
    max-height: 75vh;
    overflow-y: auto;
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 10px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06);
    z-index: 9999;
    border: 1px solid rgba(0,0,0,0.08);
    padding: 4px 0;
    animation: menuFadeIn 0.15s ease-out;
  }}"""

# -- Change 3: Replace the 400px media query --

OLD_3 = """\
  @media (max-width: 400px) {{
    .hero h1 {{ font-size: 1.3em; }}
    .nav-bar a {{ font-size: 0.72em; padding: 4px 8px; }}
    .menu-btn {{ font-size: 0.72em; padding: 4px 10px; }}
    .day-header {{ flex-wrap: wrap; }}
  }}"""

NEW_3 = """\
  @media (max-width: 400px) {{
    .hero h1 {{ font-size: 1.3em; }}
    .nav-bar {{ padding: 5px 6px; gap: 3px; }}
    .nav-bar a {{ font-size: 0.68em; padding: 3px 8px; }}
    .menu-btn {{ font-size: 0.68em; padding: 3px 8px; }}
    .day-header {{ flex-wrap: wrap; }}
  }}"""

# -- Change 4: Replace the nav-bar HTML --

OLD_4 = """\
<div class="nav-bar" id="top">
  <button class="menu-btn" id="mainMenuBtn" aria-label="Menu">\u2630 Menu</button>
  <span class="nav-group">
    <a href="#day-1">Day 1</a>
    <a href="#day-2">Day 2</a>
    <a href="#day-3">Day 3</a>
    <a href="#day-4">Day 4</a>
    <a href="#day-5">Day 5</a>
    <a href="#day-6">Day 6</a>
    <a href="#day-7">Day 7</a>
    <a href="#day-8">Day 8</a>
    <a href="#day-9">Day 9</a>
    <a href="#day-10">Day 10</a>
    <a href="#day-11">Day 11</a>
    <a href="#day-12">Day 12</a>
  </span>
</div>"""

NEW_4 = """\
<div class="nav-bar" id="top">
  <button class="menu-btn" id="mainMenuBtn" aria-label="Menu">\u2630</button>
  <a href="#day-1">1</a>
  <a href="#day-2">2</a>
  <a href="#day-3">3</a>
  <a href="#day-4">4</a>
  <a href="#day-5">5</a>
  <a href="#day-6">6</a>
  <a href="#day-7">7</a>
  <a href="#day-8">8</a>
  <a href="#day-9">9</a>
  <a href="#day-10">10</a>
  <a href="#day-11">11</a>
  <a href="#day-12">12</a>
</div>"""

# -- Apply all replacements --

changes = [
    ("Change 1: Nav-bar + nav links + nav-group + menu-btn CSS", OLD_1, NEW_1),
    ("Change 2: Menu-panel CSS", OLD_2, NEW_2),
    ("Change 3: 400px media query", OLD_3, NEW_3),
    ("Change 4: Nav-bar HTML structure", OLD_4, NEW_4),
]

all_ok = True
for label, old, new in changes:
    if old in content:
        content = content.replace(old, new)
        print(f"[OK]   {label} -- replaced successfully.")
    else:
        print(f"[FAIL] {label} -- old text NOT found!")
        all_ok = False

if not all_ok:
    print("\nABORTING: One or more replacements failed. File was NOT modified.")
    sys.exit(1)

# Verify none of the old strings remain
for label, old, _ in changes:
    if old in content:
        print(f"[WARN] {label} -- old text still present after replacement!")
        all_ok = False

if not all_ok:
    print("\nABORTING: Verification failed. File was NOT modified.")
    sys.exit(1)

# Verify all new strings are present
for label, _, new in changes:
    if new not in content:
        print(f"[WARN] {label} -- new text NOT found after replacement!")
        all_ok = False

if not all_ok:
    print("\nABORTING: Post-replacement verification failed. File was NOT modified.")
    sys.exit(1)

# Write the modified file
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nAll 4 replacements applied and verified. File saved: {FILE}")
