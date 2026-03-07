old_text = """  }})();

  // Body-appended dropdown menu with backdrop"""

new_text = """  }})();

  // Clean up route connectors after reorder — remove all, re-add between adjacent day sections
  (function() {{
    document.querySelectorAll('.route-connector').forEach(el => el.remove());
    const days = document.querySelectorAll('.day-section');
    days.forEach((section, i) => {{
      if (i > 0) {{
        const connector = document.createElement('div');
        connector.className = 'route-connector';
        connector.innerHTML = '<div class="route-dot"></div>';
        section.parentNode.insertBefore(connector, section);
      }}
    }});
  }})();

  // Body-appended dropdown menu with backdrop"""

filepath = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

count = content.count(old_text)
print(f"Found {count} occurrence(s) of the target text.")

if count > 0:
    content = content.replace(old_text, new_text)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replacement successful. File updated.")
else:
    print("Target text not found. No changes made.")
