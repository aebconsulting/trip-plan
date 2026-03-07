#!/usr/bin/env python3
"""Add forecast confidence score to weather panels."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add a temp_spread array to blendModels result to track model divergence
old_result = """  const result = {{
    time: d.time,
    temperature_2m_max: [],
    temperature_2m_min: [],
    precipitation_probability_max: [],
    wind_speed_10m_max: [],
    weather_code: []
  }};"""

new_result = """  const result = {{
    time: d.time,
    temperature_2m_max: [],
    temperature_2m_min: [],
    precipitation_probability_max: [],
    wind_speed_10m_max: [],
    weather_code: [],
    temp_spread: []
  }};"""

code = code.replace(old_result, new_result)

# 2. Track the spread when both models available
old_blend = """    if (bmHigh != null && ecHigh != null) {{
      result.temperature_2m_max.push((bmHigh + ecHigh) / 2);
      result.temperature_2m_min.push((bmLow + ecLow) / 2);
      result.precipitation_probability_max.push(Math.max(bmPrecip || 0, ecPrecip || 0));
      result.wind_speed_10m_max.push((bmWind + ecWind) / 2);
      result.weather_code.push(bmCode != null ? bmCode : ecHigh);
    }} else if (bmHigh != null) {{
      result.temperature_2m_max.push(bmHigh);
      result.temperature_2m_min.push(bmLow);
      result.precipitation_probability_max.push(bmPrecip);
      result.wind_speed_10m_max.push(bmWind);
      result.weather_code.push(bmCode);
    }} else if (ecHigh != null) {{
      result.temperature_2m_max.push(ecHigh);
      result.temperature_2m_min.push(ecLow);
      result.precipitation_probability_max.push(ecPrecip);"""

new_blend = """    if (bmHigh != null && ecHigh != null) {{
      result.temperature_2m_max.push((bmHigh + ecHigh) / 2);
      result.temperature_2m_min.push((bmLow + ecLow) / 2);
      result.precipitation_probability_max.push(Math.max(bmPrecip || 0, ecPrecip || 0));
      result.wind_speed_10m_max.push((bmWind + ecWind) / 2);
      result.weather_code.push(bmCode != null ? bmCode : ecHigh);
      result.temp_spread.push(Math.abs(bmHigh - ecHigh));
    }} else if (bmHigh != null) {{
      result.temperature_2m_max.push(bmHigh);
      result.temperature_2m_min.push(bmLow);
      result.precipitation_probability_max.push(bmPrecip);
      result.wind_speed_10m_max.push(bmWind);
      result.weather_code.push(bmCode);
      result.temp_spread.push(0);
    }} else if (ecHigh != null) {{
      result.temperature_2m_max.push(ecHigh);
      result.temperature_2m_min.push(ecLow);
      result.precipitation_probability_max.push(ecPrecip);"""

code = code.replace(old_blend, new_blend)

# 3. Add temp_spread push for the ecHigh-only and null cases
# ecHigh-only case
code = code.replace(
    """      result.weather_code.push(d.weather_code_ecmwf_ifs025 ? d.weather_code_ecmwf_ifs025[i] : 2);
    }} else {{
      result.temperature_2m_max.push(null);""",
    """      result.weather_code.push(d.weather_code_ecmwf_ifs025 ? d.weather_code_ecmwf_ifs025[i] : 2);
      result.temp_spread.push(0);
    }} else {{
      result.temperature_2m_max.push(null);"""
)

code = code.replace(
    """      result.weather_code.push(null);
    }}
  }}

  return result;""",
    """      result.weather_code.push(null);
      result.temp_spread.push(0);
    }}
  }}

  return result;"""
)

# 4. Pass temp_spread through findForecast
old_find_return = """  return {{
    day: {{
      temperature: Math.round(daily.temperature_2m_max[idx]),
      shortForecast: wmoCodeToText(daily.weather_code[idx]),
      windSpeed: Math.round(daily.wind_speed_10m_max[idx]) + " mph",
      windDirection: "",
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }},
      detailedForecast: ""
    }},"""

new_find_return = """  var spread = daily.temp_spread ? daily.temp_spread[idx] : null;
  return {{
    tempSpread: spread,
    day: {{
      temperature: Math.round(daily.temperature_2m_max[idx]),
      shortForecast: wmoCodeToText(daily.weather_code[idx]),
      windSpeed: Math.round(daily.wind_speed_10m_max[idx]) + " mph",
      windDirection: "",
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }},
      detailedForecast: ""
    }},"""

code = code.replace(old_find_return, new_find_return)

# 5. Add getConfidence function before buildPanel
confidence_fn = """
function getConfidence(dateStr, tempSpread) {{
  var today = new Date();
  today.setHours(0,0,0,0);
  var target = new Date(dateStr + 'T00:00:00');
  var daysOut = Math.round((target - today) / 86400000);

  // Base confidence from days out (meteorological accuracy curve)
  var base;
  if (daysOut <= 1) base = 95;
  else if (daysOut <= 3) base = 90;
  else if (daysOut <= 5) base = 80;
  else if (daysOut <= 7) base = 68;
  else if (daysOut <= 10) base = 55;
  else if (daysOut <= 14) base = 38;
  else base = 25;

  // Adjust for model agreement (temp spread penalty)
  // If models diverge > 5F, reduce confidence
  if (tempSpread != null && tempSpread > 0) {{
    var penalty = Math.min(15, Math.round(tempSpread * 1.2));
    base = Math.max(15, base - penalty);
  }}

  // Label
  var label, color;
  if (base >= 85) {{ label = 'High'; color = '#15803d'; }}
  else if (base >= 65) {{ label = 'Good'; color = '#65a30d'; }}
  else if (base >= 45) {{ label = 'Moderate'; color = '#ca8a04'; }}
  else if (base >= 30) {{ label = 'Low'; color = '#dc2626'; }}
  else {{ label = 'Very Low'; color = '#991b1b'; }}

  return {{ score: base, label: label, color: color, daysOut: daysOut }};
}}

"""

code = code.replace(
    "function buildPanel(dayInfo, forecast) {{",
    confidence_fn + "function buildPanel(dayInfo, forecast) {{"
)

# 6. Add confidence display to buildPanel - replace the attribution line
old_attr = """  // Forecast source attribution
  html += `<div style="margin-top:8px;font-size:0.72em;color:#999;text-align:right;">Forecast: GFS + ECMWF blend via <a href=\\"https://open-meteo.com\\" target=\\"_blank\\" style=\\"color:#999;\\">Open-Meteo</a> \u00b7 Updates on page load</div>`;"""

new_attr = """  // Forecast confidence + source attribution
  var conf = getConfidence(dateStr, forecast.tempSpread || null);
  html += `<div style="margin-top:10px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;font-size:0.75em;color:#999;">`;
  html += `<div style="display:flex;align-items:center;gap:6px;">`;
  html += `<span style="font-weight:600;color:${{conf.color}};">`;
  html += `${{conf.score}}% confidence</span>`;
  html += `<span style="color:#bbb;">\u00b7 ${{conf.label}} (${{conf.daysOut}}d out)</span>`;
  html += `</div>`;
  html += `<div>GFS + ECMWF blend via <a href=\\"https://open-meteo.com\\" target=\\"_blank\\" style=\\"color:#999;\\">Open-Meteo</a></div>`;
  html += `</div>`;"""

code = code.replace(old_attr, new_attr)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done - added forecast confidence scores")
