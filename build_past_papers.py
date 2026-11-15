"""Generate the Past Papers page from the verified link catalogue."""

import json
from html import escape

from build import EDEXCEL_CSS, ROOT

PAGE_CSS = """
.paper-list{max-width:780px;margin:24px auto}
.paper-list h2{margin:0 0 8px;font-size:18px}
.paper-list section{margin:0 0 22px}
.paper-list h3{margin:0 0 8px;font-size:16px}
.paper-archive{border-top:1px solid var(--line);padding-top:20px}
.paper-archive details{margin:0 0 14px}
.paper-archive summary{cursor:pointer;padding:8px 0;font-weight:650}
.paper-list ul{list-style:none;margin:0;padding:0;border:1px solid var(--line);
  border-radius:8px;background:#fff}
.paper-list li{display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:6px 16px;padding:10px 14px}
.paper-list li+li{border-top:1px solid var(--line)}
.paper-links{display:flex;flex-wrap:wrap;gap:6px 16px}
"""

def render_series(catalogue, *, specification=""):
    sections = []
    for series, papers in catalogue.items():
        rows = []
        for number, links in papers.items():
            paper = f"Paper {number}"
            if not specification:
                calculator = "Non-calculator" if number == "1" else "Calculator"
                paper += f" · {calculator}"
            context = f"{specification} {series}".strip()
            resources = []
            for label in ("Question paper", "Mark scheme"):
                url = links.get(label)
                if url is None:
                    resources.append('<span>Mark scheme unavailable</span>')
                    continue
                resources.append(
                    f'<a href="{escape(url)}" target="_blank" rel="noopener" '
                    f'aria-label="{escape(context)} Paper {number}, {label} (PDF)">'
                    f'{label}</a>'
                )
            rows.append(
                f'<li><span><strong>{paper}</strong></span>'
                f'<div class="paper-links">{"".join(resources)}</div></li>'
            )
        sections.append(
            f'<section><h3>{escape(series)}</h3><ul>{"".join(rows)}</ul></section>'
        )
    return "".join(sections)


def build_past_papers():
    current = json.loads((ROOT / "past_papers.json").read_text(encoding="utf-8"))
    legacy = json.loads((ROOT / "legacy_papers.json").read_text(encoding="utf-8"))
    archive = "".join(
        f'<details><summary>{escape(name)}</summary>'
        f'{render_series(series, specification=name)}</details>'
        for name, series in legacy.items()
    )

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
    <a href="maths.html">← Maths checklist</a>
  </header>
  <main class="paper-list">
    <p>PDF links open in a new tab. <a href="#older-papers">Jump to older specifications</a></p>
    <h2>Current specification (1MA1)</h2>
    {render_series(current)}
    <section class="paper-archive" id="older-papers">
      <h2>Older specifications</h2>
      <p>Higher papers for extra practice. The topics and exam format can differ from 1MA1.</p>
      {archive}
    </section>
  </main>
</div>
</body>
</html>
"""
    (ROOT / "docs" / "past-papers.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build_past_papers()
