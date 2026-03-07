"""
Convert the road trip plan markdown to a stunning, mobile-friendly HTML file.
Design: "Mountain Trail Journal" — vintage national parks poster aesthetic
meets modern travel app. Distinctive typography, warm earth tones, mountain
silhouettes, and memorable visual design.
"""
import markdown
import re
import os

plan_path = r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md"
with open(plan_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# ============================================
# PRE-PROCESSING: Fix markdown table detection
# The markdown parser needs a blank line before tables.
# Many tables in our plan follow text lines without a blank line.
# ============================================
def ensure_blank_before_tables(md_text):
    """Insert blank lines before markdown tables that don't have them."""
    lines = md_text.split('\n')
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect start of a markdown table (header row with | separators)
        if stripped.startswith('|') and '|' in stripped[1:] and i > 0:
            prev = lines[i-1].strip()
            # If previous line is not blank, not a table row, and not a separator
            if prev and not prev.startswith('|') and not all(c in '-|: ' for c in prev):
                result.append('')  # Insert blank line
        result.append(line)
    return '\n'.join(result)

md_content = ensure_blank_before_tables(md_content)

# Remove implementation plan section (not for display)
if '## IMPLEMENTATION PLAN' in md_content:
    md_content = md_content[:md_content.index('## IMPLEMENTATION PLAN')].rstrip()



# Convert markdown to HTML with proper extensions
html_body = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'sane_lists', 'smarty']
)

# Fix checkboxes
html_body = html_body.replace('[x]', '&#9989;').replace('[ ]', '&#11036;')

# ============================================
# POST-PROCESSING: Fix common markdown issues
# ============================================

def fix_dash_lists(html):
    """Convert lines with '- ' prefix inside <p> tags into proper <ul><li> lists."""
    parts = re.split(r'(<p>.*?</p>)', html, flags=re.DOTALL)
    result = []
    for part in parts:
        if part.startswith('<p>') and '\n- ' in part or part.startswith('<p>- ') or part.startswith('<p>\n- '):
            inner = part[3:-4]
            lines = inner.split('\n')
            new_lines = []
            in_list = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('- '):
                    if not in_list:
                        new_lines.append('<ul>')
                        in_list = True
                    new_lines.append(f'<li>{stripped[2:]}</li>')
                else:
                    if in_list:
                        new_lines.append('</ul>')
                        in_list = False
                    if stripped:
                        new_lines.append(f'<p>{stripped}</p>')
            if in_list:
                new_lines.append('</ul>')
            result.append('\n'.join(new_lines))
        else:
            result.append(part)
    return ''.join(result)

html_body = fix_dash_lists(html_body)
html_body = re.sub(r'<br\s*/?>[\s]*- ', '</p><ul><li>', html_body)

