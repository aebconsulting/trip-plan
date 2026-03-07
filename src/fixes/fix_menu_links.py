"""
Fix menu links in create_html.py to:
1. Prevent default anchor jump behavior
2. Open collapsed <details> accordion panels
3. Scroll smoothly to the section with nav-bar offset
"""
import re

file_path = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The old block (using exact f-string double braces from the file)
old_block = '''      menuItems.forEach(function(item) {{{{
        var a = document.createElement("a");
        a.href = item.href;
        a.textContent = item.label;
        a.addEventListener("click", function() {{{{
          closeMenu();
        }}}});
        panel.appendChild(a);
      }}}});'''

new_block = '''      menuItems.forEach(function(item) {{{{
        var a = document.createElement("a");
        a.href = item.href;
        a.textContent = item.label;
        a.addEventListener("click", function(e) {{{{
          e.preventDefault();
          closeMenu();
          var targetId = item.href.replace('#', '');
          var target = document.getElementById(targetId);
          if (target) {{{{
            if (target.tagName === 'DETAILS' && !target.hasAttribute('open')) {{{{
              target.setAttribute('open', '');
            }}}}
            setTimeout(function() {{{{
              var navH = document.querySelector('.nav-bar') ? document.querySelector('.nav-bar').offsetHeight : 40;
              var rect = target.getBoundingClientRect();
              window.scrollTo({{{{ top: window.scrollY + rect.top - navH - 8, behavior: 'smooth' }}}});
            }}}}, 50);
          }}}}
        }}}});
        panel.appendChild(a);
      }}}});'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Menu links block replaced in create_html.py")
else:
    print("ERROR: Could not find the target block in create_html.py")
    print("Searching for partial match...")
    if "menuItems.forEach" in content:
        idx = content.index("menuItems.forEach")
        print(f"Found menuItems.forEach at character {idx}")
        print("Context:")
        print(repr(content[idx:idx+300]))
    else:
        print("menuItems.forEach not found at all!")
