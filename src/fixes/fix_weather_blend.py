#!/usr/bin/env python3
"""
fix_weather_blend.py
Modifies create_html.py to implement multi-model weather blending (GFS + ECMWF)
and add forecast source attribution.
"""

import os

FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_html.py")

# ── CHANGE 1: Replace fetchWeather with multi-model blend ──────────────────

OLD_FETCH_WEATHER = r'''async function fetchWeather(lat, lon) {{
  const key = `${{lat}},${{lon}}`;
  if (weatherCache[key]) return weatherCache[key];

  try {{
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Open-Meteo error: ${{res.status}}`);
    const data = await res.json();
    weatherCache[key] = {{ daily: data.daily, hourly: data.hourly || null }};
    return weatherCache[key];
  }} catch (err) {{
    console.warn(`Weather fetch failed for ${{lat}},${{lon}}:`, err);
    return null;
  }}
}}'''

NEW_FETCH_WEATHER = r'''async function fetchWeather(lat, lon) {{
  const key = `${{lat}},${{lon}}`;
  if (weatherCache[key]) return weatherCache[key];

  try {{
    const baseParams = `latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`;

    // Fetch from two models in parallel for more robust forecast blend
    const [res1, res2] = await Promise.allSettled([
      fetch(`https://api.open-meteo.com/v1/forecast?${{baseParams}}`),
      fetch(`https://api.open-meteo.com/v1/forecast?${{baseParams}}&models=ecmwf_ifs025`)
    ]);

    let gfsData = null, ecmwfData = null;
    if (res1.status === 'fulfilled' && res1.value.ok) gfsData = await res1.value.json();
    if (res2.status === 'fulfilled' && res2.value.ok) ecmwfData = await res2.value.json();

    if (!gfsData && !ecmwfData) throw new Error('All weather models failed');

    if (!ecmwfData) {{
      weatherCache[key] = {{ daily: gfsData.daily, hourly: gfsData.hourly || null }};
      return weatherCache[key];
    }}
    if (!gfsData) {{
      weatherCache[key] = {{ daily: ecmwfData.daily, hourly: ecmwfData.hourly || null }};
      return weatherCache[key];
    }}

    // Blend both models for more accurate predictions
    const blended = blendForecasts(gfsData.daily, ecmwfData.daily);
    weatherCache[key] = {{ daily: blended, hourly: gfsData.hourly || null }};
    return weatherCache[key];
  }} catch (err) {{
    console.warn(`Weather fetch failed for ${{lat}},${{lon}}:`, err);
    return null;
  }}
}}

function blendForecasts(gfs, ecmwf) {{
  const result = {{
    time: gfs.time,
    temperature_2m_max: [],
    temperature_2m_min: [],
    precipitation_probability_max: [],
    wind_speed_10m_max: [],
    weather_code: []
  }};

  for (let i = 0; i < gfs.time.length; i++) {{
    const date = gfs.time[i];
    const eIdx = ecmwf.time ? ecmwf.time.indexOf(date) : -1;

    if (eIdx >= 0 && ecmwf.temperature_2m_max[eIdx] != null) {{
      result.temperature_2m_max.push((gfs.temperature_2m_max[i] + ecmwf.temperature_2m_max[eIdx]) / 2);
      result.temperature_2m_min.push((gfs.temperature_2m_min[i] + ecmwf.temperature_2m_min[eIdx]) / 2);
      result.precipitation_probability_max.push(Math.max(
        gfs.precipitation_probability_max[i] || 0,
        ecmwf.precipitation_probability_max[eIdx] || 0
      ));
      result.wind_speed_10m_max.push((gfs.wind_speed_10m_max[i] + ecmwf.wind_speed_10m_max[eIdx]) / 2);
      result.weather_code.push(gfs.weather_code[i]);
    }} else {{
      result.temperature_2m_max.push(gfs.temperature_2m_max[i]);
      result.temperature_2m_min.push(gfs.temperature_2m_min[i]);
      result.precipitation_probability_max.push(gfs.precipitation_probability_max[i]);
      result.wind_speed_10m_max.push(gfs.wind_speed_10m_max[i]);
      result.weather_code.push(gfs.weather_code[i]);
    }}
  }}

  return result;
}}'''

# ── CHANGE 2: Add forecast source attribution before panel.innerHTML ───────

OLD_PANEL_END = r'''  html += `</div>`;

  panel.innerHTML = html;
  return panel;
}}'''

NEW_PANEL_END = r'''  html += `</div>`;

  // Forecast source attribution
  html += `<div style="margin-top:8px;font-size:0.72em;color:#999;text-align:right;">Forecast: GFS + ECMWF blend via <a href=\"https://open-meteo.com\" target=\"_blank\" style=\"color:#999;\">Open-Meteo</a> · Updates on page load</div>`;

  panel.innerHTML = html;
  return panel;
}}'''


def main():
    print(f"Reading: {FILEPATH}")
    with open(FILEPATH, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # ── Change 1 ──
    if OLD_FETCH_WEATHER in content:
        content = content.replace(OLD_FETCH_WEATHER, NEW_FETCH_WEATHER, 1)
        print("[OK] Change 1: Replaced fetchWeather with multi-model blend + blendForecasts helper.")
    else:
        print("[SKIP] Change 1: fetchWeather pattern NOT found — may already be applied.")

    # ── Change 2 ──
    if OLD_PANEL_END in content:
        content = content.replace(OLD_PANEL_END, NEW_PANEL_END, 1)
        print("[OK] Change 2: Added forecast source attribution before panel.innerHTML.")
    else:
        print("[SKIP] Change 2: panel.innerHTML pattern NOT found — may already be applied.")

    if len(content) == original_len:
        print("\nNo changes were made. The file may already be patched.")
        return

    with open(FILEPATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nDone. File updated ({original_len} -> {len(content)} bytes).")


if __name__ == "__main__":
    main()