# ============================================
# BUILD THE FULL HTML DOCUMENT
# ============================================

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>12-Day Family Road Trip: FL → NC Mountains</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  /* ===================================================
     MOUNTAIN TRAIL JOURNAL — Design System
     Vintage national parks meets modern travel app
     =================================================== */

  :root {{
    /* Earth-tone palette */
    --cream: #F6F1E9;
    --cream-dark: #EDE6D8;
    --parchment: #FAF7F2;
    --card-bg: #FFFFFF;
    --text: #2C2416;
    --text-muted: #7A7062;
    --text-light: #A39A8C;

    /* Forest greens */
    --forest: #1B4332;
    --forest-mid: #2D6A4F;
    --forest-light: #40916C;
    --sage: #E8F0E4;
    --sage-deep: #D4E4CE;

    /* Warm accents */
    --terracotta: #C75C24;
    --terracotta-light: #FFF0E6;
    --amber: #E6A817;
    --amber-light: #FFF8E1;
    --clay: #A0522D;

    /* Sky & water */
    --slate: #4A6FA5;
    --slate-light: #E8EEF6;
    --sky: #87CEEB;

    /* Functional */
    --warning-bg: #FFF3E0;
    --warning-border: #E65100;
    --info-bg: #E8F0E4;
    --info-border: #2D6A4F;
    --border: #DDD5C8;
    --border-light: #EAE4D9;

    /* Shadows & effects */
    --shadow-sm: 0 1px 3px rgba(44,36,22,0.06), 0 1px 2px rgba(44,36,22,0.04);
    --shadow-md: 0 4px 16px rgba(44,36,22,0.08), 0 2px 6px rgba(44,36,22,0.04);
    --shadow-lg: 0 12px 40px rgba(44,36,22,0.12), 0 4px 12px rgba(44,36,22,0.06);
    --shadow-glow: 0 0 0 3px rgba(199,92,36,0.15);

    /* Spacing */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 40px;
    --space-2xl: 64px;

    /* Radius */
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 20px;
    --radius-xl: 28px;
  }}

  /* ===== RESET & BASE ===== */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html {{ scroll-behavior: smooth; }}

  body {{
    font-family: 'Outfit', system-ui, sans-serif;
    font-weight: 400;
    line-height: 1.7;
    color: var(--text);
    background: var(--cream);
    max-width: 900px;
    margin: 0 auto;
    padding: 0 var(--space-md) var(--space-xl);
    font-size: 15px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }}

  /* Subtle paper texture overlay */
  body::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.025'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
  }}

  /* ===== NAVIGATION ===== */
  .nav-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(246,241,233,0.92);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    padding: 6px 12px;
    border-bottom: 1.5px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 5px;
  }}

  .nav-bar a {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 11px;
    border-radius: 6px;
    background: transparent;
    color: var(--forest);
    font-family: 'Outfit', sans-serif;
    font-size: 0.74em;
    font-weight: 600;
    text-decoration: none;
    border: none;
    transition: all 0.2s ease;
    letter-spacing: 0.01em;
    white-space: nowrap;
  }}
  .nav-bar a:hover, .nav-bar a:active {{
    background: var(--forest);
    color: var(--cream);
    transform: none;
    box-shadow: none;
  }}
  .nav-group {{
    display: contents;
  }}

  /* Dropdown menu */
  .menu-btn {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    background: var(--forest);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-size: 0.74em;
    font-weight: 600;
    border: none;
    cursor: pointer;
    letter-spacing: 0.01em;
    transition: all 0.2s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .menu-btn:hover {{
    background: var(--forest-mid);
    transform: none;
    box-shadow: none;
  }}
  .menu-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.25);
    z-index: 10000;
    animation: backdropIn 0.15s ease-out;
  }}
  @keyframes backdropIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
  }}
  .menu-panel {{
    position: fixed;
    width: 260px;
    max-height: 80vh;
    overflow-y: auto;
    background: var(--cream);
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2), 0 4px 16px rgba(0,0,0,0.1);
    z-index: 10001;
    border: 1px solid var(--border);
    padding: 0;
    animation: menuFadeIn 0.2s cubic-bezier(.4,0,.2,1);
  }}
  @keyframes menuFadeIn {{
    from {{ opacity: 0; transform: translateY(-6px) scale(0.97); }}
    to {{ opacity: 1; transform: translateY(0) scale(1); }}
  }}
  .menu-panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 14px 10px;
    font-family: 'Fraunces', serif;
    font-size: 0.85em;
    font-weight: 700;
    color: var(--forest);
    border-bottom: 1.5px solid var(--border);
    background: rgba(27,67,50,0.04);
  }}
  .menu-close {{
    background: none;
    border: none;
    font-size: 1.1em;
    color: var(--forest);
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 4px;
    line-height: 1;
    transition: background 0.15s;
  }}
  .menu-close:hover {{
    background: rgba(27,67,50,0.1);
  }}
  .menu-panel a {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 9px 14px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.8em;
    color: var(--text);
    text-decoration: none;
    transition: background 0.12s;
    border-radius: 0;
    border: none;
    margin: 0;
    background: transparent;
    border-bottom: 1px solid rgba(0,0,0,0.04);
  }}
  .menu-panel a:last-child {{
    border-bottom: none;
  }}
  .menu-panel a:hover {{
    background: rgba(27,67,50,0.06);
    color: var(--forest);
    transform: none;
    box-shadow: none;
  }}

  /* ===== HERO HEADER ===== */
  .hero {{
    position: relative;
    background: linear-gradient(170deg, #1B4332 0%, #2D6A4F 40%, #40916C 70%, #52B788 100%);
    color: var(--cream);
    padding: 48px 32px 80px;
    border-radius: var(--radius-xl);
    margin: var(--space-md) 0 var(--space-lg);
    text-align: center;
    box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255,255,255,0.1);
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 30% 20%, rgba(230,168,23,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 80%, rgba(135,206,235,0.1) 0%, transparent 50%);
    pointer-events: none;
  }}
  .hero-mountains {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 80px;
    pointer-events: none;
  }}
  .hero h1 {{
    font-family: 'Fraunces', 'Georgia', serif;
    font-optical-sizing: auto;
    font-size: 2em;
    font-weight: 800;
    margin: 0 0 12px;
    border: none;
    color: var(--cream);
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    letter-spacing: -0.02em;
    line-height: 1.15;
    position: relative;
    z-index: 1;
  }}
  .hero .subtitle {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.92em;
    font-weight: 400;
    opacity: 0.85;
    line-height: 1.6;
    position: relative;
    z-index: 1;
    letter-spacing: 0.01em;
  }}
  .hero .route-badge {{
    display: inline-block;
    margin-top: 16px;
    padding: 6px 20px;
    border: 1.5px solid rgba(255,255,255,0.35);
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75em;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
  }}

  /* ===== CARDS ===== */
  .card {{
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin: var(--space-md) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
  }}

  /* ===== COLLAPSIBLE SECTIONS ===== */
  details {{
    background: var(--card-bg);
    border-radius: var(--radius-md);
    margin: var(--space-md) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
  }}
  details[open] {{
    border-color: var(--forest-light);
    box-shadow: var(--shadow-md);
  }}
  summary {{
    padding: 16px 22px;
    cursor: pointer;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.05em;
    color: var(--forest);
    list-style: none;
    display: flex;
    align-items: center;
    gap: 12px;
    user-select: none;
    transition: all 0.25s;
    letter-spacing: -0.01em;
  }}
  summary:hover {{
    background: var(--sage);
    color: var(--forest);
  }}
  summary::before {{
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    border-right: 2.5px solid var(--terracotta);
    border-bottom: 2.5px solid var(--terracotta);
    transform: rotate(-45deg);
    transition: transform 0.3s cubic-bezier(.4,0,.2,1);
    flex-shrink: 0;
    margin-right: 2px;
  }}
  details[open] > summary::before {{
    transform: rotate(45deg);
  }}
  summary::-webkit-details-marker {{ display: none; }}
  .details-content {{
    padding: 4px 22px 22px;
    animation: slideDown 0.3s ease-out;
  }}
  @keyframes slideDown {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ===== DAY SECTIONS ===== */
  .day-section {{
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 0;
    margin: var(--space-lg) 0;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
    overflow: hidden;
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .day-section:hover {{
    box-shadow: var(--shadow-lg);
  }}

  .day-header {{
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-mid) 100%);
    color: var(--cream);
    padding: 18px 26px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    position: relative;
    overflow: hidden;
  }}
  .day-header::after {{
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 120px;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05));
    pointer-events: none;
  }}

  .day-number {{
    font-family: 'JetBrains Mono', monospace;
    background: rgba(255,255,255,0.12);
    border-radius: var(--radius-sm);
    padding: 5px 14px;
    font-size: 0.78em;
    font-weight: 500;
    white-space: nowrap;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
  }}
  .day-date {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.82em;
    font-weight: 400;
    opacity: 0.8;
    white-space: nowrap;
  }}
  .day-title {{
    font-family: 'Fraunces', serif;
    font-size: 1.15em;
    font-weight: 600;
    letter-spacing: -0.01em;
  }}
  .day-body {{
    padding: 22px 26px;
  }}

  /* Special day themes */
  .day-spooky .day-header {{
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 30%, #4A1A6B 60%, #6B2FA0 100%);
  }}
  .day-spooky .day-header::after {{
    background: linear-gradient(90deg, transparent, rgba(107,47,160,0.15));
  }}
  .day-spooky {{ border-color: #3D1F72; }}

  .day-stpatrick .day-header {{
    background: linear-gradient(135deg, #0D5C36 0%, #1B8C5A 50%, #28A745 100%);
  }}
  .day-stpatrick {{ border-color: #1B8C5A; }}

  .day-drive .day-header {{
    background: linear-gradient(135deg, #4A3728 0%, #6B5443 50%, #8B7355 100%);
  }}

  /* Dotted route connector between days */
  .day-section + .day-section {{
    margin-top: 8px;
  }}
  .route-connector {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px 0;
    position: relative;
  }}
  .route-connector::before {{
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    border-left: 3px dotted var(--terracotta);
    opacity: 0.35;
  }}
  .route-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--terracotta);
    position: relative;
    z-index: 1;
    box-shadow: 0 0 0 4px var(--cream);
  }}

  /* ===== HEADINGS ===== */
  h1 {{
    font-family: 'Fraunces', 'Georgia', serif;
    font-size: 1.6em;
    font-weight: 700;
    color: var(--forest);
    text-align: center;
    margin: var(--space-lg) 0 var(--space-sm);
    padding-bottom: var(--space-md);
    border-bottom: 3px solid var(--terracotta);
    letter-spacing: -0.02em;
  }}
  h2 {{
    font-family: 'Fraunces', serif;
    font-size: 1.25em;
    font-weight: 600;
    color: var(--forest);
    margin: var(--space-lg) 0 var(--space-md);
    padding: 0;
    border: none;
    letter-spacing: -0.01em;
  }}
  h3 {{
    font-family: 'Fraunces', serif;
    font-size: 1.08em;
    font-weight: 600;
    color: var(--text);
    margin: var(--space-md) 0 var(--space-sm);
    letter-spacing: -0.01em;
  }}
  h4 {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.82em;
    color: var(--terracotta);
    font-weight: 700;
    margin: var(--space-md) 0 var(--space-xs);
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }}
  p {{ margin: var(--space-sm) 0; }}

  a {{
    color: var(--forest-mid);
    text-decoration: none;
    word-break: break-word;
    font-weight: 500;
    border-bottom: 1px solid rgba(45,106,79,0.25);
    transition: all 0.2s;
  }}
  a:hover {{
    color: var(--terracotta);
    border-bottom-color: var(--terracotta);
    text-decoration: none;
  }}

  /* ===== LISTS ===== */
  ul, ol {{
    margin: var(--space-sm) 0;
    padding-left: 22px;
  }}
  li {{
    margin: 6px 0;
    line-height: 1.6;
  }}
  li::marker {{
    color: var(--terracotta);
  }}
  li strong {{
    color: var(--forest);
    font-weight: 600;
  }}

  hr {{
    border: none;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: var(--space-lg) 0;
  }}

  /* ===== TABLES ===== */
  .table-scroll {{
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: var(--space-md) 0;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88em;
    min-width: 400px;
  }}
  th {{
    background: var(--forest);
    color: var(--cream);
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    padding: 12px 14px;
    text-align: left;
    white-space: nowrap;
    font-size: 0.82em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}
  td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-light);
    vertical-align: top;
  }}
  tr:nth-child(even) {{ background: var(--parchment); }}
  tr:hover {{ background: var(--sage); }}
  td:first-child {{ font-weight: 600; color: var(--text); }}

  /* ===== ALERTS ===== */
  .alert {{
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: var(--space-md) 0;
    font-size: 0.92em;
    line-height: 1.6;
    position: relative;
  }}
  .alert-warning {{
    background: var(--warning-bg);
    border-left: 4px solid var(--warning-border);
    color: #5D3A00;
  }}
  .alert-warning::before {{
    content: '\\26A0\\FE0F';
    position: absolute;
    top: 14px;
    right: 16px;
    font-size: 1.2em;
    opacity: 0.4;
  }}
  .alert-info {{
    background: var(--info-bg);
    border-left: 4px solid var(--info-border);
    color: #1B4332;
  }}
  .alert-info::before {{
    content: '\\1F50D';
    position: absolute;
    top: 14px;
    right: 16px;
    font-size: 1.1em;
    opacity: 0.35;
  }}
  .alert-success {{
    background: #F0F7EE;
    border-left: 4px solid #52B788;
    color: #1B4332;
  }}

  /* ===== MAP LINK BUTTONS ===== */
  .map-link {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-mid) 100%);
    color: var(--cream) !important;
    padding: 10px 20px;
    border-radius: 100px;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.85em;
    text-decoration: none;
    border: none !important;
    margin: var(--space-sm) var(--space-xs) var(--space-sm) 0;
    transition: all 0.3s cubic-bezier(.4,0,.2,1);
    box-shadow: var(--shadow-sm);
    letter-spacing: 0.02em;
  }}
  .map-link:hover {{
    background: linear-gradient(135deg, var(--terracotta) 0%, #D97023 100%);
    color: white !important;
    text-decoration: none;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-bottom: none !important;
  }}

  /* ===== BACK TO TOP ===== */
  .back-top {{
    display: block;
    text-align: center;
    padding: var(--space-lg);
    margin: var(--space-xl) 0 0;
    font-size: 0.85em;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}
  .back-top a {{
    color: var(--text-muted);
    border-bottom: none;
    padding: 10px 28px;
    border-radius: 100px;
    border: 1.5px solid var(--border);
    display: inline-block;
    transition: all 0.25s;
  }}
  .back-top a:hover {{
    background: var(--forest);
    color: var(--cream);
    border-color: var(--forest);
  }}

  /* ===== CHECKBOX ITEMS ===== */
  li:has(> span:first-child) {{
    list-style: none;
  }}

  /* ===== STRONG EMPHASIS ===== */
  strong {{
    font-weight: 600;
    color: var(--text);
  }}
  em {{
    font-style: italic;
    color: var(--text-muted);
  }}

  /* ===== SCROLL REVEAL ANIMATION ===== */
  .day-section, details {{
    animation: fadeInUp 0.4s ease-out both;
  }}
  @keyframes fadeInUp {{
    from {{
      opacity: 0;
      transform: translateY(16px);
    }}
    to {{
      opacity: 1;
      transform: translateY(0);
    }}
  }}

  /* Stagger day sections */
  .day-section:nth-child(1) {{ animation-delay: 0.05s; }}
  .day-section:nth-child(2) {{ animation-delay: 0.1s; }}
  .day-section:nth-child(3) {{ animation-delay: 0.15s; }}


  /* ===== WEATHER + CLOTHING + ROAD CONDITIONS ===== */
  .weather-panel {{
    background: linear-gradient(135deg, var(--parchment) 0%, var(--cream-dark) 100%);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 0 0 var(--space-md);
    box-shadow: var(--shadow-sm);
  }}
  .weather-panel-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin: 0 0 10px;
  }}
  .weather-conditions {{
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 4px;
  }}
  .weather-icon {{ font-size: 2em; line-height: 1; }}
  .weather-temps {{ display: flex; flex-direction: column; gap: 2px; }}
  .weather-high {{
    font-family: 'Fraunces', serif;
    font-size: 1.4em;
    font-weight: 700;
    color: var(--forest);
    line-height: 1;
  }}
  .weather-low {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.82em;
    color: var(--text-muted);
  }}
  .weather-details {{ display: flex; flex-direction: column; gap: 2px; }}
  .weather-forecast {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.92em;
    font-weight: 500;
    color: var(--text);
  }}
  .weather-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75em;
    color: var(--text-muted);
    display: flex;
    gap: 12px;
  }}
  .weather-loading {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
  }}
  .weather-loading .skeleton {{
    height: 14px;
    border-radius: 7px;
    background: linear-gradient(90deg, var(--border-light) 25%, var(--cream) 50%, var(--border-light) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
  }}
  @keyframes shimmer {{
    0% {{ background-position: 200% 0; }}
    100% {{ background-position: -200% 0; }}
  }}
  .weather-unavailable {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
    color: var(--text-muted);
    font-style: italic;
    padding: 6px 0;
  }}
  .clothing-label {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--terracotta);
    margin: 12px 0 8px;
  }}
  .clothing-strip {{
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0;
    scrollbar-width: none;
  }}
  .clothing-strip::-webkit-scrollbar {{ display: none; }}
  .clothing-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    min-width: 64px;
    padding: 8px 10px;
    background: var(--card-bg);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    transition: all 0.2s;
  }}
  .clothing-item:hover {{
    border-color: var(--terracotta);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
  }}
  .clothing-item svg {{ width: 32px; height: 32px; }}
  .clothing-item-label {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.68em;
    font-weight: 500;
    color: var(--text-muted);
    text-align: center;
    white-space: nowrap;
  }}
  .road-section {{
    border-top: 1px solid var(--border-light);
    margin-top: 14px;
    padding-top: 12px;
  }}
  .road-section-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.72em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin: 0 0 8px;
  }}
  .road-status {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    font-family: 'Outfit', sans-serif;
    font-size: 0.85em;
  }}
  .road-status.road-clear {{ color: var(--forest-mid); }}
  .road-status.road-closed {{ color: var(--warning-border); font-weight: 600; }}
  .road-links {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 8px;
  }}
  .road-link {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.75em;
    font-weight: 600;
    color: var(--forest-mid) !important;
    padding: 4px 12px;
    border: 1px solid var(--border) !important;
    border-radius: 100px;
    text-decoration: none;
    transition: all 0.2s;
  }}
  .road-link:hover {{
    background: var(--forest);
    color: var(--cream) !important;
    border-color: var(--forest) !important;
  }}


  /* ===== REFERENCE SECTIONS ===== */
  .reference-container {{
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    margin-top: 32px;
    overflow: hidden;
  }}
  .reference-container details {{
    border-bottom: 1px solid #e2e8f0;
  }}
  .reference-container details:last-child {{
    border-bottom: none;
  }}
  .ref-nav a:hover {{
    background: var(--forest) !important;
    color: white !important;
  }}


  /* ===== MOBILE ===== */
  @media (max-width: 640px) {{
    body {{ padding: 0 12px 30px; font-size: 14px; }}
    .hero {{
      padding: 32px 20px 64px;
      margin: 10px 0 var(--space-md);
      border-radius: var(--radius-lg);
    }}
    .hero h1 {{ font-size: 1.5em; }}
    .hero .route-badge {{ font-size: 0.68em; padding: 5px 14px; }}
    .card {{ padding: var(--space-md); border-radius: var(--radius-md); }}
    .day-header {{ padding: 14px 18px; gap: 12px; }}
    .day-body {{ padding: 18px; }}
    .day-number {{ font-size: 0.7em; padding: 4px 10px; letter-spacing: 0.08em; }}
    .day-title {{ font-size: 1em; }}
    .day-section {{ border-radius: var(--radius-md); margin: var(--space-md) 0; }}
    details {{ border-radius: var(--radius-md); }}
    summary {{ padding: 14px 18px; font-size: 0.95em; }}
    .details-content {{ padding: 4px 18px 18px; }}
    th, td {{ padding: 8px 10px; font-size: 0.82em; }}
    .map-link {{ padding: 8px 16px; font-size: 0.82em; }}
    h2 {{ font-size: 1.12em; }}
    .alert {{ padding: 14px 16px; }}
    .weather-panel {{ padding: 14px 16px; }}
    .weather-conditions {{ gap: 10px; }}
    .weather-high {{ font-size: 1.2em; }}
    .clothing-item {{ min-width: 56px; padding: 6px 8px; }}
    .clothing-item svg {{ width: 28px; height: 28px; }}
  }}

  @media (max-width: 400px) {{
    .hero h1 {{ font-size: 1.3em; }}
    .nav-bar {{ padding: 5px 6px; gap: 3px; }}
    .nav-bar a {{ font-size: 0.68em; padding: 3px 8px; }}
    .menu-btn {{ font-size: 0.68em; padding: 3px 8px; }}
    .day-header {{ flex-wrap: wrap; }}
  }}

  /* ===== PRINT ===== */
  @media print {{
    body {{ max-width: 100%; background: white; }}
    body::before {{ display: none; }}
    .nav-bar {{ display: none; }}
    .back-top {{ display: none; }}
    .hero {{ box-shadow: none; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    details {{ border: 1px solid #ccc; break-inside: avoid; }}
    details[open] > summary {{ border-bottom: 1px solid #ccc; }}
    .day-section {{ break-inside: avoid; }}
    .day-header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
</style>
</head>
<body>

<div class="nav-bar" id="top">
  <button class="menu-btn" id="mainMenuBtn" aria-label="Menu">☰</button>
  <a href="#day-1">1</a>
  <a href="#day-2">2</a>
  <a href="#day-3">3</a>
  <a href="#day-4">4</a>
  <a href="#day-5">5</a>
  <a href="#day-6">6</a>
  <a href="#day-7">7</a>
  <a href="#day-8">8</a>
  <a href="#day-9">9</a>
  <a href="#day-10">10</a>
  <a href="#day-11">11</a>
  <a href="#day-12">12</a>
</div>

<div class="hero">
  <svg class="hero-mountains" viewBox="0 0 1200 80" preserveAspectRatio="none" style="position:absolute;bottom:0;left:0;right:0;">
    <path d="M0,80 L0,55 Q60,35 120,50 Q200,25 280,42 Q340,15 400,38 Q480,8 560,32 Q620,18 700,28 Q760,12 840,35 Q920,5 1000,30 Q1060,18 1120,38 Q1160,28 1200,45 L1200,80 Z" fill="rgba(0,0,0,0.12)"/>
    <path d="M0,80 L0,62 Q80,45 160,55 Q240,38 320,52 Q400,30 480,48 Q560,35 640,45 Q720,28 800,42 Q880,32 960,50 Q1040,38 1120,52 L1200,58 L1200,80 Z" fill="rgba(0,0,0,0.08)"/>
    <path d="M0,80 L0,68 Q100,58 200,65 Q300,55 400,62 Q500,52 600,60 Q700,55 800,65 Q900,58 1000,66 Q1100,60 1200,68 L1200,80 Z" fill="rgba(0,0,0,0.05)"/>
  </svg>
  <h1 style="border:none; margin:0; padding:0; color:var(--cream);">12-Day Family Road Trip</h1>
  <div class="subtitle">
    Tamarac, FL &rarr; Savannah &rarr; NC Mountains &rarr; Home<br>
    March 11&ndash;22, 2026
  </div>
  <span class="route-badge">~2,250 mi &bull; Family of 3 &bull; Toyota Crown</span>
</div>

{html_body}

<div class="back-top"><a href="#top">&uarr; Back to Top</a></div>

<script>
// ============================================
// Post-process: Transform flat HTML into styled components
// ============================================
document.addEventListener('DOMContentLoaded', function() {{

  // Helper: wrap content between two elements in a collapsible container
  function wrapSection(heading, className, emoji, collapsed) {{
    if (!heading) return;
    const details = document.createElement('details');
    if (!collapsed) details.setAttribute('open', '');
    details.className = className || '';

    const summary = document.createElement('summary');
    summary.textContent = (emoji ? emoji + ' ' : '') + heading.textContent;

    const content = document.createElement('div');
    content.className = 'details-content';

    let next = heading.nextElementSibling;
    const collected = [];
    while (next && next.tagName !== 'H2' && !(next.tagName === 'HR')) {{
      collected.push(next);
      next = next.nextElementSibling;
    }}
    if (next && next.tagName === 'HR') {{
      collected.push(next);
      next = next.nextElementSibling;
    }}

    heading.parentNode.insertBefore(details, heading);
    details.appendChild(summary);
    details.appendChild(content);
    collected.forEach(el => content.appendChild(el));
    heading.remove();
  }}

  // Find and wrap overview sections
  const h2s = document.querySelectorAll('h2');
  const sectionConfig = {{
    'Context': {{ emoji: '\\uD83D\\uDCCD', collapsed: true }},
    'Asheville Days Flexibility Guide': {{ emoji: '\\uD83D\\uDD00', collapsed: true }},
    'Costco Locations': {{ emoji: '\\uD83D\\uDED2', collapsed: true }},
    'Vehicle Notes': {{ emoji: '\\uD83D\\uDE97', collapsed: true }},
    'Horror, Oddities': {{ emoji: '\\uD83E\\uDD87', collapsed: true }},
    'Events Calendar': {{ emoji: '\\uD83D\\uDCC5', collapsed: true }},
    'Road Condition Alerts': {{ emoji: '\\uD83D\\uDEA7', collapsed: true }},
    'Kid-Friendly Backup': {{ emoji: '\\uD83C\\uDFAE', collapsed: true }},
    'Driving Summary': {{ emoji: '\\uD83D\\uDDFA\\uFE0F', collapsed: true }},
    'Packing List': {{ emoji: '\\uD83E\\uDDF3', collapsed: true }},
    'Neighborhood Drive': {{ emoji: '\\uD83C\\uDFD8\\uFE0F', collapsed: true }},
    'What to Evaluate': {{ emoji: '\\uD83D\\uDCCA', collapsed: true }},
  }};

  h2s.forEach(h2 => {{
    for (const [key, config] of Object.entries(sectionConfig)) {{
      if (h2.textContent.includes(key)) {{
        wrapSection(h2, '', config.emoji, config.collapsed);
        break;
      }}
    }}
  }});

  // Wrap Day sections in styled cards
  const dayH2s = document.querySelectorAll('h2[id^="day-"]');
  dayH2s.forEach(h2 => {{
    const dayMatch = h2.textContent.match(/Day\\s+(\\d+)/);
    if (!dayMatch) return;

    const dayNum = dayMatch[1];
    const card = document.createElement('div');
    card.className = 'day-section';
    card.id = h2.id;

    // Special styling
    if (h2.textContent.includes('Friday the 13th')) card.classList.add('day-spooky');
    if (h2.textContent.includes('St. Patrick')) card.classList.add('day-stpatrick');
    if (h2.textContent.includes('Drive to Savannah') || h2.textContent.includes('Savannah →') || h2.textContent.includes('→ Home')) card.classList.add('day-drive');

    const header = document.createElement('div');
    header.className = 'day-header';

    // Extract date and title from heading like "Tuesday, March 11th: Drive to Savannah"
    let afterDay = h2.textContent.replace(/Day\\s+\\d+\\s*[\\u2014\\u2013-]\\s*/, '');
    let dateText = '';
    let titleText = afterDay;
    const colonIdx = afterDay.indexOf(':');
    if (colonIdx > -1) {{
      dateText = afterDay.substring(0, colonIdx).trim();
      titleText = afterDay.substring(colonIdx + 1).trim();
    }}

    let headerHtml = '<span class="day-number">DAY ' + dayNum + '</span>';
    if (dateText) {{
      headerHtml += '<span class="day-date">' + dateText + '</span>';
    }}
    headerHtml += '<span class="day-title">' + titleText + '</span>';
    header.innerHTML = headerHtml;

    const body = document.createElement('div');
    body.className = 'day-body';

    // Collect content until next day section or major section
    let next = h2.nextElementSibling;
    const collected = [];
    while (next && !(next.tagName === 'H2' || (next.tagName === 'DIV' && next.classList.contains('day-section')) || next.tagName === 'HR' || next.tagName === 'DETAILS')) {{
      collected.push(next);
      next = next.nextElementSibling;
    }}
    if (next && next.tagName === 'HR') {{
      next.remove();
    }}

    h2.parentNode.insertBefore(card, h2);
    card.appendChild(header);
    card.appendChild(body);
    collected.forEach(el => body.appendChild(el));
    h2.remove();
  }});

  // Style Google Map links as pill buttons
  document.querySelectorAll('a').forEach(a => {{
    if (a.href && (a.href.includes('google.com/maps') || a.textContent.includes('Google Map') || a.textContent.includes('Map') || a.textContent.includes('Option 1') || a.textContent.includes('Option 2'))) {{
      if (a.textContent.length < 60) {{
        a.classList.add('map-link');
        a.textContent = '\\uD83D\\uDCCD ' + a.textContent;
      }}
    }}
  }});

  // Wrap warning paragraphs in styled alert boxes
  document.querySelectorAll('p').forEach(p => {{
    const text = p.textContent;
    if (text.includes('\\u26A0') || text.includes('WARNING') || text.includes('ROUTE WARNING') || text.includes('GPS WARNING')) {{
      if (!p.closest('.alert')) {{
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning';
        p.parentNode.insertBefore(alert, p);
        alert.appendChild(p);
      }}
    }}
    if (text.includes('Scouting note') || text.includes('Scouting bonus')) {{
      if (!p.closest('.alert')) {{
        const alert = document.createElement('div');
        alert.className = 'alert alert-info';
        p.parentNode.insertBefore(alert, p);
        alert.appendChild(p);
      }}
    }}
  }});

  // Wrap tables in scroll containers
  document.querySelectorAll('table').forEach(table => {{
    if (!table.parentElement.classList.contains('table-scroll')) {{
      const wrapper = document.createElement('div');
      wrapper.className = 'table-scroll';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }}
  }});

  // Remove the raw h1 + subtitle that markdown generated (hero header replaces them)
  const firstH1 = document.querySelector('body > h1');
  if (firstH1) {{
    let next = firstH1.nextElementSibling;
    while (next && (next.tagName === 'P' || next.tagName === 'HR')) {{
      const toRemove = next;
      next = next.nextElementSibling;
      if (toRemove.textContent.includes('March 11') || toRemove.textContent.includes('Vehicle:') || toRemove.tagName === 'HR') {{
        toRemove.remove();
      }} else {{
        break;
      }}
    }}
    firstH1.remove();
  }}

  // Add route connector dots between day sections
  const daySections = document.querySelectorAll('.day-section');
  daySections.forEach((section, i) => {{
    if (i > 0) {{
      const connector = document.createElement('div');
      connector.className = 'route-connector';
      connector.innerHTML = '<div class="route-dot"></div>';
      section.parentNode.insertBefore(connector, section);
    }}
  }});

// ============================================
// WEATHER, CLOTHING & ROAD CONDITIONS MODULE
// ============================================

const DAY_LOCATIONS = [
  {{ day: 1, date: "2026-03-11", lat: 32.0809, lon: -81.0912, name: "Savannah GA" }},
  {{ day: 2, date: "2026-03-12", lat: 35.5951, lon: -82.5515, name: "Asheville NC" }},
  {{ day: 3, date: "2026-03-13", lat: 35.5951, lon: -82.5515, name: "Asheville NC" }},
  {{ day: 4, date: "2026-03-14", lat: 35.3185, lon: -82.4612, name: "Hendersonville NC" }},
  {{ day: 5, date: "2026-03-15", lat: 35.5951, lon: -82.5515, name: "Asheville NC" }},
  {{ day: 6, date: "2026-03-16", lat: 35.439, lon: -82.2462, name: "Chimney Rock NC" }},
  {{ day: 7, date: "2026-03-17", lat: 35.2716, lon: -82.7717, name: "Pisgah Forest NC" }},
  {{ day: 8, date: "2026-03-18", lat: 35.2334, lon: -82.7343, name: "Brevard NC" }},
  {{ day: 9, date: "2026-03-19", lat: 36.1338, lon: -81.671, name: "Blowing Rock NC" }},
  {{ day: 10, date: "2026-03-20", lat: 36.1338, lon: -81.671, name: "Blowing Rock NC" }},
  {{ day: 11, date: "2026-03-21", lat: 32.0809, lon: -81.0912, name: "Savannah GA" }},
  {{ day: 12, date: "2026-03-22", lat: 26.2129, lon: -80.2498, name: "Tamarac FL" }},
];

const HIKING_DAYS = [3, 4, 6, 7, 8, 9, 10];
const DRIVE_DAYS = [1, 2, 11, 12];

const CLOTHING_ICONS = {{

  heavyJacket: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L6 8V28H14V16H22V28H30V8L24 4"/><path d="M12 4C12 4 14 6 18 6C22 6 24 4 24 4"/><line x1="18" y1="16" x2="18" y2="28"/><line x1="16" y1="20" x2="16" y2="24"/><line x1="20" y1="20" x2="20" y2="24"/></svg>`,

  lightJacket: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L6 8V28H14V16H22V28H30V8L24 4"/><path d="M12 4C12 4 14 6 18 6C22 6 24 4 24 4"/></svg>`,

  fleece: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L6 8V28H14V16H22V28H30V8L24 4"/><path d="M12 4C12 4 14 6 18 6C22 6 24 4 24 4"/><line x1="10" y1="10" x2="10" y2="26"/><line x1="13" y1="10" x2="13" y2="14"/><line x1="26" y1="10" x2="26" y2="26"/><line x1="23" y1="10" x2="23" y2="14"/></svg>`,

  tshirt: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L4 10L8 12L10 10V30H26V10L28 12L32 10L24 4"/><path d="M12 4C12 4 14 7 18 7C22 7 24 4 24 4"/></svg>`,

  rainJacket: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L6 8V28H14V16H22V28H30V8L24 4"/><path d="M12 4C12 4 14 6 18 6C22 6 24 4 24 4"/><circle cx="8" cy="32" r="1"/><circle cx="14" cy="34" r="1"/><circle cx="11" cy="31" r="1"/></svg>`,

  umbrella: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6C10 6 4 12 4 18H32C32 12 26 6 18 6Z"/><line x1="18" y1="6" x2="18" y2="30"/><path d="M18 30C18 32 16 34 14 32"/></svg>`,

  longPants: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 4H26V14L22 32H20L18 18L16 32H14L10 14Z"/></svg>`,

  shorts: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 4H26V12L22 22H20L18 14L16 22H14L10 12Z"/></svg>`,

  hikingBoots: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12V24H4V28H28V24H20V8H14V12Z"/><line x1="14" y1="14" x2="8" y2="14"/><line x1="14" y1="18" x2="10" y2="18"/><path d="M4 28H28V30H4Z"/></svg>`,

  sunHat: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="18" cy="22" rx="16" ry="4"/><path d="M10 22V16C10 12 13 8 18 8C23 8 26 12 26 16V22"/></svg>`,

  gloves: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 32V14H14V6H18V14H22V8H26V20L24 32Z"/><line x1="14" y1="14" x2="14" y2="32"/><line x1="18" y1="14" x2="18" y2="32"/><line x1="22" y1="14" x2="22" y2="32"/></svg>`,

  sunglasses: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="14" width="10" height="8" rx="3"/><rect x="22" y="14" width="10" height="8" rx="3"/><path d="M14 18H22"/><line x1="4" y1="16" x2="2" y2="14"/><line x1="32" y1="16" x2="34" y2="14"/></svg>`,

  sunscreen: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="10" width="16" height="22" rx="3"/><rect x="12" y="4" width="12" height="6" rx="2"/><line x1="14" y1="18" x2="22" y2="18"/><line x1="14" y1="22" x2="22" y2="22"/><line x1="14" y1="26" x2="22" y2="26"/></svg>`,

  layers: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 4L4 14L18 24L32 14Z"/><path d="M4 18L18 28L32 18"/><path d="M4 22L18 32L32 22"/></svg>`,

  comfyShoes: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22C4 18 8 14 14 14H20C26 14 30 16 32 20V24H4Z"/><line x1="4" y1="24" x2="32" y2="24"/><path d="M14 14V12C14 10 16 8 18 8"/></svg>`,

  windbreaker: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4L6 8V28H14V16H22V28H30V8L24 4"/><path d="M12 4C12 4 14 6 18 6C22 6 24 4 24 4"/><path d="M2 12L6 14"/><path d="M2 16L6 18"/><path d="M2 20L6 22"/></svg>`,

  daypack: `<svg viewBox="0 0 36 36" fill="none" stroke="#1B4332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="10" width="20" height="22" rx="4"/><path d="M12 10V6C12 4 14 2 18 2C22 2 24 4 24 6V10"/><rect x="12" y="16" width="12" height="8" rx="2"/><line x1="18" y1="16" x2="18" y2="24"/></svg>`,

}};

function conditionIcon(forecast) {{
  const f = forecast.toLowerCase();
  if (f.includes("thunder")) return "\u26C8\uFE0F";
  if (f.includes("rain") || f.includes("shower") || f.includes("drizzle")) return "🌧️";
  if (f.includes("snow") || f.includes("sleet") || f.includes("ice") || f.includes("flurr")) return "\u2744\uFE0F";
  if (f.includes("fog") || f.includes("mist") || f.includes("haze")) return "🌫️";
  if (f.includes("cloud") || f.includes("overcast")) return "\u2601\uFE0F";
  if (f.includes("partly")) return "\u26C5";
  if (f.includes("wind")) return "🌬️";
  if (f.includes("sunny") || f.includes("clear")) return "\u2600\uFE0F";
  return "🌤️";
}}

function getClothingItems(high, low, forecast, windSpeed, dayNum) {{
  const items = [];
  const f = forecast.toLowerCase();
  const isHike = HIKING_DAYS.includes(dayNum);
  const isDrive = DRIVE_DAYS.includes(dayNum);

  if (low < 35) {{
    items.push({{ icon: CLOTHING_ICONS.heavyJacket, label: "Heavy Jacket" }});
    items.push({{ icon: CLOTHING_ICONS.gloves, label: "Gloves" }});
    items.push({{ icon: CLOTHING_ICONS.layers, label: "Warm Layers" }});
    items.push({{ icon: CLOTHING_ICONS.longPants, label: "Long Pants" }});
  }} else if (low < 45) {{
    items.push({{ icon: CLOTHING_ICONS.lightJacket, label: "Jacket" }});
    items.push({{ icon: CLOTHING_ICONS.layers, label: "Layers" }});
    items.push({{ icon: CLOTHING_ICONS.longPants, label: "Long Pants" }});
  }} else if (low < 55) {{
    items.push({{ icon: CLOTHING_ICONS.fleece, label: "Fleece" }});
    items.push({{ icon: CLOTHING_ICONS.layers, label: "Layers" }});
    items.push({{ icon: CLOTHING_ICONS.longPants, label: "Long Pants" }});
  }} else if (high > 75) {{
    items.push({{ icon: CLOTHING_ICONS.tshirt, label: "T-Shirt" }});
    items.push({{ icon: CLOTHING_ICONS.shorts, label: "Shorts" }});
    items.push({{ icon: CLOTHING_ICONS.sunHat, label: "Sun Hat" }});
    items.push({{ icon: CLOTHING_ICONS.sunscreen, label: "Sunscreen" }});
  }} else {{
    items.push({{ icon: CLOTHING_ICONS.tshirt, label: "T-Shirt" }});
    items.push({{ icon: CLOTHING_ICONS.longPants, label: "Long Pants" }});
  }}

  if (f.includes("rain") || f.includes("shower") || f.includes("drizzle") || f.includes("thunder")) {{
    items.push({{ icon: CLOTHING_ICONS.rainJacket, label: "Rain Jacket" }});
    items.push({{ icon: CLOTHING_ICONS.umbrella, label: "Umbrella" }});
  }}

  if (windSpeed > 15) {{
    items.push({{ icon: CLOTHING_ICONS.windbreaker, label: "Windbreaker" }});
  }}

  if (isHike) {{
    items.push({{ icon: CLOTHING_ICONS.hikingBoots, label: "Hiking Boots" }});
    items.push({{ icon: CLOTHING_ICONS.daypack, label: "Daypack" }});
  }}

  if (isDrive) {{
    items.push({{ icon: CLOTHING_ICONS.comfyShoes, label: "Comfy Shoes" }});
  }}

  if (high > 65 && low > 45) {{
    items.push({{ icon: CLOTHING_ICONS.sunglasses, label: "Sunglasses" }});
  }}

  return items;
}}

// ============================================
// ROAD CONDITIONS DATA
// ============================================

const KNOWN_CLOSURES = {{
  6: [
    {{ road: "US-74A", status: "Closed", reason: "Helene damage \u2014 impassable near Chimney Rock" }},
    {{ road: "US-64", status: "Closed", reason: "Helene damage \u2014 Lake Lure area" }},
    {{ road: "NC-9", status: "Closed", reason: "Helene damage \u2014 Bat Cave section" }}
  ]
}};

const KNOWN_BRP = [
  {{ section: "MP 316.5 \u2013 355.3", status: "Closed", note: "Structural damage" }},
  {{ section: "MP 420.2 \u2013 443.0", status: "Closed", note: "Landslide area" }},
  {{ section: "MP 305 \u2013 317", status: "Open", note: "Ridge Junction area" }},
  {{ section: "MP 375.7 \u2013 393.6", status: "Open", note: "Waterrock Knob area" }},
  {{ section: "MP 393.6 \u2013 420.2", status: "Open", note: "Balsam area" }}
];

const ROAD_LINKS = {{
  NC: {{ label: "DriveNC.gov", url: "https://drivenc.gov" }},
  GA: {{ label: "511GA.org", url: "https://511ga.org" }},
  SC: {{ label: "511SC.org", url: "https://511sc.org" }},
  FL: {{ label: "FL511.com", url: "https://fl511.com" }},
  BRP: {{ label: "NPS BRP Closures", url: "https://www.nps.gov/blri/planyourvisit/roadclosures.htm" }}
}};

const DAY_ROAD_LINKS = {{
  1: ["GA", "SC"],
  2: ["SC", "NC"],
  3: ["NC"],
  4: ["NC"],
  5: ["NC"],
  6: ["NC", "BRP"],
  7: ["NC", "BRP"],
  8: ["NC", "BRP"],
  9: ["NC"],
  10: ["NC", "BRP"],
  11: ["NC", "SC", "GA"],
  12: ["GA", "FL"]
}};

const BRP_DAYS = [6, 7, 8, 10];

// ============================================
// LIVE ROAD CONDITIONS API
// ============================================

// Counties along the route, mapped to trip days
const ROUTE_COUNTIES = {{
  1: [],  // FL/GA - not NC
  2: [],  // Driving through SC
  3: [11],  // Buncombe (Asheville)
  4: [45],  // Henderson (Hendersonville)
  5: [11],  // Buncombe (Asheville/Biltmore)
  6: [45, 80],  // Henderson, Rutherford (Chimney Rock)
  7: [11, 88],  // Buncombe, Transylvania (Pisgah)
  8: [88],  // Transylvania (Brevard/DuPont)
  9: [95],  // Watauga (Boone)
  10: [3, 95],  // Avery, Watauga (Grandfather Mtn)
  11: [],  // Driving south
  12: []   // Driving south
}};

// Key roads to filter for
const KEY_ROADS = ["US-74", "US-64", "US-25", "US-19", "US-70", "US-221", "US-321", "NC-9", "NC-191", "NC-280", "NC-215", "NC-276", "I-26", "I-40", "I-240", "I-77", "I-81"];

let liveClosures = {{}};
let liveBRPAlerts = [];
let roadDataTimestamp = null;

async function fetchNCDOTClosures() {{
  try {{
    const res = await fetch('https://eapps.ncdot.gov/services/traffic-prod/v1/incidents?active=true');
    if (!res.ok) throw new Error('NCDOT API error');
    const data = await res.json();
    
    // Get all road closed incident IDs
    const closedIds = data.roadClosedIncidents || [];
    if (closedIds.length === 0) return;
    
    // Fetch details for first 30 closed incidents (to limit API calls)
    const batchSize = 10;
    const idsToFetch = closedIds.slice(0, 30);
    const batches = [];
    for (let i = 0; i < idsToFetch.length; i += batchSize) {{
      batches.push(idsToFetch.slice(i, i + batchSize));
    }}
    
    const allIncidents = [];
    for (const batch of batches) {{
      const results = await Promise.all(
        batch.map(id => 
          fetch('https://eapps.ncdot.gov/services/traffic-prod/v1/incidents/' + id)
            .then(r => r.ok ? r.json() : null)
            .catch(() => null)
        )
      );
      results.forEach(r => {{ if (r) allIncidents.push(r); }});
    }}
    
    // Map incidents to days based on county
    for (const [dayStr, countyIds] of Object.entries(ROUTE_COUNTIES)) {{
      const dayNum = parseInt(dayStr);
      if (countyIds.length === 0) continue;
      const relevant = allIncidents.filter(inc => 
        inc.county && countyIds.includes(inc.county.id) && inc.condition === 'Road Closed'
      );
      if (relevant.length > 0) {{
        liveClosures[dayNum] = relevant.map(inc => ({{
          road: (inc.road ? (inc.road.commonName || inc.road.name) : 'Unknown'),
          status: inc.condition || 'Closed',
          reason: inc.reason || inc.location || 'Road closure reported'
        }}));
      }}
    }}
    
    roadDataTimestamp = new Date().toLocaleString();
    console.log('NCDOT closures loaded:', Object.keys(liveClosures).length, 'days affected');
  }} catch (err) {{
    console.warn('NCDOT fetch failed:', err);
  }}
}}

async function fetchBRPAlerts() {{
  try {{
    const res = await fetch('https://developer.nps.gov/api/v1/alerts?parkCode=blri&api_key=DEMO_KEY');
    if (!res.ok) throw new Error('NPS API error');
    const data = await res.json();
    liveBRPAlerts = (data.data || []).map(alert => ({{
      title: alert.title,
      description: alert.description,
      category: alert.category,
      url: alert.url || 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
    }}));
    console.log('BRP alerts loaded:', liveBRPAlerts.length);
  }} catch (err) {{
    console.warn('NPS BRP fetch failed:', err);
  }}
}}

// ============================================
// WEATHER API FUNCTIONS (Open-Meteo — 16-day forecast)
// ============================================

const weatherCache = {{}};

function wmoCodeToText(code) {{
  const map = {{
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
  }};
  return map[code] || "Partly cloudy";
}}

async function fetchWeather(lat, lon) {{
  const key = `${{lat}},${{lon}}`;
  if (weatherCache[key]) return weatherCache[key];

  try {{
    // Single API call with both models - avoids rate limiting
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto&models=best_match,ecmwf_ifs025`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Open-Meteo error: ${{res.status}}`);
    const data = await res.json();
    const d = data.daily;

    // Blend both models from the single response
    const blended = blendModels(d);
    // Normalize hourly fields (multi-model adds _best_match suffix)
    let hourly = data.hourly || null;
    if (hourly && !hourly.precipitation_probability && hourly.precipitation_probability_best_match) {{
      hourly = {{ time: hourly.time, precipitation_probability: hourly.precipitation_probability_best_match }};
    }}
    weatherCache[key] = {{ daily: blended, hourly: hourly }};
    return weatherCache[key];
  }} catch (err) {{
    // Fallback: try single default model if multi-model fails
    try {{
      const fallbackUrl = `https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=16&timezone=auto`;
      const res2 = await fetch(fallbackUrl);
      if (!res2.ok) throw new Error(`Fallback error: ${{res2.status}}`);
      const data2 = await res2.json();
      weatherCache[key] = {{ daily: data2.daily, hourly: data2.hourly || null }};
      return weatherCache[key];
    }} catch (err2) {{
      console.warn(`Weather fetch failed for ${{lat}},${{lon}}:`, err2);
      return null;
    }}
  }}
}}

function blendModels(d) {{
  // When both models are in one response, fields are suffixed:
  // _best_match and _ecmwf_ifs025
  const hasBM = d.temperature_2m_max_best_match != null;
  const hasEC = d.temperature_2m_max_ecmwf_ifs025 != null;

  // If only one model returned, use standard field names
  if (!hasBM && !hasEC) {{
    return d;
  }}

  const result = {{
    time: d.time,
    temperature_2m_max: [],
    temperature_2m_min: [],
    precipitation_probability_max: [],
    wind_speed_10m_max: [],
    weather_code: []
  }};

  for (let i = 0; i < d.time.length; i++) {{
    const bmHigh = hasBM ? d.temperature_2m_max_best_match[i] : null;
    const bmLow = hasBM ? d.temperature_2m_min_best_match[i] : null;
    const bmPrecip = hasBM ? d.precipitation_probability_max_best_match[i] : null;
    const bmWind = hasBM ? d.wind_speed_10m_max_best_match[i] : null;
    const bmCode = hasBM ? d.weather_code_best_match[i] : null;

    const ecHigh = hasEC ? d.temperature_2m_max_ecmwf_ifs025[i] : null;
    const ecLow = hasEC ? d.temperature_2m_min_ecmwf_ifs025[i] : null;
    const ecPrecip = hasEC ? d.precipitation_probability_max_ecmwf_ifs025[i] : null;
    const ecWind = hasEC ? d.wind_speed_10m_max_ecmwf_ifs025[i] : null;

    if (bmHigh != null && ecHigh != null) {{
      result.temperature_2m_max.push((bmHigh + ecHigh) / 2);
      result.temperature_2m_min.push((bmLow + ecLow) / 2);
      result.precipitation_probability_max.push(Math.max(bmPrecip || 0, ecPrecip || 0));
      result.wind_speed_10m_max.push((bmWind + ecWind) / 2);
      result.weather_code.push(bmCode != null ? bmCode : ecHigh);
    }} else if (bmHigh != null) {{
      result.temperature_2m_max.push(bmHigh);
      result.temperature_2m_min.push(bmLow);
      result.precipitation_probability_max.push(bmPrecip);
      result.wind_speed_10m_max.push(bmWind);
      result.weather_code.push(bmCode);
    }} else if (ecHigh != null) {{
      result.temperature_2m_max.push(ecHigh);
      result.temperature_2m_min.push(ecLow);
      result.precipitation_probability_max.push(ecPrecip);
      result.wind_speed_10m_max.push(ecWind);
      result.weather_code.push(d.weather_code_ecmwf_ifs025 ? d.weather_code_ecmwf_ifs025[i] : 2);
    }} else {{
      result.temperature_2m_max.push(null);
      result.temperature_2m_min.push(null);
      result.precipitation_probability_max.push(null);
      result.wind_speed_10m_max.push(null);
      result.weather_code.push(null);
    }}
  }}

  return result;
}}
function findForecast(daily, dateStr) {{
  if (!daily || !daily.time) return {{ day: null, night: null }};
  const idx = daily.time.indexOf(dateStr);
  if (idx === -1) return {{ day: null, night: null }};
  return {{
    day: {{
      temperature: Math.round(daily.temperature_2m_max[idx]),
      shortForecast: wmoCodeToText(daily.weather_code[idx]),
      windSpeed: Math.round(daily.wind_speed_10m_max[idx]) + " mph",
      windDirection: "",
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }},
      detailedForecast: ""
    }},
    night: {{
      temperature: Math.round(daily.temperature_2m_min[idx]),
      probabilityOfPrecipitation: {{ value: daily.precipitation_probability_max[idx] }}
    }}
  }};
}}

function extractHourlyPrecip(weatherData, dateStr) {{
  if (!weatherData || !weatherData.hourly || !weatherData.hourly.time) return null;
  const hourly = weatherData.hourly;
  const hours = [];
  for (let i = 0; i < hourly.time.length; i++) {{
    if (hourly.time[i].startsWith(dateStr)) {{
      const hr = parseInt(hourly.time[i].substring(11, 13), 10);
      hours.push({{ hour: hr, precip: hourly.precipitation_probability[i] || 0 }});
    }}
  }}
  return hours.length > 0 ? hours : null;
}}

function parseWindSpeed(windStr) {{
  if (!windStr) return 0;
  const match = windStr.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}}

// ============================================
// PANEL BUILDER
// ============================================

function buildPanel(dayInfo, forecast) {{
  const panel = document.createElement("div");
  panel.className = "weather-panel";
  panel.style.cssText = "background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #bbf7d0;border-radius:12px;padding:16px;margin:8px 0 16px 0;font-family:inherit;";

  const {{ day, night }} = forecast;
  const dayNum = dayInfo.day;
  const location = dayInfo.name;
  const dateStr = dayInfo.date;

  let html = `<div style=\"font-size:1.1em;font-weight:700;color:#1B4332;margin-bottom:8px;\">🌤️ Weather &amp; Conditions \u2014 ${{location}}</div>`;

  if (!day && !night) {{
    html += `<div style=\"color:#666;font-style:italic;margin-bottom:8px;\">Forecast available ~7 days before ${{dateStr}}</div>`;

    // Default clothing for March in WNC when forecast not available
    const defaultClothing = getClothingItems(55, 35, "Partly Cloudy", 8, dayNum);
    if (defaultClothing.length > 0) {{
      html += `<div style=\"margin-top:8px;margin-bottom:10px;\">`;
      html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:6px;\">🧥 What to Pack (typical March conditions)</div>`;
      html += `<div style=\"display:flex;flex-wrap:wrap;gap:8px;\">`;
      for (const item of defaultClothing) {{
        html += `<div style=\"display:flex;flex-direction:column;align-items:center;width:52px;\">`;
        html += `<div style=\"width:36px;height:36px;\">${{item.icon}}</div>`;
        html += `<span style=\"font-size:0.7em;text-align:center;color:#333;margin-top:2px;\">${{item.label}}</span>`;
        html += `</div>`;
      }}
      html += `</div></div>`;
    }}
  }}

  else {{
    const high = day ? day.temperature : (night ? night.temperature : "--");
    const low = night ? night.temperature : (day ? day.temperature - 15 : "--");
    const forecastText = day ? day.shortForecast : (night ? night.shortForecast : "N/A");
    const detailedForecast = day ? day.detailedForecast : "";
    const windDay = day ? day.windSpeed : "";
    const windNight = night ? night.windSpeed : "";
    const windDir = day ? (day.windDirection || "") : "";
    const precipDay = day && day.probabilityOfPrecipitation ? day.probabilityOfPrecipitation.value : null;
    const precipNight = night && night.probabilityOfPrecipitation ? night.probabilityOfPrecipitation.value : null;
    const windSpeed = parseWindSpeed(windDay || windNight);

    const icon = conditionIcon(forecastText);

    html += `<div style=\"display:flex;align-items:center;gap:12px;margin-bottom:10px;\">`;
    html += `<span style=\"font-size:2.2em;\">${{icon}}</span>`;
    html += `<div>`;
    html += `<div style=\"font-size:1.3em;font-weight:600;\">${{high}}\u00B0F / ${{low}}\u00B0F</div>`;
    html += `<div style=\"color:#555;\">${{forecastText}}</div>`;
    html += `</div></div>`;

    if (forecast.hourlyPrecip && forecast.hourlyPrecip.length > 0) {{
      html += `<div style=\"margin-bottom:8px;\">`;
      html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:4px;\">💧 Precipitation Chance by Hour</div>`;
      html += `<div style=\"display:flex;flex-wrap:wrap;gap:6px 12px;font-size:0.82em;color:#555;\">`;
      for (const h of forecast.hourlyPrecip) {{
        if (h.hour % 3 === 0) {{
          const labelStr = h.hour === 0 ? "12 AM" : h.hour < 12 ? h.hour + " AM" : h.hour === 12 ? "12 PM" : (h.hour - 12) + " PM";
          const color = h.precip > 60 ? "#2563eb" : h.precip > 30 ? "#1B4332" : "#555";
          const weight = h.precip > 30 ? "600" : "400";
          html += `<span style=\"color:${{color}};font-weight:${{weight}};\">${{labelStr}}: ${{h.precip}}%</span>`;
        }}
      }}
      html += `</div>`;
      html += `</div>`;
    }} else if (precipDay !== null || precipNight !== null) {{
      const pDay = precipDay !== null ? precipDay : "--";
      const pNight = precipNight !== null ? precipNight : "--";
      html += `<div style=\"font-size:0.9em;color:#555;margin-bottom:4px;\">💧 Precip: ${{pDay}}% day / ${{pNight}}% night</div>`;
    }}

    if (windDay || windNight) {{
      html += `<div style=\"font-size:0.9em;color:#555;margin-bottom:10px;\">🌬️ Wind: ${{windDay || windNight}} ${{windDir}}</div>`;
    }}

    // Clothing strip
    const highNum = typeof high === "number" ? high : 60;
    const lowNum = typeof low === "number" ? low : 40;
    const clothing = getClothingItems(highNum, lowNum, forecastText, windSpeed, dayNum);

    if (clothing.length > 0) {{
      html += `<div style=\"margin-top:8px;margin-bottom:10px;\">`;
      html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:6px;\">🧥 What to Wear</div>`;
      html += `<div style=\"display:flex;flex-wrap:wrap;gap:8px;\">`;
      for (const item of clothing) {{
        html += `<div style=\"display:flex;flex-direction:column;align-items:center;width:52px;\">`;
        html += `<div style=\"width:36px;height:36px;\">${{item.icon}}</div>`;
        html += `<span style=\"font-size:0.7em;text-align:center;color:#333;margin-top:2px;\">${{item.label}}</span>`;
        html += `</div>`;
      }}
      html += `</div></div>`;
    }}
  }}

  // Road conditions
  html += `<div data-road-section=\"true\" style=\"margin-top:10px;border-top:1px solid #bbf7d0;padding-top:10px;\">`;
  html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:6px;\">🛣️ Road Conditions</div>`;

  // Known closures
  if (KNOWN_CLOSURES[dayNum]) {{
    html += `<div style=\"margin-bottom:6px;\">`;
    for (const c of KNOWN_CLOSURES[dayNum]) {{
      html += `<div style=\"font-size:0.85em;color:#DC2626;margin-bottom:2px;\">\u26D4 ${{c.road}}: ${{c.status}} \u2014 ${{c.reason}}</div>`;
    }}
    html += `</div>`;
  }}

  // BRP status
  if (BRP_DAYS.includes(dayNum)) {{
    html += `<div style=\"margin-bottom:6px;\">`;
    html += `<div style=\"font-size:0.85em;font-weight:600;color:#1B4332;margin-bottom:3px;\">Blue Ridge Parkway Status:</div>`;
    for (const s of KNOWN_BRP) {{
      const color = s.status === "Closed" ? "#DC2626" : "#16A34A";
      const sym = s.status === "Closed" ? "\u26D4" : "\u2705";
      html += `<div style=\"font-size:0.82em;color:${{color}};margin-bottom:1px;\">${{sym}} ${{s.section}}: ${{s.status}} (${{s.note}})</div>`;
    }}
    html += `</div>`;
  }}

  // Road links
  const linkKeys = DAY_ROAD_LINKS[dayNum] || [];
  if (linkKeys.length > 0) {{
    html += `<div style=\"font-size:0.82em;color:#555;\">`;
    html += `Check conditions: `;
    const linkHtmlArr = linkKeys.map(k => {{
      const lnk = ROAD_LINKS[k];
      return `<a href=\"${{lnk.url}}\" target=\"_blank\" style=\"color:#15803d;\">${{lnk.label}}</a>`;
    }});
    html += linkHtmlArr.join(" | ");
    html += `</div>`;
  }}

  html += `</div>`;

  // Forecast source attribution
  html += `<div style="margin-top:8px;font-size:0.72em;color:#999;text-align:right;">Forecast: GFS + ECMWF blend via <a href=\"https://open-meteo.com\" target=\"_blank\" style=\"color:#999;\">Open-Meteo</a> · Updates on page load</div>`;

  panel.innerHTML = html;
  return panel;
}}

// ============================================
// PANEL INJECTION
// ============================================

async function injectWeatherPanels() {{
  const sections = document.querySelectorAll(".day-section");
  if (!sections.length) {{
    console.warn("No .day-section elements found");
    return;
  }}

  // Insert loading skeletons
  const placeholders = [];
  sections.forEach((sec, idx) => {{
    if (idx < DAY_LOCATIONS.length) {{
      const ph = document.createElement("div");
      ph.className = "weather-placeholder";
      ph.style.cssText = "background:linear-gradient(90deg,#f0fdf4 25%,#dcfce7 50%,#f0fdf4 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border:1px solid #bbf7d0;border-radius:12px;padding:16px;margin:8px 0 16px 0;min-height:80px;";
      ph.innerHTML = `<div style=\"color:#999;font-style:italic;\">Loading weather for ${{DAY_LOCATIONS[idx].name}}...</div>`;
      const dayBody = sec.querySelector(".day-body");
      if (dayBody) {{
        dayBody.insertBefore(ph, dayBody.firstChild);
      }} else {{
        sec.insertBefore(ph, sec.children[1] || null);
      }}
      placeholders.push(ph);
    }}
  }});

  // Add shimmer animation
  if (!document.getElementById("weather-shimmer-style")) {{
    const style = document.createElement("style");
    style.id = "weather-shimmer-style";
    style.textContent = "@keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}";
    document.head.appendChild(style);
  }}

  // Fetch weather for unique coords
  const coordMap = {{}};
  for (const loc of DAY_LOCATIONS) {{
    const key = `${{loc.lat}},${{loc.lon}}`;
    if (!coordMap[key]) {{
      coordMap[key] = fetchWeather(loc.lat, loc.lon);
    }}
  }}

  // Wait for all fetches
  const keys = Object.keys(coordMap);
  const results = await Promise.all(keys.map(k => coordMap[k]));
  const resolvedMap = {{}};
  keys.forEach((k, i) => {{ resolvedMap[k] = results[i]; }});

  // Replace placeholders with panels
  DAY_LOCATIONS.forEach((loc, idx) => {{
    const key = `${{loc.lat}},${{loc.lon}}`;
    const weatherData = resolvedMap[key];
    const periods = weatherData ? weatherData.daily : null;
    const forecast = findForecast(periods, loc.date);
    forecast.hourlyPrecip = extractHourlyPrecip(weatherData, loc.date);
    const panel = buildPanel(loc, forecast);

    if (placeholders[idx] && placeholders[idx].parentNode) {{
      placeholders[idx].parentNode.replaceChild(panel, placeholders[idx]);
    }}
  }});
}}

function enhanceRoadConditions() {{
  // Find all road sections
  const roadSections = document.querySelectorAll('[data-road-section]');
  if (!roadSections.length) return;
  
  roadSections.forEach((roadSection) => {{
    // Determine day number from the parent weather panel
    const panel = roadSection.closest('.weather-panel');
    if (!panel) return;
    const allPanels = Array.from(document.querySelectorAll('.weather-panel'));
    const dayNum = allPanels.indexOf(panel) + 1;
    if (dayNum < 1) return;
    
    // Add live NCDOT closures
    if (liveClosures[dayNum]) {{
      const liveDiv = document.createElement('div');
      liveDiv.style.cssText = 'margin-bottom:6px;';
      liveDiv.innerHTML = '<div style="font-size:0.78em;font-weight:600;color:#B45309;margin-bottom:3px;">🔴 Live Road Closures (NCDOT):</div>';
      for (const c of liveClosures[dayNum]) {{
        const el = document.createElement('div');
        el.style.cssText = 'font-size:0.82em;color:#DC2626;margin-bottom:2px;';
        el.textContent = '⛔ ' + c.road + ': ' + c.status + ' — ' + c.reason;
        liveDiv.appendChild(el);
      }}
      roadSection.insertBefore(liveDiv, roadSection.children[1]);
    }}
    
    // Add live BRP alerts for BRP days
    if ([6,7,8,10].includes(dayNum) && liveBRPAlerts.length > 0) {{
      const brpDiv = document.createElement('div');
      brpDiv.style.cssText = 'margin-bottom:6px;';
      brpDiv.innerHTML = '<div style="font-size:0.78em;font-weight:600;color:#B45309;margin-bottom:3px;">🔴 Live BRP Alerts (NPS):</div>';
      for (const alert of liveBRPAlerts) {{
        const el = document.createElement('div');
        el.style.cssText = 'font-size:0.82em;color:#DC2626;margin-bottom:2px;';
        el.textContent = (alert.category === 'Park Closure' ? '⛔ ' : '⚠️ ') + alert.title;
        brpDiv.appendChild(el);
      }}
      const linkEl = document.createElement('div');
      linkEl.style.cssText = 'font-size:0.75em;margin-top:2px;';
      linkEl.innerHTML = '<a href="https://www.nps.gov/blri/planyourvisit/roadclosures.htm" target="_blank" style="color:#15803d;">View full BRP closure details →</a>';
      brpDiv.appendChild(linkEl);
      
      // Find existing BRP section or append
      const existingBRP = Array.from(roadSection.querySelectorAll('div')).find(d => d.textContent.includes('Blue Ridge Parkway'));
      if (existingBRP) {{
        roadSection.insertBefore(brpDiv, existingBRP);
      }} else {{
        roadSection.appendChild(brpDiv);
      }}
    }}
    
    // Add timestamp
    if (roadDataTimestamp) {{
      let ts = roadSection.querySelector('.road-timestamp');
      if (!ts) {{
        ts = document.createElement('div');
        ts.className = 'road-timestamp';
        ts.style.cssText = 'font-size:0.7em;color:#999;margin-top:6px;font-style:italic;';
        roadSection.appendChild(ts);
      }}
      ts.textContent = 'Live data updated: ' + roadDataTimestamp;
    }}
  }});
}}


  // ============================================
  // REORDER: Days first, then reference sections
  // ============================================

  (function reorderSections() {{
    const container = document.querySelector('.content-wrap') || document.body;

    const daySections = Array.from(document.querySelectorAll('.day-section'));
    const detailsSections = Array.from(document.querySelectorAll('details'));

    const remainingH2s = [];
    document.querySelectorAll('h2').forEach(h2 => {{
      if (!h2.closest('.day-section') && !h2.closest('details')) {{
        const elements = [h2];
        let next = h2.nextElementSibling;
        while (next && next.tagName !== 'H2' && next.tagName !== 'DETAILS' && !next.classList.contains('day-section') && !next.classList.contains('hero') && !next.classList.contains('nav-bar')) {{
          elements.push(next);
          next = next.nextElementSibling;
        }}
        const details = document.createElement('details');
        details.className = 'reference-section';
        const summary = document.createElement('summary');
        summary.innerHTML = h2.innerHTML;
        summary.style.cssText = 'cursor:pointer;font-family:Fraunces,serif;font-size:1.15em;font-weight:600;padding:16px 22px;color:var(--forest);';
        details.appendChild(summary);
        const content = document.createElement('div');
        content.style.cssText = 'padding:0 22px 16px 22px;';
        elements.slice(1).forEach(el => content.appendChild(el));
        details.appendChild(content);
        remainingH2s.push({{ original: h2, details: details }});
      }}
    }});

    remainingH2s.forEach(item => {{
      if (item.original.parentNode) item.original.remove();
    }});

    const refContainer = document.createElement('div');
    refContainer.className = 'reference-container';
    refContainer.id = 'reference-sections';

    const refHeader = document.createElement('div');
    refHeader.style.cssText = 'background:linear-gradient(135deg,var(--forest) 0%,var(--forest-mid) 100%);color:var(--cream);padding:18px 26px;border-radius:var(--radius-lg) var(--radius-lg) 0 0;margin-top:32px;font-family:Fraunces,serif;font-size:1.3em;font-weight:700;';
    refHeader.textContent = 'Reference & Planning';
    refContainer.appendChild(refHeader);

    const refNav = document.createElement('div');
    refNav.className = 'ref-nav';
    refNav.style.cssText = 'display:flex;flex-wrap:wrap;gap:6px;padding:12px 22px;background:#f0fdf4;border-left:1px solid #e2e8f0;border-right:1px solid #e2e8f0;';

    const refOrder = [
      'Flexibility Guide',
      'Events Calendar',
      'Booking Checklist',
      'Road Condition',
      'Driving Summary',
      'Lodging Guide',
      'Land Scouting',
      'Scouting to Live',
      'Context',
      'Costco',
      'Vehicle Notes',
      'Horror',
      'Kid-Friendly',
      'Packing List'
    ];

    const allRef = [...detailsSections, ...remainingH2s.map(r => r.details)];

    const sorted = [];
    for (const keyword of refOrder) {{
      const found = allRef.find(el => {{
        const text = el.querySelector('summary')?.textContent || el.textContent;
        return text.includes(keyword);
      }});
      if (found) sorted.push(found);
    }}
    for (const el of allRef) {{
      if (!sorted.includes(el)) sorted.push(el);
    }}

    sorted.forEach((section, idx) => {{
      const summaryText = section.querySelector('summary')?.textContent.trim() || 'Section';
      const sectionId = 'ref-' + idx;
      section.id = sectionId;

      const pill = document.createElement('a');
      pill.href = '#' + sectionId;
      pill.textContent = summaryText.replace(/^[^\w]*/, '').substring(0, 30);
      pill.style.cssText = 'font-size:0.75em;padding:4px 10px;background:white;border:1px solid #bbf7d0;border-radius:20px;color:var(--forest);text-decoration:none;white-space:nowrap;font-family:Outfit,sans-serif;';
      refNav.appendChild(pill);

      refContainer.appendChild(section);
    }});

    const hero = document.querySelector('.hero');
    const navBar = document.querySelector('.nav-bar');
    // Insert days after hero banner (hero comes after nav-bar in DOM)
    let insertAfter = hero || navBar;

    if (insertAfter && insertAfter.parentNode) {{
      // Insert each day section after the hero
      let afterHero = insertAfter.nextSibling;
      daySections.forEach(ds => {{
        insertAfter.parentNode.insertBefore(ds, afterHero);
        // Update afterHero to be after the just-inserted day section
        afterHero = ds.nextSibling;
      }});

      refContainer.insertBefore(refNav, refContainer.children[1]);

      const lastDay = daySections[daySections.length - 1];
      if (lastDay && lastDay.nextSibling) {{
        lastDay.parentNode.insertBefore(refContainer, lastDay.nextSibling);
      }} else {{
        container.appendChild(refContainer);
      }}
    }}
  }})();

  // Clean up route connectors after reorder — remove all, re-add between adjacent day sections
  (function() {{
    document.querySelectorAll('.route-connector').forEach(el => el.remove());
    const days = document.querySelectorAll('.day-section');
    days.forEach((section, i) => {{
      if (i > 0) {{
        const connector = document.createElement('div');
        connector.className = 'route-connector';
        connector.innerHTML = '<div class="route-dot"></div>';
        section.parentNode.insertBefore(connector, section);
      }}
    }});
  }})();

  // Body-appended dropdown menu with backdrop
  (function() {{
    var menuBtn = document.getElementById("mainMenuBtn");
    if (!menuBtn) return;

    var menuItems = [
      {{href: "#ref-0", label: "Flexibility Guide"}},
      {{href: "#ref-1", label: "Events Calendar"}},
      {{href: "#ref-2", label: "Booking Checklist"}},
      {{href: "#ref-3", label: "Road Conditions"}},
      {{href: "#ref-4", label: "Driving Summary"}},
      {{href: "#ref-5", label: "Lodging Guide"}},
      {{href: "#ref-6", label: "Land Scouting"}},
      {{href: "#ref-7", label: "Scouting Summary"}},
      {{href: "#ref-8", label: "Context"}},
      {{href: "#ref-9", label: "Costco Locations"}},
      {{href: "#ref-10", label: "Vehicle Notes"}},
      {{href: "#ref-11", label: "Horror & Spooky Shops"}},
      {{href: "#ref-12", label: "Kid-Friendly Activities"}},
      {{href: "#ref-13", label: "Packing List"}}
    ];

    function closeMenu() {{
      var panel = document.querySelector(".menu-panel");
      var backdrop = document.querySelector(".menu-backdrop");
      if (panel) panel.remove();
      if (backdrop) backdrop.remove();
    }}

    menuBtn.addEventListener("click", function(e) {{
      e.stopPropagation();
      if (document.querySelector(".menu-panel")) {{
        closeMenu();
        return;
      }}

      var backdrop = document.createElement("div");
      backdrop.className = "menu-backdrop";
      backdrop.addEventListener("click", closeMenu);
      document.body.appendChild(backdrop);

      var panel = document.createElement("div");
      panel.className = "menu-panel";

      var header = document.createElement("div");
      header.className = "menu-panel-header";
      var headerText = document.createElement("span");
      headerText.textContent = "Jump to Section";
      header.appendChild(headerText);
      var closeBtn = document.createElement("button");
      closeBtn.className = "menu-close";
      closeBtn.innerHTML = "✕";
      closeBtn.addEventListener("click", closeMenu);
      header.appendChild(closeBtn);
      panel.appendChild(header);

      menuItems.forEach(function(item) {{
        var a = document.createElement("a");
        a.href = item.href;
        a.textContent = item.label;
        a.addEventListener("click", function(e) {{
          e.preventDefault();
          closeMenu();
          var targetId = item.href.replace('#', '');
          var target = document.getElementById(targetId);
          if (target) {{
            if (target.tagName === 'DETAILS' && !target.hasAttribute('open')) {{
              target.setAttribute('open', '');
            }}
            setTimeout(function() {{
              var navH = document.querySelector('.nav-bar') ? document.querySelector('.nav-bar').offsetHeight : 40;
              var rect = target.getBoundingClientRect();
              window.scrollTo({{ top: window.scrollY + rect.top - navH - 8, behavior: 'smooth' }});
            }}, 50);
          }}
        }});
        panel.appendChild(a);
      }});

      document.body.appendChild(panel);
      var btnRect = menuBtn.getBoundingClientRect();
      panel.style.top = (btnRect.bottom + 6) + "px";
      panel.style.left = Math.max(8, btnRect.left) + "px";
    }});

    document.addEventListener("keydown", function(e) {{
      if (e.key === "Escape") closeMenu();
    }});
  }})();

setTimeout(injectWeatherPanels, 500);

setTimeout(async function() {{
  await Promise.all([fetchNCDOTClosures(), fetchBRPAlerts()]);
  enhanceRoadConditions();
}}, 1500);
}});
</script>


<script>
// Open all external links in new tab
function openExternalLinksInNewTab(root) {{
  root.querySelectorAll('a[href]').forEach(function(a) {{
    var href = a.getAttribute('href');
    if (href && !href.startsWith('#')) {{
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'noopener noreferrer');
    }}
  }});
}}
document.addEventListener('DOMContentLoaded', function() {{
  openExternalLinksInNewTab(document);
  new MutationObserver(function(mutations) {{
    mutations.forEach(function(m) {{
      m.addedNodes.forEach(function(node) {{
        if (node.nodeType === 1) openExternalLinksInNewTab(node);
      }});
    }});
  }}).observe(document.body, {{ childList: true, subtree: true }});
}});
</script>
</body>
</html>
"""

# Add id anchors to Day headings and key sections
for day_num in range(1, 13):
    html_doc = re.sub(
        rf'<h2>Day {day_num}\b',
        f'<h2 id="day-{day_num}">Day {day_num}',
        html_doc
    )

section_anchors = {
    'Land Scouting': 'scouting',
    'Lodging Guide': 'lodging',
    'Booking Checklist': 'booking',
    'Scouting to Live Here': 'scouting-summary',
    'Political Landscape': 'politics',
    'Climate': 'climate',
}
for text, anchor_id in section_anchors.items():
    html_doc = re.sub(
        rf'<h2>([^<]*{text})',
        f'<h2 id="{anchor_id}">\\1',
        html_doc
    )

# Save
output_path = os.path.join(
    r"C:\Users\AB Digial\OneDrive\Documents\Claude",
    "road-trip-plan.html"
)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_doc)

print(f"HTML file saved to: {output_path}")
print(f"File size: {os.path.getsize(output_path):,} bytes")
