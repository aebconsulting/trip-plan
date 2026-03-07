"""
fix_nav_menu.py
Modifies create_html.py with 5 nav-bar / menu related changes:
  1. .nav-bar CSS: single-line scroll -> wrapping flexbox
  2. .nav-group CSS: inline -> flexbox
  3. Nav-bar HTML: move menu button before day links
  4. .menu-panel CSS: right -> left positioning
  5. Mobile @media .nav-bar a: adjust padding + add .menu-btn rule
"""

import sys

FILE = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

original = content  # keep a copy for final verification

# -- Change 1: .nav-bar CSS ---------------------------------------------------
old_1 = """\
  .nav-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(246,241,233,0.88);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    padding: 10px 0;
    border-bottom: 2px solid var(--border);
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }}
  .nav-bar::-webkit-scrollbar {{ display: none; }}"""

new_1 = """\
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
  }}"""

if old_1 in content:
    content = content.replace(old_1, new_1, 1)
    print("Change 1 applied: .nav-bar CSS updated to wrapping flexbox layout.")
else:
    print("ERROR: Change 1 - could not find .nav-bar CSS block!")
    sys.exit(1)

# -- Change 2: .nav-group CSS -------------------------------------------------
old_2 = """\
  .nav-group {{ display: inline; }}
  .nav-group::before {{
    content: '';
    display: inline-block;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--terracotta);
    vertical-align: middle;
    margin: 0 6px;
  }}
  .nav-group:first-child::before {{ display: none; }}"""

new_2 = """\
  .nav-group {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 3px;
  }}"""

if old_2 in content:
    content = content.replace(old_2, new_2, 1)
    print("Change 2 applied: .nav-group CSS updated to flexbox.")
else:
    print("ERROR: Change 2 - could not find .nav-group CSS block!")
    sys.exit(1)

# -- Change 3: Nav-bar HTML ---------------------------------------------------
old_3 = """\
<div class="nav-bar" id="top">
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
  <span class="nav-group">
    <button class="menu-btn" id="mainMenuBtn" aria-label="Menu">\u2630 Menu</button>
  </span>
</div>"""

new_3 = """\
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

if old_3 in content:
    content = content.replace(old_3, new_3, 1)
    print("Change 3 applied: Menu button moved before day links in HTML.")
else:
    print("ERROR: Change 3 - could not find nav-bar HTML block!")
    sys.exit(1)

# -- Change 4: .menu-panel CSS ------------------------------------------------
old_4 = """\
  .menu-panel {{
    position: fixed;
    top: 52px;
    right: 12px;
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

new_4 = """\
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

if old_4 in content:
    content = content.replace(old_4, new_4, 1)
    print("Change 4 applied: .menu-panel positioned from left instead of right.")
else:
    print("ERROR: Change 4 - could not find .menu-panel CSS block!")
    sys.exit(1)

# -- Change 5: Mobile @media .nav-bar a ---------------------------------------
old_5 = "    .nav-bar a {{ font-size: 0.72em; padding: 4px 10px; }}"

new_5 = "    .nav-bar a {{ font-size: 0.72em; padding: 4px 8px; }}\n    .menu-btn {{ font-size: 0.72em; padding: 4px 10px; }}"

if old_5 in content:
    content = content.replace(old_5, new_5, 1)
    print("Change 5 applied: Mobile .nav-bar a padding adjusted + .menu-btn rule added.")
else:
    print("ERROR: Change 5 - could not find mobile .nav-bar a rule!")
    sys.exit(1)

# -- Write file and verify ----------------------------------------------------
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\nAll 5 changes written to create_html.py successfully.")

# Final verification: re-read and confirm none of the old patterns remain
with open(FILE, "r", encoding="utf-8") as f:
    verify = f.read()

errors = []
if old_1 in verify:
    errors.append("Change 1 (.nav-bar CSS) did not persist")
if old_2 in verify:
    errors.append("Change 2 (.nav-group CSS) did not persist")
if old_3 in verify:
    errors.append("Change 3 (nav-bar HTML) did not persist")
# For change 4, check specifically in .menu-panel context
idx = verify.find(".menu-panel")
if idx != -1 and "right: 12px;" in verify[idx:idx+500]:
    errors.append("Change 4 (.menu-panel right->left) did not persist")
if old_5 in verify:
    errors.append("Change 5 (mobile .nav-bar a) did not persist")

if errors:
    print("\nVERIFICATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("Verification passed: all old patterns are gone, new patterns are in place.")
