import json
import sys

html_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/road-trip-plan.html"
json_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/place_links.json"

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
        print("  Linked: " + name + " (" + str(n) + " occurrences)")
    else:
        print("  SKIP (not found or already linked): " + name)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("\nTotal: Updated " + str(count) + " place references with links")
