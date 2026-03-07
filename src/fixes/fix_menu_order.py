#!/usr/bin/env python3
import sys, os

TARGET = r"C:\Users\AB Digial\OneDrive\Documents\Claude\create_html.py"

CSS_BLOCK = (
    '\n'
    '  /* ===== REFERENCE SECTIONS ===== */\n'
    '  .reference-container {{\n'
    '    background: white;\n'
    '    border-radius: var(--radius-lg);\n'
    '    box-shadow: var(--shadow-md);\n'
    '    margin-top: 32px;\n'
    '    overflow: hidden;\n'
    '  }}\n'
    '  .reference-container details {{\n'
    '    border-bottom: 1px solid #e2e8f0;\n'
    '  }}\n'
    '  .reference-container details:last-child {{\n'
    '    border-bottom: none;\n'
    '  }}\n'
    '  .ref-nav a:hover {{\n'
    '    background: var(--forest) !important;\n'
    '    color: white !important;\n'
    '  }}\n'
    '\n'
)

JS_BLOCK = (
    '\n'
    '  // ============================================\n'
    '  // REORDER: Days first, then reference sections\n'
    '  // ============================================\n'
    '\n'
    '  (function reorderSections() {{\n'
    "    const container = document.querySelector('.content-wrap') || document.body;\n"
    '\n'
    "    const daySections = Array.from(document.querySelectorAll('.day-section'));\n"
    "    const detailsSections = Array.from(document.querySelectorAll('details'));\n"
    '\n'
    '    const remainingH2s = [];\n'
    "    document.querySelectorAll('h2').forEach(h2 => {{\n"
    "      if (!h2.closest('.day-section') && !h2.closest('details')) {{\n"
    '        const elements = [h2];\n'
    '        let next = h2.nextElementSibling;\n'
    "        while (next && next.tagName !== 'H2' && next.tagName !== 'DETAILS' && !next.classList.contains('day-section') && !next.classList.contains('hero-card') && !next.classList.contains('day-tabs')) {{\n"
    '          elements.push(next);\n'
    '          next = next.nextElementSibling;\n'
    '        }}\n'
    "        const details = document.createElement('details');\n"
    "        details.className = 'reference-section';\n"
    "        const summary = document.createElement('summary');\n"
    '        summary.innerHTML = h2.innerHTML;\n'
    "        summary.style.cssText = 'cursor:pointer;font-family:Fraunces,serif;font-size:1.15em;font-weight:600;padding:16px 22px;color:var(--forest);';\n"
    '        details.appendChild(summary);\n'
    "        const content = document.createElement('div');\n"
    "        content.style.cssText = 'padding:0 22px 16px 22px;';\n"
    '        elements.slice(1).forEach(el => content.appendChild(el));\n'
    '        details.appendChild(content);\n'
    '        remainingH2s.push({{ original: h2, details: details }});\n'
    '      }}\n'
    '    }});\n'
    '\n'
    '    remainingH2s.forEach(item => {{\n'
    '      if (item.original.parentNode) item.original.remove();\n'
    '    }});\n'
    '\n'
    "    const refContainer = document.createElement('div');\n"
    "    refContainer.className = 'reference-container';\n"
    "    refContainer.id = 'reference-sections';\n"
    '\n'
    "    const refHeader = document.createElement('div');\n"
    "    refHeader.style.cssText = 'background:linear-gradient(135deg,var(--forest) 0%,var(--forest-mid) 100%);color:var(--cream);padding:18px 26px;border-radius:var(--radius-lg) var(--radius-lg) 0 0;margin-top:32px;font-family:Fraunces,serif;font-size:1.3em;font-weight:700;';\n"
    "    refHeader.textContent = 'Reference & Planning';\n"
    '    refContainer.appendChild(refHeader);\n'
    '\n'
    "    const refNav = document.createElement('div');\n"
    "    refNav.className = 'ref-nav';\n"
    "    refNav.style.cssText = 'display:flex;flex-wrap:wrap;gap:6px;padding:12px 22px;background:#f0fdf4;border-left:1px solid #e2e8f0;border-right:1px solid #e2e8f0;';\n"
    '\n'
    '    const refOrder = [\n'
    "      'Flexibility Guide',\n"
    "      'Events Calendar',\n"
    "      'Booking Checklist',\n"
    "      'Road Condition',\n"
    "      'Driving Summary',\n"
    "      'Lodging Guide',\n"
    "      'Land Scouting',\n"
    "      'Scouting to Live',\n"
    "      'Context',\n"
    "      'Costco',\n"
    "      'Vehicle Notes',\n"
    "      'Horror',\n"
    "      'Kid-Friendly',\n"
    "      'Packing List'\n"
    '    ];\n'
    '\n'
    '    const allRef = [...detailsSections, ...remainingH2s.map(r => r.details)];\n'
    '\n'
    '    const sorted = [];\n'
    '    for (const keyword of refOrder) {{\n'
    '      const found = allRef.find(el => {{\n'
    "        const text = el.querySelector('summary')?.textContent || el.textContent;\n"
    '        return text.includes(keyword);\n'
    '      }});\n'
    '      if (found) sorted.push(found);\n'
    '    }}\n'
    '    for (const el of allRef) {{\n'
    '      if (!sorted.includes(el)) sorted.push(el);\n'
    '    }}\n'
    '\n'
    '    sorted.forEach((section, idx) => {{\n'
    "      const summaryText = section.querySelector('summary')?.textContent.trim() || 'Section';\n"
    "      const sectionId = 'ref-' + idx;\n"
    '      section.id = sectionId;\n'
    '\n'
    "      const pill = document.createElement('a');\n"
    "      pill.href = '#' + sectionId;\n"
    "      pill.textContent = summaryText.replace(/^[^\\w]*/, '').substring(0, 30);\n"
    "      pill.style.cssText = 'font-size:0.75em;padding:4px 10px;background:white;border:1px solid #bbf7d0;border-radius:20px;color:var(--forest);text-decoration:none;white-space:nowrap;font-family:Outfit,sans-serif;';\n"
    '      refNav.appendChild(pill);\n'
    '\n'
    '      refContainer.appendChild(section);\n'
    '    }});\n'
    '\n'
    "    const hero = document.querySelector('.hero-card');\n"
    "    const dayTabs = document.querySelector('.day-tabs');\n"
    '    let insertAfter = dayTabs || hero;\n'
    '\n'
    '    if (insertAfter && insertAfter.parentNode) {{\n'
    '      let insertPoint = insertAfter.nextSibling;\n'
    '\n'
    '      daySections.forEach(ds => {{\n'
    '        insertAfter.parentNode.insertBefore(ds, insertPoint);\n'
    '      }});\n'
    '\n'
    '      refContainer.insertBefore(refNav, refContainer.children[1]);\n'
    '\n'
    '      const lastDay = daySections[daySections.length - 1];\n'
    '      if (lastDay && lastDay.nextSibling) {{\n'
    '        lastDay.parentNode.insertBefore(refContainer, lastDay.nextSibling);\n'
    '      }} else {{\n'
    '        container.appendChild(refContainer);\n'
    '      }}\n'
    '    }}\n'
    '  }})();\n'
    '\n'
)



