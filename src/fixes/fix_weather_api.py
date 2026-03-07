#!/usr/bin/env python3
"""
fix_weather_api.py
Replaces the NOAA weather API functions in create_html.py with Open-Meteo API equivalents.
Open-Meteo is free, requires no API key, supports 16-day forecasts, and has CORS enabled.
"""

import os
import sys

FILE_PATH = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

# The new weather API block (already in f-string escaped format with {{ and }})
NEW_BLOCK = r"""// ============================================
// WEATHER API FUNCTIONS (Open-Meteo — 16-day forecast)
// ============================================

const weatherCache = {{}};

function wmoCodeToText(code) {{
  const map = {{
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
  }};
  return map[code] || "Partly cloudy";
}}

async function fetchWeather(lat, lon) {{
  const key = `${{lat}},${{lon}}`;
  if (weatherCache[key]) return weatherCache[key];

  try {{
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Open-Meteo error: ${{res.status}}`);
    const data = await res.json();
    weatherCache[key] = data.daily;
    return data.daily;
  }} catch (err) {{
    console.warn(`Weather fetch failed for ${{lat}},${{lon}}:`, err);
    return null;
  }}
}}

function findForecast(daily, dateStr) {{
  if (!daily || !daily.time) return {{ day: null, night: null }};
  const idx = daily.time.indexOf(dateStr);
  if (idx === -1) return {{ day: null, night: null }};
  return {{
    day: {{
      temperature: Math.round(daily.temperature_2m_max[idx]),
      shortForecast: wmoCodeToText(daily.weather_code[idx]),
      windSpeed: Math.round(daily.wind_speed_10m_max[idx]) + " mph",
      windDirection: "",
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }},
      detailedForecast: ""
    }},
    night: {{
      temperature: Math.round(daily.temperature_2m_min[idx]),
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }}
    }}
  }};
}}

function parseWindSpeed(windStr) {{
  if (!windStr) return 0;
  const match = windStr.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}}"""


def main():
    # Read the file
    if not os.path.exists(FILE_PATH):
        print(f"ERROR: File not found: {FILE_PATH}")
        sys.exit(1)

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    original_count = len(lines)
    print(f"Read {original_count} lines from create_html.py")

    # Find the start of the weather API block
    # Looking for: "// WEATHER API FUNCTIONS"
    start_idx = None
    for i, line in enumerate(lines):
        if "// WEATHER API FUNCTIONS" in line:
            # The section header starts one line before (the === line)
            # Check if previous line is the === separator
            if i > 0 and "// ====" in lines[i - 1]:
                start_idx = i - 1
            else:
                start_idx = i
            break

    if start_idx is None:
        print("ERROR: Could not find '// WEATHER API FUNCTIONS' marker")
        sys.exit(1)

    print(f"Found WEATHER API FUNCTIONS section starting at line {start_idx + 1}")

    # Find the end of parseWindSpeed function
    # Looking for the closing }} of parseWindSpeed, then the blank line before PANEL BUILDER
    end_idx = None
    in_parse_wind = False
    for i in range(start_idx, len(lines)):
        if "function parseWindSpeed" in lines[i]:
            in_parse_wind = True
        if in_parse_wind and lines[i].strip() == "}}":
            end_idx = i
            break

    if end_idx is None:
        print("ERROR: Could not find end of parseWindSpeed function")
        sys.exit(1)

    print(f"Found end of parseWindSpeed at line {end_idx + 1}")
    print(f"Replacing lines {start_idx + 1} through {end_idx + 1} ({end_idx - start_idx + 1} lines)")

    # Build the new file content
    new_lines = lines[:start_idx] + NEW_BLOCK.split("\n") + lines[end_idx + 1:]

    new_content = "\n".join(new_lines)
    new_count = len(new_lines)

    # Write back
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"\nSUCCESS!")
    print(f"  Original lines: {original_count}")
    print(f"  New lines:      {new_count}")
    print(f"  Lines removed:  {end_idx - start_idx + 1}")
    print(f"  Lines added:    {len(NEW_BLOCK.split(chr(10)))}")
    print(f"  Net change:     {new_count - original_count:+d} lines")

    # Verify the changes
    print("\n--- Verification ---")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        verify_lines = f.read().split("\n")

    # Check for key markers
    checks = [
        ("Open-Meteo", False),
        ("wmoCodeToText", False),
        ("api.open-meteo.com", False),
        ("data.daily", False),
        ("daily.time.indexOf", False),
        ("temperature_2m_max", False),
        ("api.weather.gov", True),  # This should NOT be present
    ]

    all_ok = True
    for marker, should_be_absent in checks:
        found = any(marker in line for line in verify_lines)
        if should_be_absent:
            if found:
                print(f"  FAIL: '{marker}' should have been removed but is still present")
                all_ok = False
            else:
                print(f"  OK:   '{marker}' correctly removed")
        else:
            if found:
                print(f"  OK:   '{marker}' found")
            else:
                print(f"  FAIL: '{marker}' not found")
                all_ok = False

    if all_ok:
        print("\nAll verification checks passed!")
    else:
        print("\nWARNING: Some verification checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
