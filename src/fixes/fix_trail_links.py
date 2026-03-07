import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

html_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/road-trip-plan.html"
json_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/trail_links.json"

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

count = 0

for item in data:
    name = item[0]
    url = item[1]
    old = "<strong>" + name + "</strong>"
    link_tag = "<a href=\"" + url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + name + "</a>"
    new_str = "<strong>" + link_tag + "</strong>"
    if old in content:
        n = content.count(old)
        content = content.replace(old, new_str)
        count += n
        print("Linked: " + name + " (" + str(n) + " occurrences)")
    else:
        print("SKIPPED (not found as simple strong): " + name)

# Handle special cases - trails in combined headings
# "HIKE \u2014 Glen Burney Falls Trail (Blowing Rock):" - the trail name is inside a larger strong
# Check for Glen Burney Falls Trail as part of a heading
special = [
    ["Glen Burney Falls Trail", "https://blueridgeconservancy.org/glen-burney-trail"],
    ["Bent Creek Trails", "https://www.fs.usda.gov/r08/northcarolina/recreation/trails/homestead-trail"],
    ["Lake Tomahawk", "https://www.townofblackmountain.org/Facilities/Facility/Details/Lake-Tomahawk-Park-5"],
]

for item in special:
    name = item[0]
    url = item[1]
    old = "<strong>" + name + "</strong>"
    link_tag = "<a href=\"" + url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + name + "</a>"
    new_str = "<strong>" + link_tag + "</strong>"
    if old in content:
        n = content.count(old)
        content = content.replace(old, new_str)
        count += n
        print("Linked (special): " + name + " (" + str(n) + " occurrences)")

# Handle Linville Falls appearing in headings like "Afternoon \u2014 Linville Falls + Rough Ridge:"
# These are inside larger <strong> tags so we need to target just the name within links context
# Skip these - they are in combined headings and harder to link without breaking HTML

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Done! Total trail references linked: " + str(count))