def main():
    if not os.path.isfile(TARGET):
        print(f"ERROR: File not found: {TARGET}")
        return 1

    with open(TARGET, "r", encoding="utf-8") as f:
        content = f.read()

    css_marker = "  /* ===== MOBILE ===== */"
    if css_marker not in content:
        print("ERROR: Could not find CSS marker")
        return 1

    if "/* ===== REFERENCE SECTIONS ===== */" in content:
        print("INFO: CSS block already present, skipping CSS insertion.")
    else:
        content = content.replace(css_marker, CSS_BLOCK + chr(10) + css_marker, 1)
        print("OK: Inserted CSS for .reference-container and .ref-nav")

    js_marker = "setTimeout(injectWeatherPanels, 500);"
    if js_marker not in content:
        print("ERROR: Could not find JS marker")
        return 1

    if "REORDER: Days first, then reference sections" in content:
        print("INFO: JS block already present, skipping JS insertion.")
    else:
        content = content.replace(js_marker, JS_BLOCK + js_marker, 1)
        print("OK: Inserted JS reorder/menu code before setTimeout")

    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"SUCCESS: {TARGET} has been updated.")
    print("  - CSS for reference-container and ref-nav added before MOBILE section")
    print("  - JS reorder + reference nav menu added before setTimeout(injectWeatherPanels)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
