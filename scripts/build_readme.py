#!/usr/bin/env python3
"""Builds README.md from awards.csv.

    python scripts/build_readme.py           # check awards.csv, then write README.md
    python scripts/build_readme.py --check   # check awards.csv only

It needs Python 3 and nothing else. The text above and below the tables lives in
scripts/readme_header.md and scripts/readme_footer.md.
"""
import csv
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ["category", "name", "organization", "url", "eligibility", "support", "deadline",
          "deadline_month", "verified"]
CATEGORIES = [
    ("students", "Student paper awards and student travel awards"),
    ("asa-sections", "ASA section competitions for the Joint Statistical Meetings"),
    ("early-career", "Early-career awards and travel grants"),
    ("conferences", "Conference support in mathematics, machine learning, computational biology and R"),
    ("other", "Scholarships and other support"),
]
ASA_NOTE = (
    "Most sections of the American Statistical Association run a student or early-career paper "
    "competition for JSM. The [ASA page](https://www.amstat.org/your-career/student-paper-competitions) "
    "sets the common rules: sections must receive all materials by November 15 (some sections close "
    "earlier or later), a student may enter at most two sections and accept one award, and winners "
    "hear by January 15.\n"
)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]


def read_awards():
    """Reads and checks awards.csv. Returns the rows, or stops with a list of problems."""
    path = ROOT / "awards.csv"
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            sys.exit(f"awards.csv: the header row must be exactly:\n{','.join(FIELDS)}")
        rows = list(reader)
    problems = []
    known = {key for key, _ in CATEGORIES}
    for n, r in enumerate(rows, start=2):
        where = f"line {n} ({r['name'] or 'no name'})"
        for field in ("category", "name", "organization", "url", "eligibility", "support",
                      "deadline", "verified"):
            if not (r[field] or "").strip():
                problems.append(f"{where}: '{field}' is empty")
        if r["category"] not in known:
            problems.append(f"{where}: category must be one of {', '.join(sorted(known))}")
        if not r["url"].startswith("https://"):
            problems.append(f"{where}: url must start with https://")
        if r["deadline_month"] and r["deadline_month"] not in [str(m) for m in range(1, 13)]:
            problems.append(f"{where}: deadline_month must be a number from 1 to 12, or empty")
        if r["verified"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["verified"]):
            problems.append(f"{where}: verified must look like 2026-10-03")
        if any("|" in (v or "") for v in r.values()):
            problems.append(f"{where}: the character | cannot be used")
    if problems:
        sys.exit("awards.csv has problems:\n  " + "\n  ".join(problems))
    return rows


def pretty(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def table(rows, asa=False):
    first = "Section" if asa else "Award"
    out = [f"| {first} | Who can apply | What it covers | Deadline |",
           "|---|---|---|---|"]
    for r in rows:
        if asa:
            label = f"{r['organization'].replace('ASA ', '', 1)}<br>[{r['name']}]({r['url']})"
        else:
            label = f"[{r['name']}]({r['url']})<br><sub>{r['organization']}</sub>"
        out.append(f"| {label} | {r['eligibility']} | {r['support']} | **{r['deadline']}** |")
    return "\n".join(out) + "\n"


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def build(rows):
    verified = max(r["verified"] for r in rows)
    parts = [(ROOT / "scripts" / "readme_header.md").read_text(encoding="utf-8").rstrip() + "\n"]
    parts.append(f"**{len(rows)} awards. Last verified against the official pages on {pretty(verified)}.**\n")

    parts.append("## Contents\n")
    toc = [f"- [{title}](#{anchor(title)})" for _, title in CATEGORIES]
    toc += ["- [Deadlines by month](#deadlines-by-month)", "- [Help wanted](#help-wanted)",
            "- [Contributing](#contributing)"]
    parts.append("\n".join(toc) + "\n")

    for key, title in CATEGORIES:
        parts.append(f"## {title}\n")
        if key == "asa-sections":
            parts.append(ASA_NOTE)
        parts.append(table([r for r in rows if r["category"] == key], asa=(key == "asa-sections")))

    parts.append("## Deadlines by month\n")
    parts.append("The month in which each call usually closes. Awards whose deadline varies by "
                 "conference are left out.\n")
    lines = []
    for m in range(1, 13):
        names = [f"[{r['name']}]({r['url']})" + (f" ({r['organization'].replace('ASA ', '', 1)})"
                                                   if r["category"] == "asa-sections" else "")
                 for r in rows if r["deadline_month"] == str(m)]
        if names:
            lines.append(f"- **{MONTHS[m - 1]}:** " + "; ".join(names))
    parts.append("\n".join(lines) + "\n")

    parts.append((ROOT / "scripts" / "readme_footer.md").read_text(encoding="utf-8").rstrip() + "\n")
    return "\n".join(parts)


def main():
    rows = read_awards()
    if "--check" in sys.argv:
        print(f"awards.csv is fine: {len(rows)} awards.")
        return
    text = build(rows)
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md written: {len(rows)} awards.")


if __name__ == "__main__":
    main()
