#!/usr/bin/env python3
"""Fix script: Add phone numbers to lodging lines in the trip plan markdown."""

import os

PLAN_PATH = os.path.expanduser(r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md")

replacements = [
    {
        "label": "Holiday Inn Express Savannah (Day 1 & Day 11)",
        "find": '🏨 **Lodging:** Holiday Inn Express Savannah — [Booking & Check-in Info](https://www.ihg.com/holidayinnexpress/hotels/us/en/savannah/savex/hoteldetail)',
        "replace": '🏨 **Lodging:** Holiday Inn Express Savannah — [Booking & Check-in Info](https://www.ihg.com/holidayinnexpress/hotels/us/en/savannah/savex/hoteldetail) | 📞 [(912) 231-9000](tel:9122319000)',
        "expected": 2,
    },
    {
        "label": "Barefoot Lodge at Dix Creek / VRBO (Days 2-8)",
        "find": '🏡 **Lodging:** Barefoot Lodge at Dix Creek (Candler) — [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
        "replace": '🏡 **Lodging:** Barefoot Lodge at Dix Creek (Candler) — [VRBO Property & Check-in](https://www.vrbo.com/2185348) | 📞 [(877) 228-3145](tel:8772283145)',
        "expected": 7,
    },
    {
        "label": "Mountainaire Inn & Log Cabins (Days 9-10)",
        "find": '🏡 **Lodging:** Mountainaire Inn & Log Cabins (Blowing Rock) — [Property Info](https://www.mountainaireinn.com/)',
        "replace": '🏡 **Lodging:** Mountainaire Inn & Log Cabins (Blowing Rock) — [Property Info](https://www.mountainaireinn.com/) | 📞 [(828) 295-3272](tel:8282953272)',
        "expected": 2,
    },
]

# Read
with open(PLAN_PATH, "r", encoding="utf-8") as f:
    content = f.read()

total = 0
for r in replacements:
    count = content.count(r["find"])
    print(f"[{r['label']}]  found {count} occurrence(s) (expected {r['expected']})")
    if count != r["expected"]:
        print(f"  WARNING: expected {r['expected']} but found {count}")
    content = content.replace(r["find"], r["replace"])
    total += count

# Write
with open(PLAN_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone — {total} total replacements written to {PLAN_PATH}")
