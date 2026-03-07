import re

path = r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define lodging lines for each day
lodging = {
    1: '\U0001f3e8 **Lodging:** Holiday Inn Express Savannah \u2014 [Booking & Check-in Info](https://www.ihg.com/holidayinnexpress/hotels/us/en/savannah/savex/hoteldetail)',
    2: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    3: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    4: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    5: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    6: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    7: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    8: '\U0001f3e1 **Lodging:** Barefoot Lodge at Dix Creek (Candler) \u2014 [VRBO Property & Check-in](https://www.vrbo.com/2185348)',
    9: '\U0001f3e1 **Lodging:** Mountainaire Inn & Log Cabins (Blowing Rock) \u2014 [Property Info](https://www.mountainaireinn.com/)',
    10: '\U0001f3e1 **Lodging:** Mountainaire Inn & Log Cabins (Blowing Rock) \u2014 [Property Info](https://www.mountainaireinn.com/)',
    11: '\U0001f3e8 **Lodging:** Holiday Inn Express Savannah \u2014 [Booking & Check-in Info](https://www.ihg.com/holidayinnexpress/hotels/us/en/savannah/savex/hoteldetail)',
    12: '\U0001f3e0 **Home day** \u2014 no lodging needed!',
}

lines = content.split('\n')
new_lines = []
i = 0
count = 0

while i < len(lines):
    new_lines.append(lines[i])
    # Check if this is a Day heading
    m = re.match(r'^## Day (\d+)\b', lines[i])
    if m:
        day_num = int(m.group(1))
        if day_num in lodging:
            # Look at the next line
            i += 1
            if i < len(lines):
                next_line = lines[i]
                if next_line.strip() == '':
                    # Empty line after heading (Days 4,5,6,7,8,9,10,11 pattern)
                    # Insert lodging after the empty line
                    new_lines.append(next_line)  # keep the empty line
                    new_lines.append(lodging[day_num])
                    new_lines.append('')
                    count += 1
                else:
                    # There's a subtitle line right after the heading
                    new_lines.append(next_line)  # add the subtitle line
                    new_lines.append('')
                    new_lines.append(lodging[day_num])
                    count += 1
            continue
    i += 1

content = '\n'.join(new_lines)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Added lodging links to {count} days')
