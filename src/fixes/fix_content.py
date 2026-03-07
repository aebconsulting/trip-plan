#!/usr/bin/env python3
"""fix_content.py"""
import re

FILE_PATH = r"C:\Users\AB Digial\.claude\plans\typed-dancing-adleman.md"

def main():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    counts = {}
    def tracked_replace(label, old, new, text):
        n = text.count(old)
        counts[label] = n
        return text.replace(old, new)

    # C2-03
    content = tracked_replace(
        "C2-03: Trim visiting line",
        " Visiting Asheville, Hendersonville/Flat Rock, Black Mountain, and Boone/Blowing Rock areas. Friend from Greenville, SC will meet you in the Asheville area.",
        " Visiting Asheville, Hendersonville/Flat Rock, Black Mountain, and Boone/Blowing Rock areas.",
        content)

    # C2-02
    content = tracked_replace(
        "C2-02: Remove standalone Friend from Greenville",
        "Friend from Greenville, SC will meet you in the Asheville area.",
        "", content)

    # C2-04
    content = tracked_replace(
        "C2-04: Day 5 summary",
        "- **Day 5 (Sun, March 15) \u2014 Biltmore** \u2014 weekend day for your friend to join",
        "- **Day 5 (Sun, March 15) \u2014 Biltmore** \u2014 weekend day",
        content)

    # C2-05
    content = tracked_replace(
        "C2-05: Remove Day 4 italicized intro",
        "*Great day to invite your Greenville friend \u2014 Hendersonville is only ~45 min from them! Their kids (ages 1 & 4) will love the goats and the children\u2019s museum.*",
        "", content)

    # C2-06
    content = tracked_replace(
        "C2-06: Remove Day 5 italicized intro",
        "*Great day to invite your Greenville friend for a second day! Weekend = easier for them. Their kids (ages 1 & 4) will love the Farmyard animals. Biltmore\u2019s flat trails work for strollers too.*",
        "", content)

    # C2-07
    content = tracked_replace(
        "C2-07: Remove (Perfect for...)",
        "(Perfect for your friend\u2019s 1 & 4-year-old too)",
        "", content)

    # C2-08
    content = tracked_replace(
        "C2-08: Trim Great for ages line",
        "Great for ages 1\u20138 \u2014 perfect for your friend\u2019s little ones too.",
        "Great for ages 1\u20138.",
        content)

    # C2-09
    content = tracked_replace(
        "C2-09: Remove Stroller-friendly line",
        "Stroller-friendly for your friend\u2019s 1-year-old.",
        "", content)

    # C2-10
    content = tracked_replace(
        "C2-10: Rewrite son may or may not line",
        "your son may or may not enjoy this; friend\u2019s toddlers probably won\u2019t",
        "Ethan may or may not enjoy this",
        content)

    # C2-11
    content = tracked_replace(
        "C2-11: Remove visit your friend from Greenville stop",
        "- **Greenville, SC stop: 10 Hub St, Greenville, SC 29601** (~260 mi / ~4 hrs from cemetery) \u2014 visit your friend, grab lunch, explore the area. **Allow 1\u20132 hours.** Near downtown Greenville \u2014 walking distance to Main Street, the Commons, and the Swamp Rabbit Trail.",
        "- **Greenville, SC stop: 10 Hub St, Greenville, SC 29601** (~260 mi / ~4 hrs from cemetery) \u2014 grab lunch, explore the area. **Allow 1\u20132 hours.** Near downtown Greenville \u2014 walking distance to Main Street, the Commons, and the Swamp Rabbit Trail.",
        content)

    # C2-12
    content = tracked_replace(
        "C2-12: Remove Coordinate with Greenville friend block",
        "**Coordinate with Greenville friend** (2 kids, ages 1 & 4) \u2014 best days: **Day 4 Sat, March 14 (Hendersonville)** + **Day 5 Sun, March 15 (Biltmore)**. Both are weekend days \u2014 Hendersonville is toddler heaven (goats, children\u2019s museum), Biltmore has Farmyard + stroller-friendly trails.",
        "", content)

    # C2-13
    content = tracked_replace("C2-13: Remove remaining visit your friend", "visit your friend, ", "", content)

    # C2-16
    content = tracked_replace("C2-16: Remove (friend joins!)", "(friend joins!)", "", content)

    # C2-14
    content = tracked_replace("C2-14: Remove remaining your friend", "your friend", "", content)

    # C2-15
    content = tracked_replace("C2-15: Remove remaining friend joins", "friend joins", "", content)

    # C2-17a
    content = tracked_replace("C2-17a: Remove remaining friend smart-quote-s", "friend\u2019s", "", content)
    content = tracked_replace("C2-17b: Remove remaining friend straight-quote-s", "friend's", "", content)

    # === SECOND PASS: straight-quote variants that the first pass missed ===
    # C2-05 straight quote variant
    content = tracked_replace(
        "C2-05b: Day 4 intro (straight quote)",
        "*Great day to invite your Greenville friend — Hendersonville is only ~45 min from them! Their kids (ages 1 & 4) will love the goats and the children's museum.*",
        "", content)
    # C2-06 straight quote variant
    content = tracked_replace(
        "C2-06b: Day 5 intro (straight quote)",
        "*Great day to invite your Greenville friend for a second day! Weekend = easier for them. Their kids (ages 1 & 4) will love the Farmyard animals. Biltmore's flat trails work for strollers too.*",
        "", content)
    # C2-12 straight quote variant
    content = tracked_replace(
        "C2-12b: Coordinate block (straight quote)",
        "**Coordinate with Greenville friend** (2 kids, ages 1 & 4) — best days: **Day 4 Sat, March 14 (Hendersonville)** + **Day 5 Sun, March 15 (Biltmore)**. Both are weekend days — Hendersonville is toddler heaven (goats, children's museum), Biltmore has Farmyard + stroller-friendly trails.",
        "", content)
    # Fix broken stroller fragment
    content = tracked_replace("C2-09b: Broken stroller fragment", "Stroller-friendly for 's 1-year-old.", "", content)
    # Table cell
    content = tracked_replace("TABLE: Visit with friend", "*Visit with friend + lunch*", "*Grab lunch, explore area*", content)
    # Son in loft description
    content = tracked_replace("SON-LOFT: son gets his own", "(son gets his own loft space!)", "(Ethan gets his own loft space!)", content)

    # C3-01
    content = tracked_replace("C3-01: Header family line", "**Family of 3 (couple + son, age 5\u20138)**", "**Family of 3 (couple + Ethan, age 8)**", content)
    # C3-02
    content = tracked_replace("C3-02: remaining couple + son age 5-8", "couple + son, age 5\u20138", "couple + Ethan, age 8", content)

    # C4-01
    content = tracked_replace("C4-01: little one -> Ethan", "with indoor backup plans for each day when the little one gets tired.", "with indoor backup plans for each day when Ethan gets tired.", content)

    # C1-01
    content = tracked_replace("C1-01: son age 5-8", "son, age 5\u20138", "Ethan, age 8", content)
    # C1-02
    content = tracked_replace("C1-02: your son", "your son", "Ethan", content)
    # C1-03
    content = tracked_replace("C1-03: Your son", "Your son", "Ethan", content)
    # C1-04 son quote s regex
    for quote_char, label_suffix in [("\u2019", "smart"), ("'", "straight")]:
        pattern = r"(?<![a-zA-Z])son" + re.escape(quote_char) + r"s"
        matches = re.findall(pattern, content)
        counts[f"C1-04: standalone son-quote-s ({label_suffix})"] = len(matches)
        content = re.sub(pattern, f"Ethan{quote_char}s", content)

    # C1-05 son (
    pattern = r"(?<![a-zA-Z])son \("
    matches = re.findall(pattern, content)
    counts["C1-05: standalone son ("] = len(matches)
    content = re.sub(pattern, "Ethan (", content)

    # Final sweep
    content = tracked_replace("FINAL: remaining your son", "your son", "Ethan", content)
    content = tracked_replace("FINAL: remaining Your son", "Your son", "Ethan", content)

    # Cleanup blank lines
    before_cleanup = content
    content = re.sub(r'\n{3,}', '\n\n', content)
    collapsed = len(re.findall(r'\n{3,}', before_cleanup))
    counts["CLEANUP: collapsed excess blank lines"] = collapsed

    # Write
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    # Report
    print("=" * 70)
    print("REPLACEMENT REPORT")
    print("=" * 70)
    total = 0
    for label, n in counts.items():
        status = f"{n} replacement(s)" if n > 0 else "0 (not found)"
        print(f"  {label}: {status}")
        total += n
    print("-" * 70)
    print(f"  TOTAL replacements made: {total}")
    print("=" * 70)

    # Verification
    print("\nVERIFICATION - scanning for remaining references:")
    checks = [
        "your son", "Your son", "your friend", "friend joins",
        "friend's", "friend\u2019s", "(friend joins!)",
        "the little one gets tired",
        "couple + son, age 5",
    ]
    any_found = False
    for phrase in checks:
        c = content.count(phrase)
        if c > 0:
            print(f"  WARNING: '{phrase}' still appears {c} time(s)")
            any_found = True
    if not any_found:
        print("  All clear - no unwanted references remain.")
    ethan_count = content.count("Ethan")
    print(f"\n  'Ethan' now appears {ethan_count} time(s) in the file.")
    print("\nDone. File saved.")

if __name__ == "__main__":
    main()
