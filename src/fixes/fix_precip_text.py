#!/usr/bin/env python3
"""Replace the bar-chart precipitation block with a text-based display in create_html.py."""

import os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_html.py")

OLD_BLOCK = r'''    if (forecast.hourlyPrecip && forecast.hourlyPrecip.length > 0) {{
      const maxP = Math.max(...forecast.hourlyPrecip.map(h => h.precip), 1);
      html += `<div style=\"margin-bottom:8px;\">`;
      html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:4px;\">💧 Hourly Precipitation Chance</div>`;
      html += `<div style=\"display:flex;align-items:flex-end;gap:1px;height:48px;padding:2px 0;\">`;
      for (const h of forecast.hourlyPrecip) {{
        const barH = Math.max((h.precip / 100) * 44, 1);
        const color = h.precip > 60 ? "#2563eb" : h.precip > 30 ? "#60a5fa" : "#93c5fd";
        const show = (h.hour % 3 === 0);
        const labelStr = h.hour === 0 ? "12a" : h.hour < 12 ? h.hour + "a" : h.hour === 12 ? "12p" : (h.hour - 12) + "p";
        html += `<div style=\"display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;\">`;
        html += `<div style=\"width:100%;max-width:14px;height:${{barH}}px;background:${{color}};border-radius:2px 2px 0 0;margin:0 auto;\" title=\"${{labelStr}}: ${{h.precip}}%\"></div>`;
        if (show) {{
          html += `<span style=\"font-size:0.55em;color:#888;margin-top:1px;white-space:nowrap;\">${{labelStr}}</span>`;
        }}
        html += `</div>`;
      }}
      html += `</div>`;
      const overallMax = Math.max(...forecast.hourlyPrecip.map(h => h.precip));
      html += `<div style=\"font-size:0.75em;color:#666;margin-top:2px;\">Peak: ${{overallMax}}%</div>`;
      html += `</div>`;
    }}'''

NEW_BLOCK = r'''    if (forecast.hourlyPrecip && forecast.hourlyPrecip.length > 0) {{
      html += `<div style=\"margin-bottom:8px;\">`;
      html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:4px;\">💧 Precipitation Chance by Hour</div>`;
      html += `<div style=\"display:flex;flex-wrap:wrap;gap:6px 12px;font-size:0.82em;color:#555;\">`;
      for (const h of forecast.hourlyPrecip) {{
        if (h.hour % 3 === 0) {{
          const labelStr = h.hour === 0 ? "12 AM" : h.hour < 12 ? h.hour + " AM" : h.hour === 12 ? "12 PM" : (h.hour - 12) + " PM";
          const color = h.precip > 60 ? "#2563eb" : h.precip > 30 ? "#1B4332" : "#555";
          const weight = h.precip > 30 ? "600" : "400";
          html += `<span style=\"color:${{color}};font-weight:${{weight}};\">${{labelStr}}: ${{h.precip}}%</span>`;
        }}
      }}
      html += `</div>`;
      html += `</div>`;
    }}'''

# Read file
with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if OLD_BLOCK not in content:
    print("ERROR: Could not find the old bar-chart block in create_html.py")
    print("The exact text was not matched.")
    raise SystemExit(1)

# Replace
new_content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)

# Verify replacement happened
if new_content == content:
    print("ERROR: Replacement produced no change.")
    raise SystemExit(1)

# Write back
with open(FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

old_lines = OLD_BLOCK.count("\n") + 1
new_lines = NEW_BLOCK.count("\n") + 1
print(f"SUCCESS: Replaced precipitation bar chart ({old_lines} lines) with text-based display ({new_lines} lines).")
print(f"File updated: {FILE}")
