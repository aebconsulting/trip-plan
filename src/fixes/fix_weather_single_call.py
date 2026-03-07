import os

filepath = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Documents", "Claude", "create_html.py")

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "async function fetchWeather(lat, lon) {{"
end_marker = "function findForecast(daily, dateStr) {{"

si = content.find(start_marker)
ei = content.find(end_marker)

if si == -1:
    print("ERROR: Could not find fetchWeather start marker")
    raise SystemExit(1)
if ei == -1:
    print("ERROR: Could not find findForecast end marker")
    raise SystemExit(1)

new_block = 'async function fetchWeather(lat, lon) {{\n  const key = `${{lat}},${{lon}}`;\n  if (weatherCache[key]) return weatherCache[key];\n\n  try {{\n    // Single API call with both models - avoids rate limiting\n    const url = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto&models=best_match,ecmwf_ifs025`;\n    const res = await fetch(url);\n    if (!res.ok) throw new Error(`Open-Meteo error: ${{res.status}}`);\n    const data = await res.json();\n    const d = data.daily;\n\n    // Blend both models from the single response\n    const blended = blendModels(d);\n    weatherCache[key] = {{ daily: blended, hourly: data.hourly || null }};\n    return weatherCache[key];\n  }} catch (err) {{\n    // Fallback: try single default model if multi-model fails\n    try {{\n      const fallbackUrl = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`;\n      const res2 = await fetch(fallbackUrl);\n      if (!res2.ok) throw new Error(`Fallback error: ${{res2.status}}`);\n      const data2 = await res2.json();\n      weatherCache[key] = {{ daily: data2.daily, hourly: data2.hourly || null }};\n      return weatherCache[key];\n    }} catch (err2) {{\n      console.warn(`Weather fetch failed for ${{lat}},${{lon}}:`, err2);\n      return null;\n    }}\n  }}\n}}\n\nfunction blendModels(d) {{\n  // When both models are in one response, fields are suffixed:\n  // _best_match and _ecmwf_ifs025\n  const hasBM = d.temperature_2m_max_best_match != null;\n  const hasEC = d.temperature_2m_max_ecmwf_ifs025 != null;\n\n  // If only one model returned, use standard field names\n  if (!hasBM && !hasEC) {{\n    return d;\n  }}\n\n  const result = {{\n    time: d.time,\n    temperature_2m_max: [],\n    temperature_2m_min: [],\n    precipitation_probability_max: [],\n    wind_speed_10m_max: [],\n    weather_code: []\n  }};\n\n  for (let i = 0; i < d.time.length; i++) {{\n    const bmHigh = hasBM ? d.temperature_2m_max_best_match[i] : null;\n    const bmLow = hasBM ? d.temperature_2m_min_best_match[i] : null;\n    const bmPrecip = hasBM ? d.precipitation_probability_max_best_match[i] : null;\n    const bmWind = hasBM ? d.wind_speed_10m_max_best_match[i] : null;\n    const bmCode = hasBM ? d.weather_code_best_match[i] : null;\n\n    const ecHigh = hasEC ? d.temperature_2m_max_ecmwf_ifs025[i] : null;\n    const ecLow = hasEC ? d.temperature_2m_min_ecmwf_ifs025[i] : null;\n    const ecPrecip = hasEC ? d.precipitation_probability_max_ecmwf_ifs025[i] : null;\n    const ecWind = hasEC ? d.wind_speed_10m_max_ecmwf_ifs025[i] : null;\n\n    if (bmHigh != null && ecHigh != null) {{\n      result.temperature_2m_max.push((bmHigh + ecHigh) / 2);\n      result.temperature_2m_min.push((bmLow + ecLow) / 2);\n      result.precipitation_probability_max.push(Math.max(bmPrecip || 0, ecPrecip || 0));\n      result.wind_speed_10m_max.push((bmWind + ecWind) / 2);\n      result.weather_code.push(bmCode != null ? bmCode : ecHigh);\n    }} else if (bmHigh != null) {{\n      result.temperature_2m_max.push(bmHigh);\n      result.temperature_2m_min.push(bmLow);\n      result.precipitation_probability_max.push(bmPrecip);\n      result.wind_speed_10m_max.push(bmWind);\n      result.weather_code.push(bmCode);\n    }} else if (ecHigh != null) {{\n      result.temperature_2m_max.push(ecHigh);\n      result.temperature_2m_min.push(ecLow);\n      result.precipitation_probability_max.push(ecPrecip);\n      result.wind_speed_10m_max.push(ecWind);\n      result.weather_code.push(d.weather_code_ecmwf_ifs025 ? d.weather_code_ecmwf_ifs025[i] : 2);\n    }} else {{\n      result.temperature_2m_max.push(null);\n      result.temperature_2m_min.push(null);\n      result.precipitation_probability_max.push(null);\n      result.wind_speed_10m_max.push(null);\n      result.weather_code.push(null);\n    }}\n  }}\n\n  return result;\n}}\n'

content = content[:si] + new_block + content[ei:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS: Replaced dual-call fetchWeather + blendForecasts with single-call fetchWeather + blendModels.")
