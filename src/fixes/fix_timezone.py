"""Fix countdown and confidence calculations to use Eastern Time."""
import re

with open('create_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix getConfidence - use Eastern Time for "today" and "target"
old_conf = """function getConfidence(dateStr, tempSpread) {{
  var today = new Date();
  today.setHours(0,0,0,0);
  var target = new Date(dateStr + 'T00:00:00');
  var daysOut = Math.round((target - today) / 86400000);"""

new_conf = """function getConfidence(dateStr, tempSpread) {{
  // Use Eastern Time for day calculations
  var eastern = new Date(new Date().toLocaleString('en-US', {{timeZone: 'America/New_York'}}));
  eastern.setHours(0,0,0,0);
  var parts = dateStr.split('-');
  var target = new Date(parts[0], parts[1] - 1, parts[2]);
  target.setHours(0,0,0,0);
  var daysOut = Math.round((target - eastern) / 86400000);"""

if old_conf in content:
    content = content.replace(old_conf, new_conf)
    print("Fixed getConfidence to use Eastern Time")
else:
    print("WARNING: Could not find getConfidence block")

# 2. Fix countdown - use Eastern Time for tripStart, tripEnd, and now
old_countdown = """// Trip countdown
(function() {{
  var tripStart = new Date('2026-03-11T00:00:00');
  var tripEnd = new Date('2026-03-22T23:59:59');
  var el = document.getElementById('trip-countdown');
  if (!el) return;

  function update() {{
    var now = new Date();"""

new_countdown = """// Trip countdown (Eastern Time)
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
    var now = easternNow();"""

if old_countdown in content:
    content = content.replace(old_countdown, new_countdown)
    print("Fixed countdown to use Eastern Time")
else:
    print("WARNING: Could not find countdown block")

with open('create_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - all date calculations now use Eastern Time")
