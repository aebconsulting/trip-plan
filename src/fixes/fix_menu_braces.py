"""
Fix script: Correct brace escaping in the menu IIFE section of create_html.py.

Problem: Lines ~2065-2152 use quadruple braces {{{{ and }}}} for JS curly braces,
but since this is inside a Python f-string that only needs double braces {{ and }}
to produce single braces { and } in the output. Quadruple braces produce double
braces in the output, causing a JavaScript syntax error.

Fix: Replace {{{{ with {{ and }}}} with }} ONLY in the menu IIFE section.
The menuItems array (which already correctly uses {{ and }}) is left untouched.
"""

import re

FILE_PATH = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

# Read the file
with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Find the start marker: "// Body-appended dropdown menu with backdrop"
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if "// Body-appended dropdown menu with backdrop" in line:
        start_idx = i
        print(f"Found start marker at line {i + 1}: {line.rstrip()[:80]}")
        break

if start_idx is None:
    print("ERROR: Could not find start marker '// Body-appended dropdown menu with backdrop'")
    exit(1)

# Find the end marker: the "}})();" line that closes this IIFE
# It should be the first "}}}})" or similar pattern after the keydown listener
for i in range(start_idx, min(start_idx + 120, len(lines))):
    stripped = lines[i].strip()
    # The IIFE closing line: either "}}}})();" (broken) or "}})();" (fixed)
    if stripped in ("}}}})()", "}}}})();", "  }}}})();", "}})();", "  }})();"):
        # Check if this is the IIFE closing (not a nested one)
        # The IIFE close follows the keydown event listener
        # Look back a few lines for "keydown"
        for j in range(max(0, i - 10), i):
            if "keydown" in lines[j]:
                end_idx = i
                print(f"Found end marker at line {i + 1}: {lines[i].rstrip()[:80]}")
                break
        if end_idx is not None:
            break

if end_idx is None:
    print("ERROR: Could not find end marker for menu IIFE")
    exit(1)

# Now process ONLY lines between start_idx and end_idx (inclusive)
# But skip the menuItems array lines (which use {{ and }} correctly)
changes_made = 0
in_menu_items = False

for i in range(start_idx, end_idx + 1):
    line = lines[i]

    # Detect menuItems array boundaries to skip them
    if "var menuItems = [" in line:
        in_menu_items = True
        continue
    if in_menu_items:
        if line.strip() == "];" or line.strip() == "];":
            in_menu_items = False
        continue

    # Replace quadruple braces with double braces
    original = line
    # Replace {{{{ with {{ and }}}} with }}
    new_line = line.replace("{{{{", "{{").replace("}}}}", "}}")
    if new_line != original:
        lines[i] = new_line
        changes_made += 1
        print(f"  Fixed line {i + 1}: {original.rstrip()[:70]} -> {new_line.rstrip()[:70]}")

print(f"\nTotal lines changed: {changes_made}")

if changes_made == 0:
    print("WARNING: No changes were made. The file may already be fixed.")
else:
    # Write the file back
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"File written successfully: {FILE_PATH}")

    # Verify: re-read and check no quadruple braces remain in the section
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        verify_content = f.read()
    verify_lines = verify_content.split("\n")

    quad_open = 0
    quad_close = 0
    for i in range(start_idx, end_idx + 1):
        if "{{{{" in verify_lines[i]:
            quad_open += 1
        if "}}}}" in verify_lines[i]:
            quad_close += 1

    if quad_open == 0 and quad_close == 0:
        print("VERIFICATION PASSED: No quadruple braces remain in the menu IIFE section.")
    else:
        print(f"VERIFICATION FAILED: Still found {quad_open} '{{{{{{{{' and {quad_close} '}}}}}}}}' occurrences.")
