html_file = "C:/Users/AB Digial/OneDrive/Documents/Claude/road-trip-plan.html"

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

count = 0

def lnk(url, text):
    return "<a href=\"" + url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + text + "</a>"

fixes = [
    # Carl Sandburg Home - table cells and heading
    ("Carl Sandburg Home (Flat Rock)", lnk("https://www.nps.gov/carl", "Carl Sandburg Home") + " (Flat Rock)"),
    ("Carl Sandburg Home Trails (Flat Rock)", lnk("https://www.nps.gov/carl", "Carl Sandburg Home") + " Trails (Flat Rock)"),
    ("Carl Sandburg Home &rarr;", lnk("https://www.nps.gov/carl", "Carl Sandburg Home") + " &rarr;"),

    # Chimney Rock State Park - table cells and heading
    ("Chimney Rock State Park</td>", lnk("https://www.chimneyrockpark.com", "Chimney Rock State Park") + "</td>"),
    ("HIKE &mdash; Chimney Rock State Park:", "HIKE &mdash; " + lnk("https://www.chimneyrockpark.com", "Chimney Rock State Park") + ":"),

    # DuPont - link to forest website
    ("<strong>DuPont Waterfalls</strong>", "<strong>" + lnk("https://www.dupontstaterecreationalforest.com", "DuPont Waterfalls") + "</strong>"),

    # Wolf Museum - mark as permanently closed
    ("<strong>Wolf&rsquo;s Museum of Mystery</strong>", "<strong>Wolf&rsquo;s Museum of Mystery (PERMANENTLY CLOSED)</strong>"),
]

for old, new in fixes:
    if old in content:
        n = content.count(old)
        content = content.replace(old, new)
        count += n
        print("  Fixed: " + old[:50] + " (" + str(n) + ")")
    else:
        print("  SKIP: " + old[:50])

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("\nFixed " + str(count) + " additional references")
