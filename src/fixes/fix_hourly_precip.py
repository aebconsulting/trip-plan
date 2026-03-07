"""
fix_hourly_precip.py
Patches create_html.py so that the fetchWeather function normalizes
hourly field names after blending daily data.

When Open-Meteo is called with &models=best_match,ecmwf_ifs025 the
hourly keys come back as precipitation_probability_best_match instead
of precipitation_probability.  The extractHourlyPrecip function
expects the plain name, so we add a normalization step.
"""

import pathlib, sys

target = pathlib.Path(r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py")

OLD = """\
    // Blend both models from the single response
    const blended = blendModels(d);
    weatherCache[key] = {{ daily: blended, hourly: data.hourly || null }};
    return weatherCache[key];"""

NEW = """\
    // Blend both models from the single response
    const blended = blendModels(d);
    // Normalize hourly fields (multi-model adds _best_match suffix)
    let hourly = data.hourly || null;
    if (hourly && !hourly.precipitation_probability && hourly.precipitation_probability_best_match) {{
      hourly = {{ time: hourly.time, precipitation_probability: hourly.precipitation_probability_best_match }};
    }}
    weatherCache[key] = {{ daily: blended, hourly: hourly }};
    return weatherCache[key];"""

content = target.read_text(encoding="utf-8")

if OLD not in content:
    print("ERROR: Could not find the expected text block in create_html.py")
    print("The file may have already been patched or the text has changed.")
    sys.exit(1)

count = content.count(OLD)
print(f"Found {count} occurrence(s) of the target text.")

new_content = content.replace(OLD, NEW, 1)
target.write_text(new_content, encoding="utf-8")

print("Patch applied successfully.")
print(f"  File: {target}")
print(f"  Replaced {len(OLD)} chars with {len(NEW)} chars")
