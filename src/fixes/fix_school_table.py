#!/usr/bin/env python3
"""Fix script to add land scouting counties/cities to the School Comparison table."""

import os

plan_path = os.path.expanduser(r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md")

with open(plan_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the old text to find
old_text = """**For comparison — the "town" counties you're already scouting:**

| County | City/Town | School District | District Grade | Middle School | High School | Notes |
|---|---|---|---|---|---|---|
| **Buncombe** | Asheville, Black Mtn, Weaverville | Buncombe County Schools | **A-** | Multiple options, strong | Multiple options, strong | Largest district in WNC, 45 schools |
| **Henderson** | Hendersonville | Henderson County Schools | **B+** | Top 50% in NC | Multiple good options | 2nd largest in WNC |
| **Watauga** | Boone, Blowing Rock | Watauga County Schools | **A-** | Strong | Watauga HS: 65% math prof (vs 51% state avg) | Strong across the board |
| **Transylvania** | Brevard | Transylvania County Schools | **B+** | Above avg | 86% grad rate | Smaller, solid district |"""

# Define the new replacement text
new_text = """**All counties — town areas + land scouting areas:**

| County | City/Town | School District | District Grade | Middle School | High School | Notes |
|---|---|---|---|---|---|---|
| **Buncombe** | Asheville, Black Mtn, Weaverville | Buncombe County Schools | **A-** | Multiple options, strong | Multiple options, strong | Largest district in WNC, 45 schools |
| **Henderson** | Hendersonville | Henderson County Schools | **B+** | Top 50% in NC | Multiple good options | 2nd largest in WNC |
| **Watauga** | Boone, Blowing Rock | Watauga County Schools | **A-** | Strong | Watauga HS: 65% math prof (vs 51% state avg) | Strong across the board |
| **Transylvania** | Brevard | Transylvania County Schools | **B+** | Above avg | 86% grad rate | Smaller, solid district |
| **Yancey** | Burnsville, South Toe | Yancey County Schools | **B+** | **A-** (#147 in NC). 13:1 ratio | **B** | Top pick for land + schools |
| **Madison** | Marshall, Hot Springs | Madison County Schools | **B** | **A-** (#162 in NC) | Early College HS: **A** (#104 in NC). Regular: **C+** | Early College HS is a standout |
| **Mitchell** | Spruce Pine, Bakersville | Mitchell County Schools | **C** | **C\u2013D** | **C** | Schools are weaker |
| **McDowell** | Marion, Old Fort | McDowell County Schools | **C** | **C\u2013D** (mixed) | **C** | Schools below average |
| **Burke** | Morganton | Burke County Schools | **C+** | Mixed — some ok, some weak | Mixed | Beautiful scenery, affordable |
| **Avery** | Banner Elk, Elk Park | Avery County Schools | **B-** | Smaller schools | Smaller schools | Highest elevation, pricier |"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(plan_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: School comparison table updated with land scouting counties.")
else:
    print("ERROR: Could not find the expected text block in the plan file.")
    print("Attempting a more flexible search...")
    # Try to find a partial match for debugging
    search_key = '**For comparison \u2014 the "town" counties'
    if search_key in content:
        idx = content.index(search_key)
        print(f"Found header at position {idx}. Showing surrounding text:")
        print(repr(content[idx:idx+200]))
    else:
        print("Could not find even the header line.")
        # Try unicode variants
        for variant in ['**For comparison', 'town" counties', 'already scouting']:
            if variant in content:
                idx = content.index(variant)
                print(f"Found '{variant}' at position {idx}")
                print(repr(content[idx:idx+100]))
