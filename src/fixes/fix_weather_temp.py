import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

html_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/road-trip-plan.html"

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# 1. Add hourly temperature_2m to API URLs
old1 = "&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto&models=best_match,ecmwf_ifs025"
new1 = "&hourly=precipitation_probability,temperature_2m&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto&models=best_match,ecmwf_ifs025"
if old1 in content:
    content = content.replace(old1, new1)
    count += 1
    print("Updated: main API URL with hourly temperature")

old1b = "&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`"
new1b = "&hourly=precipitation_probability,temperature_2m&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`"
if old1b in content:
    content = content.replace(old1b, new1b)
    count += 1
    print("Updated: fallback API URL with hourly temperature")

# 2. Update hourly normalization to handle temperature_2m
old2 = """    if (hourly && !hourly.precipitation_probability && hourly.precipitation_probability_best_match) {
      hourly = { time: hourly.time, precipitation_probability: hourly.precipitation_probability_best_match };
    }"""
new2 = """    if (hourly && !hourly.precipitation_probability && hourly.precipitation_probability_best_match) {
      hourly = {
        time: hourly.time,
        precipitation_probability: hourly.precipitation_probability_best_match,
        temperature_2m: hourly.temperature_2m_best_match || hourly.temperature_2m || []
      };
    } else if (hourly) {
      hourly.temperature_2m = hourly.temperature_2m_best_match || hourly.temperature_2m || [];
    }"""
if old2 in content:
    content = content.replace(old2, new2)
    count += 1
    print("Updated: hourly normalization for temperature")

# 3. Update extractHourlyPrecip to include temperature
old3 = """function extractHourlyPrecip(weatherData, dateStr) {
  if (!weatherData || !weatherData.hourly || !weatherData.hourly.time) return null;
  const hourly = weatherData.hourly;
  const hours = [];
  for (let i = 0; i < hourly.time.length; i++) {
    if (hourly.time[i].startsWith(dateStr)) {
      const hr = parseInt(hourly.time[i].substring(11, 13), 10);
      hours.push({ hour: hr, precip: hourly.precipitation_probability[i] || 0 });
    }
  }
  return hours.length > 0 ? hours : null;
}"""
new3 = """function extractHourlyPrecip(weatherData, dateStr) {
  if (!weatherData || !weatherData.hourly || !weatherData.hourly.time) return null;
  const hourly = weatherData.hourly;
  const hours = [];
  const temps = hourly.temperature_2m || [];
  for (let i = 0; i < hourly.time.length; i++) {
    if (hourly.time[i].startsWith(dateStr)) {
      const hr = parseInt(hourly.time[i].substring(11, 13), 10);
      hours.push({
        hour: hr,
        precip: hourly.precipitation_probability[i] || 0,
        temp: temps[i] != null ? Math.round(temps[i]) : null
      });
    }
  }
  return hours.length > 0 ? hours : null;
}"""
if old3 in content:
    content = content.replace(old3, new3)
    count += 1
    print("Updated: extractHourlyPrecip with temperature")

# 4. Update the main high/low display to be more prominent
old4 = """    html += `<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">`;
    html += `<span style="font-size:2.2em;">${icon}</span>`;
    html += `<div>`;
    html += `<div style="font-size:1.3em;font-weight:600;">${high}\u00b0F / ${low}\u00b0F</div>`;
    html += `<div style="color:#555;">${forecastText}</div>`;
    html += `</div></div>`;"""
new4 = """    html += `<div style="display:flex;align-items:center;gap:14px;margin-bottom:12px;">`;
    html += `<span style="font-size:2.4em;">${icon}</span>`;
    html += `<div>`;
    html += `<div style="display:flex;align-items:baseline;gap:8px;">`;
    html += `<span style="font-size:1.6em;font-weight:700;color:#1B4332;">${high}\u00b0</span>`;
    html += `<span style="font-size:0.95em;color:#888;">/ ${low}\u00b0F</span>`;
    html += `</div>`;
    html += `<div style="color:#555;font-size:0.95em;">${forecastText}</div>`;
    html += `</div></div>`;"""
if old4 in content:
    content = content.replace(old4, new4)
    count += 1
    print("Updated: high/low display - more prominent")

# 5. Update hourly precipitation display to include temperature
old5 = """    if (forecast.hourlyPrecip && forecast.hourlyPrecip.length > 0) {
      html += `<div style="margin-bottom:8px;">`;
      html += `<div style="font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:4px;">\U0001f4a7 Precipitation Chance by Hour</div>`;
      html += `<div style="display:flex;flex-wrap:wrap;gap:6px 12px;font-size:0.82em;color:#555;">`;
      for (const h of forecast.hourlyPrecip) {
        if (h.hour % 3 === 0) {
          const labelStr = h.hour === 0 ? "12 AM" : h.hour < 12 ? h.hour + " AM" : h.hour === 12 ? "12 PM" : (h.hour - 12) + " PM";
          const color = h.precip > 60 ? "#2563eb" : h.precip > 30 ? "#1B4332" : "#555";
          const weight = h.precip > 30 ? "600" : "400";
          html += `<span style="color:${color};font-weight:${weight};">${labelStr}: ${h.precip}%</span>`;
        }
      }
      html += `</div>`;
      html += `</div>`;"""
new5 = """    if (forecast.hourlyPrecip && forecast.hourlyPrecip.length > 0) {
      html += `<div style="margin-bottom:10px;">`;
      html += `<div style="font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:6px;">\U0001f321\ufe0f Hourly Forecast</div>`;
      html += `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(105px,1fr));gap:4px 8px;font-size:0.82em;">`;
      for (const h of forecast.hourlyPrecip) {
        if (h.hour % 3 === 0) {
          const labelStr = h.hour === 0 ? "12a" : h.hour < 12 ? h.hour + "a" : h.hour === 12 ? "12p" : (h.hour - 12) + "p";
          const precipColor = h.precip > 60 ? "#2563eb" : h.precip > 30 ? "#1B4332" : "#999";
          const precipWeight = h.precip > 30 ? "600" : "400";
          const tempStr = h.temp != null ? h.temp + "\u00b0" : "";
          html += `<div style="display:flex;align-items:center;gap:4px;padding:2px 0;">`;
          html += `<span style="font-weight:600;color:#1B4332;min-width:28px;">${labelStr}</span>`;
          if (tempStr) html += `<span style="font-weight:500;color:#333;min-width:28px;">${tempStr}</span>`;
          html += `<span style="color:${precipColor};font-weight:${precipWeight};">\U0001f4a7${h.precip}%</span>`;
          html += `</div>`;
        }
      }
      html += `</div>`;
      html += `</div>`;"""
if old5 in content:
    content = content.replace(old5, new5)
    count += 1
    print("Updated: hourly display with temperature")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Done! " + str(count) + " changes applied")
