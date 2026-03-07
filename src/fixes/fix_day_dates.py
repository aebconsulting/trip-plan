"""fix_day_dates.py - Add dates to day section headers"""
import sys, base64

filepath = "C:/Users/AB Digial/OneDrive/Documents/Claude/create_html.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# Change 1: Replace JavaScript header code
OLD_JS_B64 = "ICAgIC8vIENsZWFuIHVwIHRoZSB0aXRsZQogICAgbGV0IHRpdGxlVGV4dCA9IGgyLnRleHRDb250ZW50CiAgICAgIC5yZXBsYWNlKC9EYXlcXHMrXFxkK1xccypbXFx1MjAxNFxcdTIwMTMtXVxccyovLCAnJykKICAgICAgLnJlcGxhY2UoL15bXjpdKzpcXHMqLywgJycpOwoKICAgIGhlYWRlci5pbm5lckhUTUwgPSAnPHNwYW4gY2xhc3M9ImRheS1udW1iZXIiPkRBWSAnICsgZGF5TnVtICsgJzwvc3Bhbj48c3BhbiBjbGFzcz0iZGF5LXRpdGxlIj4nICsgdGl0bGVUZXh0ICsgJzwvc3Bhbj4nOw=="
NEW_JS_B64 = "ICAgIC8vIEV4dHJhY3QgZGF0ZSBhbmQgdGl0bGUgZnJvbSBoZWFkaW5nIGxpa2UgIlR1ZXNkYXksIE1hcmNoIDExdGg6IERyaXZlIHRvIFNhdmFubmFoIgogICAgbGV0IGFmdGVyRGF5ID0gaDIudGV4dENvbnRlbnQucmVwbGFjZSgvRGF5XFxzK1xcZCtcXHMqW1xcdTIwMTRcXHUyMDEzLV1cXHMqLywgJycpOwogICAgbGV0IGRhdGVUZXh0ID0gJyc7CiAgICBsZXQgdGl0bGVUZXh0ID0gYWZ0ZXJEYXk7CiAgICBjb25zdCBjb2xvbklkeCA9IGFmdGVyRGF5LmluZGV4T2YoJzonKTsKICAgIGlmIChjb2xvbklkeCA+IC0xKSB7ewogICAgICBkYXRlVGV4dCA9IGFmdGVyRGF5LnN1YnN0cmluZygwLCBjb2xvbklkeCkudHJpbSgpOwogICAgICB0aXRsZVRleHQgPSBhZnRlckRheS5zdWJzdHJpbmcoY29sb25JZHggKyAxKS50cmltKCk7CiAgICB9fQoKICAgIGxldCBoZWFkZXJIdG1sID0gJzxzcGFuIGNsYXNzPSJkYXktbnVtYmVyIj5EQVkgJyArIGRheU51bSArICc8L3NwYW4+JzsKICAgIGlmIChkYXRlVGV4dCkge3sKICAgICAgaGVhZGVySHRtbCArPSAnPHNwYW4gY2xhc3M9ImRheS1kYXRlIj4nICsgZGF0ZVRleHQgKyAnPC9zcGFuPic7CiAgICB9fQogICAgaGVhZGVySHRtbCArPSAnPHNwYW4gY2xhc3M9ImRheS10aXRsZSI+JyArIHRpdGxlVGV4dCArICc8L3NwYW4+JzsKICAgIGhlYWRlci5pbm5lckhUTUwgPSBoZWFkZXJIdG1sOw=="
old_js = base64.b64decode(OLD_JS_B64).decode("utf-8")
new_js = base64.b64decode(NEW_JS_B64).decode("utf-8")

if old_js in content:
    content = content.replace(old_js, new_js, 1)
    changes += 1
    print("Change 1 (JavaScript): SUCCESS")
else:
    print("Change 1 (JavaScript): ERROR - old string not found")

# Change 2: Add .day-date CSS
css_anchor = "backdrop-filter: blur(8px);" + chr(10) + "  }}"
css_anchor_idx = content.find(css_anchor)
if css_anchor_idx > 0:
    insert_at = css_anchor_idx + len(css_anchor)
    day_date_css = chr(10)
    day_date_css += "  .day-date {{" + chr(10)
    day_date_css += "    font-family: 'Outfit', sans-serif;" + chr(10)
    day_date_css += "    font-size: 0.82em;" + chr(10)
    day_date_css += "    font-weight: 400;" + chr(10)
    day_date_css += "    opacity: 0.8;" + chr(10)
    day_date_css += "    white-space: nowrap;" + chr(10)
    day_date_css += "  }}"
    content = content[:insert_at] + day_date_css + content[insert_at:]
    changes += 1
    print("Change 2 (CSS .day-date): SUCCESS")
else:
    print("Change 2 (CSS .day-date): ERROR")

# Change 3: Add flex-wrap to .day-header
dh_idx = content.find(".day-header {{")
if dh_idx > 0:
    old_gap = "    gap: 16px;" + chr(10) + "    position: relative;"
    new_gap = "    gap: 16px;" + chr(10) + "    flex-wrap: wrap;" + chr(10) + "    position: relative;"
    gap_idx = content.find(old_gap, dh_idx)
    if gap_idx > 0 and gap_idx < dh_idx + 500:
        content = content[:gap_idx] + new_gap + content[gap_idx + len(old_gap):]
        changes += 1
        print("Change 3 (flex-wrap): SUCCESS")
    else:
        print("Change 3 (flex-wrap): ERROR - gap not found")
else:
    print("Change 3 (flex-wrap): ERROR - .day-header not found")

if changes == 3:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print()
    print("SUCCESS: All 3 changes applied.")
else:
    print()
    print(f"ERROR: Only {changes}/3 changes matched. File NOT modified.")
    sys.exit(1)
