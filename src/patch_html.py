"""
Patch create_html.py to add weather, clothing, and road conditions features.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. INSERT WEATHER CSS before /* ===== MOBILE ===== */
weather_css = r"""
  /* ===== WEATHER + CLOTHING + ROAD CONDITIONS ===== */
  .weather-panel {
    background: linear-gradient(135deg, var(--parchment) 0%, var(--cream-dark) 100%);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 0 0 var(--space-md);
    box-shadow: var(--shadow-sm);
  }
  .weather-panel-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin: 0 0 10px;
  }
  .weather-conditions {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 4px;
  }
  .weather-icon { font-size: 2em; line-height: 1; }
  .weather-temps { display: flex; flex-direction: column; gap: 2px; }
  .weather-high {
    font-family: 'Fraunces', serif;
    font-size: 1.4em;
    font-weight: 700;
    color: var(--forest);
    line-height: 1;
  }
  .weather-low {
    font-family: 'Outfit', sans-serif;
    font-size: 0.82em;
    color: var(--text-muted);
  }
  .weather-details { display: flex; flex-direction: column; gap: 2px; }
  .weather-forecast {
    font-family: 'Outfit', sans-serif;
    font-size: 0.92em;
    font-weight: 500;
    color: var(--text);
  }
  .weather-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75em;
    color: var(--text-muted);
    display: flex;
    gap: 12px;
  }
  .weather-loading {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
  }
  .weather-loading .skeleton {
    height: 14px;
    border-radius: 7px;
    background: linear-gradient(90deg, var(--border-light) 25%, var(--cream) 50%, var(--border-light) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
  }
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  .weather-unavailable {
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
    color: var(--text-muted);
    font-style: italic;
    padding: 6px 0;
  }
  .clothing-label {
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--terracotta);
    margin: 12px 0 8px;
  }
  .clothing-strip {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0;
    scrollbar-width: none;
  }
  .clothing-strip::-webkit-scrollbar { display: none; }
  .clothing-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    min-width: 64px;
    padding: 8px 10px;
    background: var(--card-bg);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    transition: all 0.2s;
  }
  .clothing-item:hover {
    border-color: var(--terracotta);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
  }
  .clothing-item svg { width: 32px; height: 32px; }
  .clothing-item-label {
    font-family: 'Outfit', sans-serif;
    font-size: 0.68em;
    font-weight: 500;
    color: var(--text-muted);
    text-align: center;
    white-space: nowrap;
  }
  .road-section {
    border-top: 1px solid var(--border-light);
    margin-top: 14px;
    padding-top: 12px;
  }
  .road-section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin: 0 0 8px;
  }
  .road-status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
  }
  .road-status.road-clear { color: var(--forest-mid); }
  .road-status.road-closed { color: var(--warning-border); font-weight: 600; }
  .road-links {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 8px;
  }
  .road-link {
    font-family: 'Outfit', sans-serif;
    font-size: 0.75em;
    font-weight: 600;
    color: var(--forest-mid) !important;
    padding: 4px 12px;
    border: 1px solid var(--border) !important;
    border-radius: 100px;
    text-decoration: none;
    transition: all 0.2s;
  }
  .road-link:hover {
    background: var(--forest);
    color: var(--cream) !important;
    border-color: var(--forest) !important;
  }

"""

# The CSS uses single braces but the file uses double braces (f-string)
# Convert single braces to double for the f-string context
weather_css_escaped = weather_css.replace('{', '{{').replace('}', '}}')

content = content.replace(
    '  /* ===== MOBILE ===== */',
    weather_css_escaped + '  /* ===== MOBILE ===== */'
)

# Add mobile styles
mobile_add = """    .weather-panel {{ padding: 14px 16px; }}
    .weather-conditions {{ gap: 10px; }}
    .weather-high {{ font-size: 1.2em; }}
    .clothing-item {{ min-width: 56px; padding: 6px 8px; }}
    .clothing-item svg {{ width: 28px; height: 28px; }}
"""
content = content.replace(
    "    .alert {{ padding: 14px 16px; }}\n  }}",
    "    .alert {{ padding: 14px 16px; }}\n" + mobile_add + "  }}"
)

# 2. INSERT WEATHER JAVASCRIPT
# Read the JS from a separate file we'll create
js_path = r"C:\Users\AB Digial\OneDrive\Documents\Claude\weather_js.txt"
with open(js_path, 'r', encoding='utf-8') as jf:
    weather_js = jf.read()

content = content.replace(
    "\n}});\n</script>",
    "\n" + weather_js + "\n}});\n</script>"
)

# 3. Filter out IMPLEMENTATION PLAN from markdown
filter_code = """
# Remove implementation plan section (not for display)
if '## IMPLEMENTATION PLAN' in md_content:
    md_content = md_content[:md_content.index('## IMPLEMENTATION PLAN')].rstrip()

"""
content = content.replace(
    "md_content = ensure_blank_before_tables(md_content)",
    "md_content = ensure_blank_before_tables(md_content)\n" + filter_code
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched create_html.py successfully!")
print(f"New size: {len(content):,} chars")
