import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

html_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/road-trip-plan.html"

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

count = 0

def lnk(url, text):
    return "<a href=\"" + url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + text + "</a>"

fixes = [
    ("Carl Sandburg Home \u2192", lnk("https://www.nps.gov/carl", "Carl Sandburg Home") + " \u2192"),
    ("HIKE \u2014 Chimney Rock State Park:", "HIKE \u2014 " + lnk("https://www.chimneyrockpark.com", "Chimney Rock State Park") + ":"),
]

for old, new in fixes:
    if old in content:
        n = content.count(old)
        content = content.replace(old, new)
        count += n
        print("  Fixed (" + str(n) + ")")
    else:
        print("  SKIP")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed " + str(count) + " more references")
