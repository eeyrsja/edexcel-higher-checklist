"""Build the subject index and AQA English Literature pages."""

from html import escape

from build import EDEXCEL_CSS, ROOT, main as build_maths
from build_past_papers import build_past_papers
from english_data import AQA, EXAMS, PMT_NOTES, TEXTS, paper_links

CSS = """
.hub{max-width:960px}
.hub nav{display:flex;gap:10px 18px;flex-wrap:wrap;margin:16px 0}
.hub nav a,.actions a{font-weight:650}
.hub main{margin-top:24px}
.hub main > section{margin-top:26px}
.hub h2{font-size:22px;margin:0 0 10px;line-height:1.25}
.hub h3{font-size:16px;margin:0 0 6px}
.hub p{margin:0 0 10px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}
.tile,.panel,.question,.topic-card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px}
.tile p,.question p,.muted{color:#4d626d}
.actions{display:flex;gap:6px 16px;flex-wrap:wrap;align-items:center}
.questions{display:grid;gap:8px}
.question{padding:12px 14px}
.question h3{margin:0 0 4px}
.topic-card{margin-bottom:10px}
.topic-card summary,.panel summary{cursor:pointer;font-size:16px;font-weight:700}
.topic-card[open] summary,.panel[open] summary{margin-bottom:10px}
.hub .hero p{margin:7px 0 0}
.hub .hero{grid-template-columns:1fr}
.practice{border-left:3px solid #83b9ae;padding:8px 12px;margin:12px 0;background:#f0f8f5}
.plot{margin:0;padding-left:22px}
.plot li{padding:4px 0}
"""

SELF_CHECK = (
    "Make a clear argument that answers the question.",
    "Use a precise reference from the extract and another from elsewhere in the text.",
    "Explain how the writer’s language, form or structure shapes the reader’s or audience’s response.",
    "Use context where it helps explain your interpretation.",
)


def external(label, url):
    return f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(label)} ↗</a>'


def page(filename, title, subtitle, navigation, body):
    nav = "".join(f'<a href="{url}">{label}</a>' for label, url in navigation)
    menu = f'<nav aria-label="Navigation">{nav}</nav>' if nav else ""
    legacy_redirect = """
<script>
  // Keep bookmarks to the old checklist sections and topics working.
  const hash = location.hash;
  const mathsSections = ['#number', '#algebra', '#geometrymeasures',
    '#probabilitystatistics', '#higheralgebrafunctions', '#checklist', '#speccoverage'];
  if (hash.startsWith('#topic-') || mathsSections.includes(hash)) {
    location.replace('maths.html' + hash);
  }
</script>""" if filename == "index.html" else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>{legacy_redirect}
<style>{EDEXCEL_CSS}{CSS}</style>
</head>
<body>
<div class="wrap hub">
  <header class="hero">
    <div class="hero-title">
      <img class="hero-logo" src="sjalogo.png" width="36" height="36" alt="SJA monogram">
      <div><h1>{title}</h1><p>{subtitle}</p></div>
    </div>
  </header>
{menu}
  <main>{body}</main>
