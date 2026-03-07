# _write_gen.py: builds the replacement blocks and fix script
import os, sys, base64, json
basedir = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Claude")
print("basedir:", basedir)
SQ = chr(39)
NL = chr(10)
RED = chr(0x1f534)
NOENTRY = chr(0x26d4)
WARN = chr(0x26a0) + chr(0xfe0f)
EMDASH = chr(0x2014)
ARROW = chr(0x2192)
ROAD_EMOJI = chr(0x1f6e3) + chr(0xfe0f)

srcpath = os.path.join(basedir, "create_html.py")
with open(srcpath, "r", encoding="utf-8") as fh:
    content = fh.read()
original = content
print("Loaded:", len(content), "chars")

# Step 1: Build weather API marker
weather_marker = NL.join([
    "// " + "="*44,
    "// WEATHER API FUNCTIONS (Open-Meteo " + EMDASH + " 16-day forecast)",
    "// " + "="*44,
])
if weather_marker not in content:
    print("ERROR: Weather API marker not found")
    sys.exit(1)
print("  Found weather API marker")

# Build JS block for live road API
b1 = []
b1.append("// " + "="*44)
b1.append("// LIVE ROAD CONDITIONS API")
b1.append("// " + "="*44)
b1.append("")
b1.append("// Counties along the route, mapped to trip days")
b1.append("const ROUTE_COUNTIES = {{")
b1.append("  1: [],  // FL/GA - not NC")
b1.append("  2: [],  // Driving through SC")
b1.append("  3: [11],  // Buncombe (Asheville)")
b1.append("  4: [45],  // Henderson (Hendersonville)")
b1.append("  5: [11],  // Buncombe (Asheville/Biltmore)")
b1.append("  6: [45, 80],  // Henderson, Rutherford (Chimney Rock)")
b1.append("  7: [11, 88],  // Buncombe, Transylvania (Pisgah)")
b1.append("  8: [88],  // Transylvania (Brevard/DuPont)")
b1.append("  9: [95],  // Watauga (Boone)")
b1.append("  10: [3, 95],  // Avery, Watauga (Grandfather Mtn)")
b1.append("  11: [],  // Driving south")
b1.append("  12: []   // Driving south")
b1.append("}};")
b1.append("")
b1.append("// Key roads to filter for")
b1.append("const KEY_ROADS = [" + ", ".join([chr(34)+r+chr(34) for r in ["US-74","US-64","US-25","US-19","US-70","US-221","US-321","NC-9","NC-191","NC-280","NC-215","NC-276","I-26","I-40","I-240","I-77","I-81"]]) + "];")
b1.append("")
b1.append("let liveClosures = {{}};")
b1.append("let liveBRPAlerts = [];")
b1.append("let roadDataTimestamp = null;")
b1.append("")
b1.append("async function fetchNCDOTClosures() {{")
b1.append("  try {{")
b1.append("    const res = await fetch(" + SQ + "https://eapps.ncdot.gov/services/traffic-prod/v1/incidents?active=true" + SQ + ");")
b1.append("    if (!res.ok) throw new Error(" + SQ + "NCDOT API error" + SQ + ");")
b1.append("    const data = await res.json();")
b1.append("    ")
b1.append("    // Get all road closed incident IDs")
b1.append("    const closedIds = data.roadClosedIncidents || [];")
b1.append("    if (closedIds.length === 0) return;")
b1.append("    ")
b1.append("    // Fetch details for first 30 closed incidents (to limit API calls)")
b1.append("    const batchSize = 10;")
b1.append("    const idsToFetch = closedIds.slice(0, 30);")
b1.append("    const batches = [];")
b1.append("    for (let i = 0; i < idsToFetch.length; i += batchSize) {{")
b1.append("      batches.push(idsToFetch.slice(i, i + batchSize));")
b1.append("    }}")
b1.append("    ")
b1.append("    const allIncidents = [];")
b1.append("    for (const batch of batches) {{")
b1.append("      const results = await Promise.all(")
b1.append("        batch.map(id => ")
b1.append("          fetch(" + SQ + "https://eapps.ncdot.gov/services/traffic-prod/v1/incidents/" + SQ + " + id)")
b1.append("            .then(r => r.ok ? r.json() : null)")
b1.append("            .catch(() => null)")
b1.append("        )")
b1.append("      );")
b1.append("      results.forEach(r => {{ if (r) allIncidents.push(r); }});")
b1.append("    }}")
b1.append("    ")
b1.append("    // Map incidents to days based on county")
b1.append("    for (const [dayStr, countyIds] of Object.entries(ROUTE_COUNTIES)) {{")
b1.append("      const dayNum = parseInt(dayStr);")
b1.append("      if (countyIds.length === 0) continue;")
b1.append("      const relevant = allIncidents.filter(inc => ")
b1.append("        inc.county && countyIds.includes(inc.county.id) && inc.condition === " + SQ + "Road Closed" + SQ)
b1.append("      );")
b1.append("      if (relevant.length > 0) {{")
b1.append("        liveClosures[dayNum] = relevant.map(inc => ({{")
b1.append("          road: (inc.road ? (inc.road.commonName || inc.road.name) : " + SQ + "Unknown" + SQ + "),")
b1.append("          status: inc.condition || " + SQ + "Closed" + SQ + ",")
b1.append("          reason: inc.reason || inc.location || " + SQ + "Road closure reported" + SQ)
b1.append("        }}));")
b1.append("      }}")
b1.append("    }}")
b1.append("    ")
b1.append("    roadDataTimestamp = new Date().toLocaleString();")
b1.append("    console.log(" + SQ + "NCDOT closures loaded:" + SQ + ", Object.keys(liveClosures).length, " + SQ + "days affected" + SQ + ");")
b1.append("  }} catch (err) {{")
b1.append("    console.warn(" + SQ + "NCDOT fetch failed:" + SQ + ", err);")
b1.append("  }}")
b1.append("}}")
b1.append("")
b1.append("async function fetchBRPAlerts() {{")
b1.append("  try {{")
b1.append("    const res = await fetch(" + SQ + "https://developer.nps.gov/api/v1/alerts?parkCode=blri&api_key=DEMO_KEY" + SQ + ");")
b1.append("    if (!res.ok) throw new Error(" + SQ + "NPS API error" + SQ + ");")
b1.append("    const data = await res.json();")
b1.append("    liveBRPAlerts = (data.data || []).map(alert => ({{")
b1.append("      title: alert.title,")
b1.append("      description: alert.description,")
b1.append("      category: alert.category,")
b1.append("      url: alert.url || " + SQ + "https://www.nps.gov/blri/planyourvisit/roadclosures.htm" + SQ)
b1.append("    }}));")
b1.append("    console.log(" + SQ + "BRP alerts loaded:" + SQ + ", liveBRPAlerts.length);")
b1.append("  }} catch (err) {{")
b1.append("    console.warn(" + SQ + "NPS BRP fetch failed:" + SQ + ", err);")
b1.append("  }}")
b1.append("}}")
b1.append("")

