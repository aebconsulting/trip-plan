"""
Fix menu z-index stacking issue in create_html.py.

Changes:
1. .menu-backdrop z-index: 9998 -> 10000
2. .menu-panel z-index: 9999 -> 10001
3. panel.style.top offset: +4 -> +6
"""

import re

filepath = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Change 1: menu-backdrop z-index 9998 -> 10000
# Target the specific block: .menu-backdrop { ... z-index: 9998; ... }
old1 = """.menu-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.25);
    z-index: 9998;"""

new1 = """.menu-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.25);
    z-index: 10000;"""

if old1 in content:
    content = content.replace(old1, new1, 1)
    print("[OK] Change 1: menu-backdrop z-index 9998 -> 10000")
else:
    print("[SKIP] Change 1: pattern not found for menu-backdrop z-index")

# Change 2: menu-panel z-index 9999 -> 10001
old2 = """    z-index: 9999;
    border: 1px solid var(--border);
    padding: 0;
    animation: menuFadeIn 0.2s cubic-bezier(.4,0,.2,1);"""

new2 = """    z-index: 10001;
    border: 1px solid var(--border);
    padding: 0;
    animation: menuFadeIn 0.2s cubic-bezier(.4,0,.2,1);"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("[OK] Change 2: menu-panel z-index 9999 -> 10001")
else:
    print("[SKIP] Change 2: pattern not found for menu-panel z-index")

# Change 3: panel.style.top offset 4 -> 6
old3 = 'panel.style.top = (btnRect.bottom + 4) + "px";'
new3 = 'panel.style.top = (btnRect.bottom + 6) + "px";'

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("[OK] Change 3: panel.style.top offset 4 -> 6")
else:
    print("[SKIP] Change 3: pattern not found for panel.style.top")

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("\nAll changes written to create_html.py successfully.")
else:
    print("\nNo changes were made.")
