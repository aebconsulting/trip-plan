#!/usr/bin/env python3
"""Add target=_blank to all external links (static + dynamic)."""
import re

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# Find the closing </script> before </body> and inject a link handler right before it
# We'll add a small JS block that:
# 1. On DOMContentLoaded, sets target=_blank on all non-anchor links
# 2. Uses MutationObserver to catch dynamically added links (weather panels, road conditions)

js_snippet = r"""
// Open all external links in new tab
function openExternalLinksInNewTab(root) {{
  root.querySelectorAll('a[href]').forEach(function(a) {{
    var href = a.getAttribute('href');
    if (href && !href.startsWith('#')) {{
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'noopener noreferrer');
    }}
  }});
}}
document.addEventListener('DOMContentLoaded', function() {{
  openExternalLinksInNewTab(document);
  new MutationObserver(function(mutations) {{
    mutations.forEach(function(m) {{
      m.addedNodes.forEach(function(node) {{
        if (node.nodeType === 1) openExternalLinksInNewTab(node);
      }});
    }});
  }}).observe(document.body, {{ childList: true, subtree: true }});
}});
"""

# Insert before the last </script> tag (which closes the main script block)
# Find the position of </body>
body_close = code.rfind('</body>')
if body_close == -1:
    print("ERROR: Could not find </body>")
    exit(1)

# Insert a new script block right before </body>
insert_code = f'\n<script>{js_snippet}</script>\n'
code = code[:body_close] + insert_code + code[body_close:]

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done — added external link handler before </body>")