block1_str = NL.join(b1)
live_api_block = block1_str + NL + weather_marker
content = content.replace(weather_marker, live_api_block)
print("  [1/4] Added live road conditions API section")

# Step 2: Add data-road-section attribute
old_div_marker = "html += " + chr(96) + "<div style=" + chr(92) + chr(34) + "margin-top:10px;border-top:1px solid #bbf7d0;padding-top:10px;" + chr(92) + chr(34) + ">" + chr(96)
new_div_marker = "html += " + chr(96) + "<div data-road-section=" + chr(92) + chr(34) + "true" + chr(92) + chr(34) + " style=" + chr(92) + chr(34) + "margin-top:10px;border-top:1px solid #bbf7d0;padding-top:10px;" + chr(92) + chr(34) + ">" + chr(96)
if old_div_marker not in content:
    print("ERROR: Road conditions div not found")
    print("  Looking for:", repr(old_div_marker))
    idx = content.find("Road Conditions")
    if idx >= 0:
        print("  Nearby:", repr(content[max(0,idx-150):idx+30]))
    sys.exit(1)
content = content.replace(old_div_marker, new_div_marker)
print("  [2/4] Added data-road-section attribute")

# Step 3: Add enhanceRoadConditions function
inject_end = ("  }});" + NL + "}}" + NL + NL + NL +
    "  // " + "="*44 + NL +
    "  // REORDER: Days first, then reference sections" + NL +
    "  // " + "="*44)
