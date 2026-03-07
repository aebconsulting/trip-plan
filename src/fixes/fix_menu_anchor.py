"""
Fix script: Anchor the menu panel to the hamburger button instead of centering it.

Changes:
1. CSS: Remove fixed top/left/transform from .menu-panel (JS will set dynamically)
2. CSS animation: Remove translateX(-50%) from menuFadeIn keyframes
3. JS: After appendChild(panel), position the panel relative to the button
"""
import re

file_path = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- Change 1: CSS .menu-panel ---
old_css = """  .menu-panel {{
    position: fixed;
    top: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;"""

new_css = """  .menu-panel {{
    position: fixed;
    width: 260px;"""

assert old_css in content, "Change 1: Could not find .menu-panel CSS block!"
content = content.replace(old_css, new_css)
print("Change 1 applied: Removed top/left/transform from .menu-panel CSS")

# --- Change 2: CSS animation menuFadeIn ---
old_anim = """  @keyframes menuFadeIn {{
    from {{ opacity: 0; transform: translateX(-50%) translateY(-6px) scale(0.97); }}
    to {{ opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }}
  }}"""

new_anim = """  @keyframes menuFadeIn {{
    from {{ opacity: 0; transform: translateY(-6px) scale(0.97); }}
    to {{ opacity: 1; transform: translateY(0) scale(1); }}
  }}"""

assert old_anim in content, "Change 2: Could not find menuFadeIn keyframes!"
content = content.replace(old_anim, new_anim)
print("Change 2 applied: Removed translateX(-50%) from menuFadeIn keyframes")

# --- Change 3: JS positioning after appendChild ---
old_js = """      document.body.appendChild(panel);
    }}}});"""

new_js = """      document.body.appendChild(panel);
      var btnRect = menuBtn.getBoundingClientRect();
      panel.style.top = (btnRect.bottom + 4) + "px";
      panel.style.left = Math.max(8, btnRect.left) + "px";
    }}}});"""

assert old_js in content, "Change 3: Could not find appendChild(panel) + closing block!"
content = content.replace(old_js, new_js, 1)
print("Change 3 applied: Added dynamic positioning after appendChild(panel)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll 3 changes applied successfully to create_html.py")
