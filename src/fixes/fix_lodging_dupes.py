import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
i = 0
removed = 0

while i < len(lines):
    # Check if this line is a lodging line
    if lines[i].startswith('\U0001f3e8 **Lodging:**') or lines[i].startswith('\U0001f3e1 **Lodging:**') or lines[i].startswith('\U0001f3e0 **Home day**'):
        new_lines.append(lines[i])
        # Check if the next line is a duplicate of the subtitle
        if i + 1 < len(lines) and len(new_lines) >= 3:
            subtitle_idx = len(new_lines) - 3
            if subtitle_idx >= 0:
                subtitle = new_lines[subtitle_idx]
                next_line = lines[i + 1]
                if next_line == subtitle and subtitle.strip() != '':
                    i += 2  # skip the duplicate line
                    removed += 1
                    continue
        i += 1
        continue
    new_lines.append(lines[i])
    i += 1

content = '\n'.join(new_lines)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Cleanup complete. Removed {removed} duplicate lines. Total lines: {len(new_lines)}")