if inject_end not in content:
    print("ERROR: inject end marker not found")
    sys.exit(1)
print("  Found inject end marker")

ef = []
ef.append("  }});")
ef.append("}}")
ef.append("")
ef.append("function enhanceRoadConditions() {{")
ef.append("  // Find all road sections")
ef.append("  const roadSections = document.querySelectorAll(" + SQ + "[data-road-section]" + SQ + ");")
ef.append("  if (!roadSections.length) return;")
ef.append("  ")
ef.append("  roadSections.forEach((roadSection) => {{")
ef.append("    // Determine day number from the parent weather panel")
ef.append("    const panel = roadSection.closest(" + SQ + ".weather-panel" + SQ + ");")
ef.append("    if (!panel) return;")
ef.append("    const allPanels = Array.from(document.querySelectorAll(" + SQ + ".weather-panel" + SQ + "));")
ef.append("    const dayNum = allPanels.indexOf(panel) + 1;")
ef.append("    if (dayNum < 1) return;")
ef.append("    ")
ef.append("    // Add live NCDOT closures")
ef.append("    if (liveClosures[dayNum]) {{")
ef.append("      const liveDiv = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("      liveDiv.style.cssText = " + SQ + "margin-bottom:6px;" + SQ + ";")
ef.append("      liveDiv.innerHTML = " + SQ + "<div style=" + chr(34) + "font-size:0.78em;font-weight:600;color:#B45309;margin-bottom:3px;" + chr(34) + ">" + RED + " Live Road Closures (NCDOT):</div>" + SQ + ";")
ef.append("      for (const c of liveClosures[dayNum]) {{")
ef.append("        const el = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("        el.style.cssText = " + SQ + "font-size:0.82em;color:#DC2626;margin-bottom:2px;" + SQ + ";")
ef.append("        el.textContent = " + SQ + NOENTRY + " " + SQ + " + c.road + " + SQ + ": " + SQ + " + c.status + " + SQ + " " + EMDASH + " " + SQ + " + c.reason;")
ef.append("        liveDiv.appendChild(el);")
ef.append("      }}")
ef.append("      roadSection.insertBefore(liveDiv, roadSection.children[1]);")
ef.append("    }}")
ef.append("    ")
ef.append("    // Add live BRP alerts for BRP days")
ef.append("    if ([6,7,8,10].includes(dayNum) && liveBRPAlerts.length > 0) {{")
ef.append("      const brpDiv = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("      brpDiv.style.cssText = " + SQ + "margin-bottom:6px;" + SQ + ";")
ef.append("      brpDiv.innerHTML = " + SQ + "<div style=" + chr(34) + "font-size:0.78em;font-weight:600;color:#B45309;margin-bottom:3px;" + chr(34) + ">" + RED + " Live BRP Alerts (NPS):</div>" + SQ + ";")
ef.append("      for (const alert of liveBRPAlerts) {{")
ef.append("        const el = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("        el.style.cssText = " + SQ + "font-size:0.82em;color:#DC2626;margin-bottom:2px;" + SQ + ";")
ef.append("        el.textContent = (alert.category === " + SQ + "Park Closure" + SQ + " ? " + SQ + NOENTRY + " " + SQ + " : " + SQ + WARN + " " + SQ + ") + alert.title;")
ef.append("        brpDiv.appendChild(el);")
ef.append("      }}")
ef.append("      const linkEl = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("      linkEl.style.cssText = " + SQ + "font-size:0.75em;margin-top:2px;" + SQ + ";")
ef.append("      linkEl.innerHTML = " + SQ + "<a href=" + chr(34) + "https://www.nps.gov/blri/planyourvisit/roadclosures.htm" + chr(34) + " target=" + chr(34) + "_blank" + chr(34) + " style=" + chr(34) + "color:#15803d;" + chr(34) + ">View full BRP closure details " + ARROW + "</a>" + SQ + ";")
ef.append("      brpDiv.appendChild(linkEl);")
ef.append("      ")
ef.append("      // Find existing BRP section or append")
ef.append("      const existingBRP = Array.from(roadSection.querySelectorAll(" + SQ + "div" + SQ + ")).find(d => d.textContent.includes(" + SQ + "Blue Ridge Parkway" + SQ + "));")
ef.append("      if (existingBRP) {{")
ef.append("        roadSection.insertBefore(brpDiv, existingBRP);")
ef.append("      }} else {{")
ef.append("        roadSection.appendChild(brpDiv);")
ef.append("      }}")
ef.append("    }}")
ef.append("    ")
ef.append("    // Add timestamp")
ef.append("    if (roadDataTimestamp) {{")
ef.append("      let ts = roadSection.querySelector(" + SQ + ".road-timestamp" + SQ + ");")
ef.append("      if (!ts) {{")
ef.append("        ts = document.createElement(" + SQ + "div" + SQ + ");")
ef.append("        ts.className = " + SQ + "road-timestamp" + SQ + ";")
ef.append("        ts.style.cssText = " + SQ + "font-size:0.7em;color:#999;margin-top:6px;font-style:italic;" + SQ + ";")
ef.append("        roadSection.appendChild(ts);")
ef.append("      }}")
ef.append("      ts.textContent = " + SQ + "Live data updated: " + SQ + " + roadDataTimestamp;")
ef.append("    }}")
ef.append("  }});")
ef.append("}}")
ef.append("")
ef.append("")
ef.append("  // " + "="*44)
ef.append("  // REORDER: Days first, then reference sections")
ef.append("  // " + "="*44)

enhance_block = NL.join(ef)
content = content.replace(inject_end, enhance_block)
print("  [3/4] Added enhanceRoadConditions() function")

# Step 4: Add setTimeout for live data fetching
old_timeout = "setTimeout(injectWeatherPanels, 500);"
new_timeout = NL.join([
    "setTimeout(injectWeatherPanels, 500);",
    "",
    "setTimeout(async function() {{",
    "  await Promise.all([fetchNCDOTClosures(), fetchBRPAlerts()]);",
    "  enhanceRoadConditions();",
    "}}, 1500);",
])
if old_timeout not in content:
    print("ERROR: setTimeout not found")
    sys.exit(1)
content = content.replace(old_timeout, new_timeout)
print("  [4/4] Added setTimeout for live data fetching")

if content == original:
    print("ERROR: No changes made")
    sys.exit(1)

with open(srcpath, "w", encoding="utf-8") as fh:
    fh.write(content)

checks = [
    ("ROUTE_COUNTIES", "Live road API constants"),
    ("fetchNCDOTClosures", "NCDOT fetch function"),
    ("fetchBRPAlerts", "BRP alerts fetch function"),
    ("data-road-section", "data-road-section attribute"),
    ("enhanceRoadConditions", "enhanceRoadConditions function"),
    ("fetchNCDOTClosures(), fetchBRPAlerts()", "setTimeout live fetch call"),
]
all_ok = True
for marker, desc in checks:
    if marker not in content:
        print(f"  VERIFY FAIL: {desc} not found")
        all_ok = False
    else:
        print(f"  VERIFY OK: {desc}")

if all_ok:
    print()
    print("SUCCESS: All 4 modifications applied and verified.")
else:
    print()
    print("ERROR: Some verifications failed.")
    sys.exit(1)

# Copy this script as fix_live_roads.py
import shutil
fix_path = os.path.join(basedir, "fix_live_roads.py")
shutil.copy2(os.path.abspath(__file__), fix_path)
print("Copied script to", fix_path)
