"""
Fix script: Change the menu panel CSS in create_html.py from
opening left-aligned to opening centered on desktop.

Two changes:
1. .menu-panel: replace left:10px with left:50% + transform:translateX(-50%)
2. @keyframes menuFadeIn: prepend translateX(-50%) to transform values
"""
import re

file_path = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- Change 1: Center the .menu-panel ---
old_menu_panel = """\
  .menu-panel {{
    position: fixed;
    top: 40px;
    left: 10px;
    width: 260px;"""

new_menu_panel = """\
  .menu-panel {{
    position: fixed;
    top: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;"""

if old_menu_panel in content:
    content = content.replace(old_menu_panel, new_menu_panel)
    print("[OK] Replaced .menu-panel positioning (left:10px -> left:50% + transform).")
else:
    print("[WARN] Could not find the original .menu-panel block. Already patched?")

# --- Change 2: Update @keyframes menuFadeIn to include translateX(-50%) ---
old_keyframes = """\
  @keyframes menuFadeIn {{
    from {{ opacity: 0; transform: translateY(-6px) scale(0.97); }}
    to {{ opacity: 1; transform: translateY(0) scale(1); }}
  }}"""

new_keyframes = """\
  @keyframes menuFadeIn {{
    from {{ opacity: 0; transform: translateX(-50%) translateY(-6px) scale(0.97); }}
    to {{ opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }}
  }}"""

if old_keyframes in content:
    content = content.replace(old_keyframes, new_keyframes)
    print("[OK] Updated @keyframes menuFadeIn with translateX(-50%).")
else:
    print("[WARN] Could not find the original @keyframes menuFadeIn block. Already patched?")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[DONE] create_html.py has been updated.")
