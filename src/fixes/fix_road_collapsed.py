"""
Fix script: Make the Road Conditions section start collapsed like all other sections.
Changes 'collapsed: false' to 'collapsed: true' for Road Condition Alerts in create_html.py.
"""

import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_html.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = "collapsed: false"
# Only replace in the Road Condition Alerts line
road_marker = "Road Condition Alerts"
idx = content.find(road_marker)
if idx >= 0:
    # Find 'collapsed: false' after this marker within the same line
    line_end = content.find("\n", idx)
    line = content[idx:line_end]
    if "collapsed: false" in line:
        new_line = line.replace("collapsed: false", "collapsed: true")
        content = content[:idx] + new_line + content[line_end:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Replaced 'collapsed: false' with 'collapsed: true' for Road Condition Alerts.")
    else:
        print("INFO: Road Condition Alerts line already has 'collapsed: true' or different format.")
else:
    print("WARNING: 'Road Condition Alerts' not found in the file.")
