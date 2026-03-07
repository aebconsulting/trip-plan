#!/usr/bin/env python3
"""
fix_buildpanel.py - Fix the buildPanel() early return bug in create_html.py

Bug: Lines 1414-1418 have an early return when weather data is unavailable (!day && !night).
This prevents road conditions (lines 1468-1506) from ever rendering when there's no forecast.

Fix: Remove the early return, add default clothing for the no-forecast case,
and wrap the existing weather detail code in an else block.
"""

import sys
import os

FILE_PATH = r'C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py'

def main():
    # Read the file
    if not os.path.exists(FILE_PATH):
        print(f"ERROR: File not found: {FILE_PATH}")
        sys.exit(1)

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Read {len(lines)} lines from {FILE_PATH}")

    # Validate we're editing the right lines (1-indexed line numbers)
    # Line 1414 should start the if (!day && !night) block
    line_1414 = lines[1413].rstrip('\n')
    line_1415 = lines[1414].rstrip('\n')
    line_1416 = lines[1415].rstrip('\n')
    line_1417 = lines[1416].rstrip('\n')
    line_1418 = lines[1417].rstrip('\n')
    line_1420 = lines[1419].rstrip('\n')

    print(f"Line 1414: {line_1414!r}")
    print(f"Line 1415: {line_1415!r}")
    print(f"Line 1416: {line_1416!r}")
    print(f"Line 1417: {line_1417!r}")
    print(f"Line 1418: {line_1418!r}")
    print(f"Line 1420: {line_1420!r}")

    # Verify the content matches what we expect
    if '!day && !night' not in line_1414:
        print(f"ERROR: Line 1414 does not contain '!day && !night'. Got: {line_1414!r}")
        sys.exit(1)
    if 'return panel' not in line_1417:
        print(f"ERROR: Line 1417 does not contain 'return panel'. Got: {line_1417!r}")
        sys.exit(1)
    if 'const high' not in line_1420:
        print(f"ERROR: Line 1420 does not contain 'const high'. Got: {line_1420!r}")
        sys.exit(1)

    print("\nValidation passed. Applying fix...")

    # Build the new lines for the replacement
    # We replace lines 1414-1418 (0-indexed: 1413-1417) with the new if block (no early return)
    # Then insert "else {" before line 1420 (0-indexed: 1419)
    # Then insert closing "}" after line 1466 (0-indexed: 1465)

    # New replacement for lines 1414-1418 (the if block without early return)
    new_if_block = [
        '  if (!day && !night) {{\n',
        '    html += `<div style=\\"color:#666;font-style:italic;margin-bottom:8px;\\">Forecast available ~7 days before ${{dateStr}}</div>`;\n',
        '\n',
        '    // Default clothing for March in WNC when forecast not available\n',
        '    const defaultClothing = getClothingItems(55, 35, "Partly Cloudy", 8, dayNum);\n',
        '    if (defaultClothing.length > 0) {{\n',
        '      html += `<div style=\\"margin-top:8px;margin-bottom:10px;\\">`;\n',
        '      html += `<div style=\\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:6px;\\">\U0001F9E5 What to Pack (typical March conditions)</div>`;\n',
        '      html += `<div style=\\"display:flex;flex-wrap:wrap;gap:8px;\\">`;\n',
        '      for (const item of defaultClothing) {{\n',
        '        html += `<div style=\\"display:flex;flex-direction:column;align-items:center;width:52px;\\">`;\n',
        '        html += `<div style=\\"width:36px;height:36px;\\">${{item.icon}}</div>`;\n',
        '        html += `<span style=\\"font-size:0.7em;text-align:center;color:#333;margin-top:2px;\\">${{item.label}}</span>`;\n',
        '        html += `</div>`;\n',
        '      }}\n',
        '      html += `</div></div>`;\n',
        '    }}\n',
        '  }}\n',
    ]

    # Build the new file content
    new_lines = []

    # Lines 1-1413 (0-indexed: 0-1412) - unchanged
    new_lines.extend(lines[0:1413])

    # Lines 1414-1418 replaced with new if block
    new_lines.extend(new_if_block)

    # Blank line + else block opener before line 1420
    new_lines.append('\n')
    new_lines.append('  else {{\n')

    # Lines 1420-1466 (0-indexed: 1419-1465) - the weather details + clothing, now indented +2
    for i in range(1419, 1466):
        line = lines[i]
        # Add 2 spaces of indentation to each non-empty line
        if line.strip():
            new_lines.append('  ' + line)
        else:
            new_lines.append(line)

    # Close the else block
    new_lines.append('  }}\n')

    # Lines 1467 onward (0-indexed: 1466+) - unchanged (road conditions and rest)
    new_lines.extend(lines[1466:])

    # Write the modified file
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    new_total = len(new_lines)
    print(f"\nSUCCESS: File written with {new_total} lines (was {len(lines)} lines)")
    print(f"Changes made:")
    print(f"  - Replaced lines 1414-1418: removed early return, added default clothing for March")
    print(f"  - Wrapped lines 1420-1466 in else block (weather details + clothing)")
    print(f"  - Road conditions (after line 1466) now ALWAYS execute regardless of forecast availability")

    # Verify the fix by reading back and checking key lines
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        verify_lines = f.readlines()

    print(f"\nVerification - checking key sections of modified file:")

    # Find the if (!day && !night) line
    found_if = False
    found_else = False
    found_road = False
    for i, line in enumerate(verify_lines):
        if '!day && !night' in line:
            found_if = True
            print(f"  Line {i+1}: {line.rstrip()}")
        if 'else {{' in line and found_if and not found_else:
            found_else = True
            print(f"  Line {i+1}: {line.rstrip()}")
        if 'Road Conditions' in line:
            found_road = True
            print(f"  Line {i+1}: {line.rstrip()}")

    # Check that no 'return panel' exists between the if block and road conditions
    in_if_block = False
    early_return_found = False
    for i, line in enumerate(verify_lines):
        if '!day && !night' in line:
            in_if_block = True
        if in_if_block and 'Road Conditions' in line:
            break
        if in_if_block and 'return panel' in line:
            early_return_found = True
            print(f"  WARNING: Early return still present at line {i+1}")

    if not early_return_found:
        print("  VERIFIED: No early return before road conditions")
    if found_if and found_else and found_road:
        print("  VERIFIED: if/else structure and road conditions all present")


if __name__ == '__main__':
    main()
