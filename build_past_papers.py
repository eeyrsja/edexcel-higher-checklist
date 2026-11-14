"""Generate the Past Papers page from the verified link catalogue."""

import json
from html import escape

from build import EDEXCEL_CSS, ROOT

PAGE_CSS = """
.paper-list{max-width:780px;margin:24px auto}
.paper-list h2{margin:0 0 8px;font-size:18px}
.paper-list section{margin:0 0 22px}
.paper-list ul{list-style:none;margin:0;padding:0;border:1px solid var(--line);
  border-radius:8px;background:#fff}
.paper-list li{display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:6px 16px;padding:10px 14px}
.paper-list li+li{border-top:1px solid var(--line)}
.paper-links{display:flex;flex-wrap:wrap;gap:6px 16px}
"""

def build_past_papers():
    catalogue = json.loads((ROOT / "past_papers.json").read_text(encoding="utf-8"))
    sections = []
    for series, papers in catalogue.items():
        rows = []
        for number, links in papers.items():
            calculator = "Non-calculator" if number == "1" else "Calculator"
            resources = []
            for label, url in links.items():
                resources.append(
                    f'<a href="{escape(url)}" target="_blank" rel="noopener" '
                    f'aria-label="{escape(series)} Paper {number}, {label} (PDF)">'
                    f'{label}</a>'
                )
            rows.append(
                f'<li><span><strong>Paper {number}</strong> · {calculator}</span>'
                f'<div class="paper-links">{"".join(resources)}</div></li>'
            )
        sections.append(f'<section><h2>{escape(series)}</h2><ul>{"".join(rows)}</ul></section>')

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Past Papers | Edexcel Higher GCSE Maths</title>
<style>{EDEXCEL_CSS}{PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="hero-title">
      <img class="hero-logo" src="sjalogo.png" width="36" height="36" alt="SJA monogram">
      <h1>Past papers</h1>
    </div>
    <a href="./">← Revision checklist</a>
  </header>
  <main class="paper-list">
    <p>Edexcel Higher GCSE Maths (1MA1). PDF links open in a new tab.</p>
    {"".join(sections)}
  </main>
</div>
</body>
</html>
"""
    (ROOT / "docs" / "past-papers.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build_past_papers()
