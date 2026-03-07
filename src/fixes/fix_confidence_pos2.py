#!/usr/bin/env python3
"""Move confidence score between wind and What to Wear."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove the confidence line from inside the temp block (where it got lost)
code = code.replace(
    """    html += `<div style=\\"color:#555;\\">${{forecastText}}</div>`;
    var conf = getConfidence(dateStr, forecast.tempSpread || null);
    html += `<div style=\\"font-size:0.75em;margin-top:3px;\\"><span style=\\"font-weight:600;color:${{conf.color}};\\">${{conf.score}}% confidence</span> <span style=\\"color:#bbb;">\u00b7 ${{conf.label}} (${{conf.daysOut}}d out)</span></div>`;
    html += `</div></div>`;""",
    """    html += `<div style=\\"color:#555;\\">${{forecastText}}</div>`;
    html += `</div></div>`;"""
)

# 2. Add confidence between wind and clothing strip
old_wind_to_clothing = """    if (windDay || windNight) {{
      html += `<div style=\\"font-size:0.9em;color:#555;margin-bottom:10px;\\">🌬️ Wind: ${{windDay || windNight}} ${{windDir}}</div>`;
    }}

    // Clothing strip"""

new_wind_to_clothing = """    if (windDay || windNight) {{
      html += `<div style=\\"font-size:0.9em;color:#555;margin-bottom:10px;\\">🌬️ Wind: ${{windDay || windNight}} ${{windDir}}</div>`;
    }}

    // Forecast confidence
    var conf = getConfidence(dateStr, forecast.tempSpread || null);
    html += `<div style=\\"font-size:0.82em;margin-bottom:10px;padding:6px 10px;background:rgba(0,0,0,0.03);border-radius:8px;display:inline-block;\\">`;
    html += `<span style=\\"font-weight:600;color:${{conf.color}};\\">${{conf.score}}% confidence</span>`;
    html += ` <span style=\\"color:#999;\\">\u00b7 ${{conf.label}} (${{conf.daysOut}}d out)</span>`;
    html += `</div>`;

    // Clothing strip"""

code = code.replace(old_wind_to_clothing, new_wind_to_clothing)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - confidence now between wind and What to Wear")
