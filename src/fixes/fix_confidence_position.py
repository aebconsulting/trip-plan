#!/usr/bin/env python3
"""Move confidence score under temperature, keep source attribution at bottom."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add confidence line right after the temperature/forecast text block
# Current: icon + temp + forecast text, then closes the div
old_temp_block = """    html += `<div style=\\"font-size:1.3em;font-weight:600;\\">${{high}}\u00B0F / ${{low}}\u00B0F</div>`;
    html += `<div style=\\"color:#555;\\">${{forecastText}}</div>`;
    html += `</div></div>`;"""

new_temp_block = """    html += `<div style=\\"font-size:1.3em;font-weight:600;\\">${{high}}\u00B0F / ${{low}}\u00B0F</div>`;
    html += `<div style=\\"color:#555;\\">${{forecastText}}</div>`;
    var conf = getConfidence(dateStr, forecast.tempSpread || null);
    html += `<div style=\\"font-size:0.75em;margin-top:3px;\\"><span style=\\"font-weight:600;color:${{conf.color}};\\">${{conf.score}}% confidence</span> <span style=\\"color:#bbb;\\">\u00b7 ${{conf.label}} (${{conf.daysOut}}d out)</span></div>`;
    html += `</div></div>`;"""

code = code.replace(old_temp_block, new_temp_block)

# 2. Replace the bottom confidence+attribution with just attribution
old_bottom = """  // Forecast confidence + source attribution
  var conf = getConfidence(dateStr, forecast.tempSpread || null);
  html += `<div style="margin-top:10px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;font-size:0.75em;color:#999;">`;
  html += `<div style="display:flex;align-items:center;gap:6px;">`;
  html += `<span style="font-weight:600;color:${{conf.color}};">`;
  html += `${{conf.score}}% confidence</span>`;
  html += `<span style="color:#bbb;">\u00b7 ${{conf.label}} (${{conf.daysOut}}d out)</span>`;
  html += `</div>`;
  html += `<div>GFS + ECMWF blend via <a href=\\"https://open-meteo.com\\" target=\\"_blank\\" style=\\"color:#999;\\">Open-Meteo</a></div>`;
  html += `</div>`;"""

new_bottom = """  // Forecast source attribution
  html += `<div style="margin-top:8px;font-size:0.72em;color:#999;text-align:right;">GFS + ECMWF blend via <a href=\\"https://open-meteo.com\\" target=\\"_blank\\" style=\\"color:#999;\\">Open-Meteo</a></div>`;"""

code = code.replace(old_bottom, new_bottom)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - moved confidence under temperature")
