"""Fix countdown and confidence to use calendar date comparison instead of raw milliseconds."""

with open('create_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix countdown — use calendar dates, not millisecond math
old_countdown = """// Trip countdown (Eastern Time)
(function() {{
  function easternNow() {{
    return new Date(new Date().toLocaleString('en-US', {{timeZone: 'America/New_York'}}));
  }}
  // Trip dates in Eastern Time (March 11-22 is EDT, UTC-4)
  var tripStart = new Date('2026-03-11T00:00:00-04:00');
  var tripEnd = new Date('2026-03-22T23:59:59-04:00');
  var el = document.getElementById('trip-countdown');
  if (!el) return;

  function update() {{
    var now = easternNow();
    if (now < tripStart) {{
      var diff = tripStart - now;
      var days = Math.floor(diff / 86400000);
      var hours = Math.floor((diff % 86400000) / 3600000);
      if (days === 0) {{
        el.innerHTML = 'Trip starts in <span class="count-num">' + hours + '</span> hour' + (hours !== 1 ? 's' : '') + '!';
      }} else if (days === 1) {{
        el.innerHTML = '<span class="count-num">Tomorrow!</span> Trip starts in <span class="count-num">1</span> day';
      }} else {{
        el.innerHTML = '<span class="count-num">' + days + '</span> day' + (days !== 1 ? 's' : '') + ' until adventure begins';
      }}
    }} else if (now <= tripEnd) {{
      var dayNum = Math.floor((now - tripStart) / 86400000) + 1;
      var daysLeft = 12 - dayNum;
      el.className = 'countdown-banner trip-active';
      el.innerHTML = '\xf0\x9f\x9a\x97 Day <span class="count-num">' + dayNum + '</span> of 12 \xe2\x80\x94 ' + (daysLeft > 0 ? daysLeft + ' day' + (daysLeft !== 1 ? 's' : '') + ' remaining' : 'Final day!');
    }} else {{
      el.className = 'countdown-banner trip-over';"""

new_countdown = """// Trip countdown (Eastern Time, calendar date math)
(function() {{
  function easternNow() {{
    return new Date(new Date().toLocaleString('en-US', {{timeZone: 'America/New_York'}}));
  }}
  // Compare calendar dates to avoid DST and time-of-day errors
  function calendarDaysBetween(from, to) {{
    var a = new Date(from.getFullYear(), from.getMonth(), from.getDate());
    var b = new Date(to.getFullYear(), to.getMonth(), to.getDate());
    return Math.round((b - a) / 86400000);
  }}
  var startYear = 2026, startMonth = 2, startDay = 11; // March 11
  var tripDays = 12;
  var el = document.getElementById('trip-countdown');
  if (!el) return;

  function update() {{
    var now = easternNow();
    var tripStartDate = new Date(startYear, startMonth, startDay);
    var tripEndDate = new Date(startYear, startMonth, startDay + tripDays - 1);
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var days = calendarDaysBetween(today, tripStartDate);
    if (days > 0) {{
      // Before trip
      var diff = new Date(startYear, startMonth, startDay, 0, 0, 0) - now;
      var hours = Math.max(0, Math.floor(diff / 3600000));
      if (days === 1 && hours < 24) {{
        el.innerHTML = '<span class="count-num">Tomorrow!</span> Trip starts in <span class="count-num">1</span> day';
      }} else if (days === 0 || (days === 1 && hours === 0)) {{
        el.innerHTML = 'Trip starts in <span class="count-num">' + Math.max(1, hours) + '</span> hour' + (hours !== 1 ? 's' : '') + '!';
      }} else {{
        el.innerHTML = '<span class="count-num">' + days + '</span> day' + (days !== 1 ? 's' : '') + ' until adventure begins';
      }}
    }} else if (today <= tripEndDate) {{
      // During trip
      var dayNum = calendarDaysBetween(tripStartDate, today) + 1;
      var daysLeft = tripDays - dayNum;
      el.className = 'countdown-banner trip-active';
      el.innerHTML = '\xf0\x9f\x9a\x97 Day <span class="count-num">' + dayNum + '</span> of ' + tripDays + ' \xe2\x80\x94 ' + (daysLeft > 0 ? daysLeft + ' day' + (daysLeft !== 1 ? 's' : '') + ' remaining' : 'Final day!');
    }} else {{
      el.className = 'countdown-banner trip-over';"""

if old_countdown in content:
    content = content.replace(old_countdown, new_countdown)
    print("Fixed countdown to use calendar date comparison")
else:
    # Try with the actual emoji chars
    print("Trying alternate match...")
    # Let's find the block another way
    import re
    # Match from "// Trip countdown" to "countdown-banner trip-over"
    pattern = r"// Trip countdown.*?el\.className = 'countdown-banner trip-over';"
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        print(f"Found {len(matches)} match(es) via regex")
        # Just do a line-by-line approach
    else:
        print("ERROR: Could not find countdown block at all")

# 2. Fix getConfidence — use calendar date comparison too
old_conf = """function getConfidence(dateStr, tempSpread) {{
  // Use Eastern Time for day calculations
  var eastern = new Date(new Date().toLocaleString('en-US', {{timeZone: 'America/New_York'}}));
  eastern.setHours(0,0,0,0);
  var parts = dateStr.split('-');
  var target = new Date(parts[0], parts[1] - 1, parts[2]);
  target.setHours(0,0,0,0);
  var daysOut = Math.round((target - eastern) / 86400000);"""

new_conf = """function getConfidence(dateStr, tempSpread) {{
  // Use Eastern Time calendar dates for accurate day count
  var en = new Date(new Date().toLocaleString('en-US', {{timeZone: 'America/New_York'}}));
  var today = new Date(en.getFullYear(), en.getMonth(), en.getDate());
  var parts = dateStr.split('-');
  var target = new Date(parts[0], parts[1] - 1, parts[2]);
  var daysOut = Math.round((target - today) / 86400000);"""

if old_conf in content:
    content = content.replace(old_conf, new_conf)
    print("Fixed getConfidence to use calendar date comparison")
else:
    print("WARNING: Could not find getConfidence block")

with open('create_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
