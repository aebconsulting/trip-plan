#!/usr/bin/env python3
"""Add a countdown timer to the hero header showing days until trip."""

SRC = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

with open(SRC, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add CSS for the countdown badge
countdown_css = """
  .countdown-badge {{
    display: inline-block;
    margin-top: 12px;
    padding: 8px 20px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
    font-weight: 500;
    letter-spacing: 0.3px;
    animation: pulse-glow 3s ease-in-out infinite;
  }}
  .countdown-badge .count-num {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.15em;
    color: #fbbf24;
  }}
  .countdown-badge.trip-active {{
    background: rgba(34,197,94,0.25);
    border-color: rgba(34,197,94,0.4);
  }}
  .countdown-badge.trip-active .count-num {{
    color: #4ade80;
  }}
  .countdown-badge.trip-over {{
    opacity: 0.6;
  }}
  @keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 8px rgba(251,191,36,0.15); }}
    50% {{ box-shadow: 0 0 16px rgba(251,191,36,0.3); }}
  }}
"""

# Insert CSS before the .menu-panel-header rule
anchor = '  .menu-panel-header {{'
code = code.replace(anchor, countdown_css + '\n' + anchor, 1)

# 2. Add the countdown HTML element after the route-badge
countdown_html = """  <div class="countdown-badge" id="trip-countdown"></div>"""
route_badge_line = '  <span class="route-badge">~2,250 mi &bull; Family of 3 &bull; Toyota Crown</span>'
code = code.replace(route_badge_line, route_badge_line + '\n' + countdown_html, 1)

# 3. Add the JS that calculates and updates the countdown
countdown_js = r"""
// Trip countdown
(function() {{
  var tripStart = new Date('2026-03-11T00:00:00');
  var tripEnd = new Date('2026-03-22T23:59:59');
  var el = document.getElementById('trip-countdown');
  if (!el) return;

  function update() {{
    var now = new Date();
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
      el.className = 'countdown-badge trip-active';
      el.innerHTML = '\uD83D\uDE97 Day <span class="count-num">' + dayNum + '</span> of 12 — ' + (daysLeft > 0 ? daysLeft + ' day' + (daysLeft !== 1 ? 's' : '') + ' remaining' : 'Final day!');
    }} else {{
      el.className = 'countdown-badge trip-over';
      el.innerHTML = 'Trip complete \u2014 what an adventure!';
    }}
  }}
  update();
  setInterval(update, 60000);
}})();
"""

# Insert the countdown JS before the closing </body> tag
# Find the openExternalLinksInNewTab script we added earlier and put it right before that
body_close = code.rfind('</body>')
insert_code = f'\n<script>{countdown_js}</script>\n'
code = code[:body_close] + insert_code + code[body_close:]

with open(SRC, "w", encoding="utf-8") as f:
    f.write(code)

print("Done — added trip countdown to hero header")