</div>
</body>
</html>
"""
    (ROOT / "docs" / filename).write_text(html, encoding="utf-8")


def question_card(exam, text):
    series, year, macbeth, frankenstein = exam
    is_play = text == "macbeth"
    title, location = macbeth if is_play else frankenstein
    component, paper, scheme = paper_links(year, text)
    number = "1" if is_play else "5" if component == "8702/1N" else "11"
    label = f'{TEXTS[text]["title"]} · {series}'
    return f"""<article class="question">
      <h3>{escape(label)} · {escape(title)}</h3>
      <p>{location} · {component}, Question {number}</p>
      <div class="actions">
        {external(f"Question paper", paper)}
        {external(f"Mark scheme", scheme)}
      </div>
    </article>"""


def build_text(slug, text):
    plot = "".join(f"<li><strong>{location}</strong> · {summary}</li>" for location, summary in text["plot"])
    topics = []
    for title, note, prompt, years in text["topics"]:
        links = "".join(
            f'<li><a href="#exam-{exam[1]}">{exam[0]} · {escape(exam[2 if slug == "macbeth" else 3][0])}</a></li>'
            for exam in EXAMS if exam[1] in years
        )
        topics.append(f"""<details class="topic-card">
          <summary>{escape(title)}</summary>
          <p>{escape(note)}</p>
          <div class="practice"><strong>Practice question</strong><br>{escape(prompt)}</div>
          <p>Spend five minutes planning an answer. Then write one paragraph using evidence from two points in the text.</p>
          <strong>Related AQA questions</strong><ul>{links}</ul>
        </details>""")
    checks = SELF_CHECK
    if slug == "macbeth":
        checks += ("Check your spelling, punctuation and sentence clarity for AO4.",)
    checklist = "".join(f"<li>{check}</li>" for check in checks)
    questions = "".join(f'<div id="exam-{exam[1]}">{question_card(exam, slug)}</div>' for exam in EXAMS)
    body = f"""
      <div class="actions">
        {external("Read the full text", text["reading"])}
        {external("PMT revision notes", PMT_NOTES + slug + "/")}
        {external("BBC guided essay", text["guided"])}
      </div>
      <section id="plot"><h2>Plot at a glance</h2><ol class="plot">{plot}</ol></section>
      <section id="topics"><h2>Revise by topic</h2>{"".join(topics)}
        <details class="panel"><summary>Check your answer</summary><ul>{checklist}</ul></details>
      </section>
      <section id="questions"><h2>Past and specimen questions</h2><div class="questions">{questions}</div></section>"""
    page(
        f"{slug}.html", text["title"], f'{text["author"]} · {text["section"]}',
        (("All subjects", "./"), ("English Literature", "english.html"), ("Plot", "#plot"),
         ("Topics", "#topics"), ("Exam questions", "#questions")), body,
    )


def build_english():
    for slug, text in TEXTS.items():
        build_text(slug, text)

    archive = []
    for exam in EXAMS:
        if exam[1] in {"2021", "2022"}:
            heading = f'{exam[0]} · papers split by text'
            cards = "".join(question_card(exam, slug) for slug in TEXTS)
        else:
            heading = exam[0]
            _, paper, scheme = paper_links(exam[1], "macbeth")
            cards = f"""<div class="actions">
              <a href="macbeth.html#exam-{exam[1]}">Macbeth · Q1</a>
              <a href="frankenstein.html#exam-{exam[1]}">Frankenstein · Q11</a>
              {external("Question paper", paper)} {external("Mark scheme", scheme)}
            </div>"""
        archive.append(f'<div class="question"><h3>{heading}</h3>{cards}</div>')
    page("english.html", "AQA English Literature", "GCSE 8702 · Macbeth and Frankenstein",
         (("All subjects", "./"), ("How it’s marked", "#marking"), ("Past papers", "#past-papers")),
         f"""
      <div class="cards">
        <article class="tile"><h2><a href="macbeth.html">Macbeth</a></h2><p>William Shakespeare · 34 marks</p></article>
        <article class="tile"><h2><a href="frankenstein.html">Frankenstein</a></h2><p>Mary Shelley · 1831 edition · 30 marks</p></article>
      </div>
      <section id="marking">
        <h2>How Paper 1 is marked</h2>
        <div class="panel">
          <p>In the current format you have 1 hour 45 minutes for two essays. Use the printed extract and examples from across the play or novel.</p>
          <ul>
            <li><strong>AO1</strong> · Make an argument and support it with references.</li>
            <li><strong>AO2</strong> · Explain how the writer uses language, form and structure.</li>
            <li><strong>AO3</strong> · Use context that helps explain your reading of the text.</li>
            <li><strong>AO4</strong> · Write clearly and accurately. Macbeth carries four marks for this.</li>
          </ul>
          <div class="actions">
            {external("AQA assessment objectives", AQA + "/subjects/english/gcse/english-8702/specification/scheme-of-assessment")}
            {external("AQA assessment resources", AQA + "/subjects/english/gcse/english-8702/assessment-resources")}
          </div>
        </div>
      </section>
      <section id="past-papers">
        <h2>Past papers</h2>
        <p>For November 2021 and June 2022, use Paper 2 for Macbeth and Paper 1N for Frankenstein.</p>
        <div class="questions">{"".join(archive)}</div>
      </section>""")


def build_home():
    page("index.html", "GCSE Revision", "Choose a subject", (), """
      <div class="cards">
        <article class="tile">
          <h2>Edexcel Higher GCSE Maths</h2>
          <p>Topic videos, worksheets and online practice.</p>
          <div class="actions"><a href="maths.html">Revision checklist</a><a href="past-papers.html">Past papers</a></div>
        </article>
        <article class="tile">
          <h2>AQA English Literature</h2>
          <p>Topic revision, essay practice and past questions.</p>
          <div class="actions"><a href="macbeth.html">Macbeth</a><a href="frankenstein.html">Frankenstein</a><a href="english.html">Exam guide and papers</a></div>
        </article>
      </div>""")


if __name__ == "__main__":
    build_maths()
    build_past_papers()
    build_home()
    build_english()
