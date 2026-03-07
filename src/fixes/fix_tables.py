#!/usr/bin/env python3
"""
fix_tables.py — Reconcile city, county, and school district names
across all three location tables in the road trip plan markdown.
"""

import re

FILE = r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# ─────────────────────────────────────────────────────────────────────
# TABLE 1: Land Scouting — Add "School District" column
# ─────────────────────────────────────────────────────────────────────

old_table1_header = "| County | Town/Area | Avg $/Acre | Elevation | Water | Schools (Niche) | Notes |"
new_table1_header = "| County | Town/Area | School District | Avg $/Acre | Elevation | Water | Schools (Niche) | Notes |"

old_table1_sep = "|---|---|---|---|---|---|---|"
new_table1_sep = "|---|---|---|---|---|---|---|---|"

# Row replacements: insert school district after Town/Area
table1_rows = [
    (
        "| **Yancey** | Burnsville, South Toe | ~$10–15K |",
        "| **Yancey** | Burnsville, South Toe | Yancey County Schools | ~$10–15K |",
    ),
    (
        "| **Madison** | Marshall, Hot Springs | ~$8–15K |",
        "| **Madison** | Marshall, Hot Springs | Madison County Schools | ~$8–15K |",
    ),
    (
        "| **Mitchell** | Spruce Pine, Bakersville | ~$8–12K |",
        "| **Mitchell** | Spruce Pine, Bakersville | Mitchell County Schools | ~$8–12K |",
    ),
    (
        "| **McDowell** | Marion, Old Fort | ~$6.5–9K |",
        "| **McDowell** | Marion, Old Fort | McDowell County Schools | ~$6.5–9K |",
    ),
    (
        "| **Burke** | Morganton area | ~$6.5–9K |",
        "| **Burke** | Morganton area | Burke County Schools | ~$6.5–9K |",
    ),
    (
        "| **Avery** | Banner Elk, Elk Park | ~$15–25K |",
        "| **Avery** | Banner Elk, Elk Park | Avery County Schools | ~$15–25K |",
    ),
]

# Apply Table 1 changes
for old, new in [(old_table1_header, new_table1_header),
                  (old_table1_sep, new_table1_sep)] + table1_rows:
    if old in content:
        content = content.replace(old, new, 1)
        changes += 1
    else:
        print(f"WARNING: Could not find Table 1 text: {old[:60]}...")

# ─────────────────────────────────────────────────────────────────────
# School verdict line — change "5–8 year old" to "8 year old"
# ─────────────────────────────────────────────────────────────────────

old_verdict = "and it does with a 5–8 year old),"
new_verdict = "and it does with an 8 year old),"

# Also try the en-dash variant
old_verdict_alt = "and it does with a 5\u20138 year old),"

if old_verdict in content:
    content = content.replace(old_verdict, new_verdict, 1)
    changes += 1
elif old_verdict_alt in content:
    content = content.replace(old_verdict_alt, new_verdict, 1)
    changes += 1
else:
    print(f"WARNING: Could not find school verdict text")

# ─────────────────────────────────────────────────────────────────────
# TABLE 2: School comparison — Add City/Town and School District columns
# ─────────────────────────────────────────────────────────────────────

old_table2_header = "| County | District Grade | Middle School | High School | Notes |"
new_table2_header = "| County | City/Town | School District | District Grade | Middle School | High School | Notes |"

old_table2_sep = "|---|---|---|---|---|"
new_table2_sep = "|---|---|---|---|---|---|---|"

table2_rows = [
    (
        "| **Buncombe** (Asheville, Black Mtn, Weaverville) | **A-** |",
        "| **Buncombe** | Asheville, Black Mtn, Weaverville | Buncombe County Schools | **A-** |",
    ),
    (
        "| **Henderson** (Hendersonville) | **B+** |",
        "| **Henderson** | Hendersonville | Henderson County Schools | **B+** |",
    ),
    (
        "| **Watauga** (Boone, Blowing Rock) | **A-** |",
        "| **Watauga** | Boone, Blowing Rock | Watauga County Schools | **A-** |",
    ),
    (
        "| **Transylvania** (Brevard) | **B+** |",
        "| **Transylvania** | Brevard | Transylvania County Schools | **B+** |",
    ),
]

# We need to be careful with the separator — Table 2's separator "|---|---|---|---|---|"
# is a substring of Table 1's new separator. So we match contextually.
# Replace Table 2 header first, then find the separator immediately after it.

if old_table2_header in content:
    content = content.replace(old_table2_header, new_table2_header, 1)
    changes += 1
else:
    print(f"WARNING: Could not find Table 2 header")

# For the separator, find it after the new Table 2 header position
t2_header_pos = content.find(new_table2_header)
if t2_header_pos >= 0:
    # Find the separator that comes right after Table 2 header
    after_header = content[t2_header_pos + len(new_table2_header):]
    sep_pos = after_header.find(old_table2_sep)
    if sep_pos is not None and sep_pos < 5:  # Should be on the very next line
        abs_pos = t2_header_pos + len(new_table2_header) + sep_pos
        content = content[:abs_pos] + new_table2_sep + content[abs_pos + len(old_table2_sep):]
        changes += 1
    else:
        print(f"WARNING: Could not find Table 2 separator near header")

for old, new in table2_rows:
    if old in content:
        content = content.replace(old, new, 1)
        changes += 1
    else:
        print(f"WARNING: Could not find Table 2 row: {old[:60]}...")

# ─────────────────────────────────────────────────────────────────────
# TABLE 3: Scouting Summary — Replace Schools row with County +
#           School District + Schools (Grade) rows
# ─────────────────────────────────────────────────────────────────────

old_table3_schools = "| **Schools** | Buncombe Co. | Henderson Co. | Buncombe Co. | Transylvania Co. (above avg) | Buncombe Co. | Watauga Co. |"

new_table3_rows = (
    "| **County** | Buncombe | Henderson | Buncombe | Transylvania | Buncombe | Watauga |\n"
    "| **School District** | Buncombe County Schools | Henderson County Schools | Buncombe County Schools | Transylvania County Schools | Buncombe County Schools | Watauga County Schools |\n"
    "| **Schools (Grade)** | Buncombe Co. (A-) | Henderson Co. (B+) | Buncombe Co. (A-) | Transylvania Co. (B+, above avg) | Buncombe Co. (A-) | Watauga Co. (A-) |"
)

if old_table3_schools in content:
    content = content.replace(old_table3_schools, new_table3_rows, 1)
    changes += 1
else:
    print(f"WARNING: Could not find Table 3 Schools row")

# ─────────────────────────────────────────────────────────────────────
# Write result
# ─────────────────────────────────────────────────────────────────────

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. {changes} replacements made in {FILE}")
