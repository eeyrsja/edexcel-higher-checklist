"""Build the subject index and AQA English Literature pages."""

from html import escape

from build import EDEXCEL_CSS, ROOT, main as build_maths
from build_past_papers import build_past_papers
from english_practice import PRACTICE
from english_reader import SOURCES, read_sections, reading_anchor
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
.question>summary{cursor:pointer;padding:2px 0;font-weight:700;font-size:16px}
.question[open]>summary{margin-bottom:8px}
.marking-notes{margin:12px 0;color:var(--ink)}
.marking-notes summary{cursor:pointer;font-weight:650}
.marking-notes li{margin:7px 0}
.question-layout{display:grid;gap:14px;align-items:start}
.question-layout:has(.question-reader[open]){grid-template-columns:minmax(0,1fr) minmax(0,1.25fr)}
.question-reader{min-width:0;border:1px solid var(--line);border-radius:8px;background:#f5f7f6}
.question-reader summary{padding:8px 10px;color:var(--teal);cursor:pointer;font-weight:650}
.question-reader iframe{display:block;width:100%;height:clamp(340px,63dvh,650px);border:0;border-top:1px solid var(--line)}
@media(max-width:700px){
  .question-layout:has(.question-reader[open]){grid-template-columns:minmax(0,1fr)}
  .question-reader iframe{height:clamp(260px,45dvh,480px)}
}
.reader-in-pane{scroll-padding-top:120px}
.reader-in-pane .wrap{padding:10px 12px}
.reader-in-pane .hero,.reader-in-pane nav{display:none}
.reader-in-pane .hub main{margin-top:0}
.reader-in-pane .reader-panel{position:sticky;top:0;z-index:1;padding:8px}
.reader-in-pane .reader-controls{gap:6px 10px}
.reader-in-pane .reader-controls label{flex-basis:135px}
.reader-in-pane .text-results{max-height:100px;overflow:auto;margin-bottom:0}
.reader-in-pane .reading-copy{font-size:16px}
.question .references{border-top:1px solid var(--line);padding-top:9px;font-size:13px}
.reader-controls{display:flex;flex-wrap:wrap;gap:10px 18px}
.reader-controls label{display:grid;gap:4px;flex:1 1 230px;font-weight:650}
.reader-controls input,.reader-controls select{width:100%;padding:8px;border:1px solid #9eb5b9;
  background:#fff;color:var(--ink);border-radius:6px;font:inherit}
.text-results{padding-left:20px;margin-top:6px}
.text-results li{margin-bottom:6px}
.text-results span{display:block;color:var(--muted)}
.reading-section{padding:18px 0;border-top:1px solid var(--line)}
.reading-copy{max-width:70ch;font:17px/1.65 Georgia,serif}
.reading-copy pre{font:inherit;white-space:pre-wrap;margin:0 0 12px}
.reading-copy p:target,.reading-copy pre:target{background:#e3f3ee}
.reading-copy :is(p,pre){scroll-margin-top:12px}
"""

SELF_CHECK = (
    "Make a clear argument that answers the question.",
    "Use a precise reference from the extract and another from elsewhere in the text.",
    "Explain how the writer’s language, form or structure shapes the reader’s or audience’s response.",
    "Use context where it helps explain your interpretation.",
)


def external(label, url):
    return f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(label)} ↗</a>'


def page(filename, title, subtitle, navigation, body, script=""):
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
</div>{chr(10) + script if script else ""}
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
    prompt, scene, ao1, ao2, ao3 = PRACTICE[text]["2018" if year == "specimen-2022" else year]
    assessment = [("Your interpretation", ao1), ("Writer’s choices", ao2), ("Context and ideas", ao3)]
    if is_play:
        assessment.append(("Expression", "Read one sentence aloud. Where might a different word, a shorter sentence or clearer punctuation make your meaning easier to follow?"))
    notes = "".join(f"<li><strong>{ao}</strong> · {escape(note)}</li>" for ao, note in assessment)
    passage = "Walton’s continuation" if not is_play and year in {"2018", "specimen-2022"} else location
    anchor = escape(reading_anchor(passage))
    reader = f"{text}-text.html"
    return f"""<details class="question" id="exam-{year}">
      <summary>{escape(series)} · {escape(title)}</summary>
      <div class="question-layout">
        <div>
          <p>{escape(location)} · {component}, Question {number} · {"34" if is_play else "30"} marks</p>
          <div class="practice"><strong>Practice task</strong><br>{escape(prompt)}</div>
          <p>{escape(scene)} Use this passage and evidence from elsewhere in the work.</p>
          <details class="marking-notes">
            <summary>Thinking prompts</summary>
            <p>These questions draw on what AQA rewards. Start with the one that helps you notice something in the text.</p>
            <ul>{notes}</ul>
          </details>
        </div>
        <details class="question-reader">
          <summary>Read {escape(passage)} in the text pane</summary>
          <iframe title="{escape(TEXTS[text]['title'])} full text" loading="lazy"
                  data-src="{reader}?pane=1#{anchor}"></iframe>
          <noscript><p><a href="{reader}#{anchor}" target="_blank" rel="noopener">Open the full text in a new tab</a></p></noscript>
        </details>
      </div>
      <div class="actions references">
        {external("Original question paper", paper)}
        {external("Official mark scheme", scheme)}
      </div>
    </details>"""


def build_reader(slug, text):
    sections = read_sections(ROOT / "texts" / f"{slug}.txt")
    options = "".join(f'<option value="{escape(anchor)}">{escape(title)}</option>'
                      for anchor, title, _ in sections)
    contents = []
    for anchor, title, content in sections:
        blocks = []
        for block in content.split("\n\n"):
            if not block.strip():
                continue
            if slug == "macbeth":
                blocks.append(f"<pre>{escape(block.strip())}</pre>")
            else:
                blocks.append(f"<p>{escape(' '.join(block.split()))}</p>")
        contents.append(f'<section class="reading-section" id="{escape(anchor)}">'
                        f'<h2>{escape(title)}</h2><div class="reading-copy">{"".join(blocks)}</div></section>')

    body = f"""
      <div class="panel reader-panel">
        <div class="reader-controls">
          <label>Find a word or phrase <input type="search" id="text-search"></label>
          <label>Jump to a section <select id="text-jump"><option value="">Choose a section</option>{options}</select></label>
        </div>
        <p id="text-search-status" role="status"></p>
        <ol class="text-results" id="text-results"></ol>
      </div>
      {"".join(contents)}
      <footer>Source · {external("Project Gutenberg", SOURCES[slug])}</footer>"""
    script = (ROOT / "reader.js").read_text(encoding="utf-8")
    page(f"{slug}-text.html", f'{text["title"]} · Full text', text["author"],
         (("All subjects", "./"), ("Back to revision", f"{slug}.html"),
          ("Exam questions", f"{slug}.html#questions")), body, f"<script>{script}</script>")


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
    questions = "".join(question_card(exam, slug) for exam in EXAMS)
    body = f"""
      <div class="actions">
        <a href="{slug}-text.html">Read and search the full text</a>
        {external("PMT revision notes", PMT_NOTES + slug + "/")}
        {external("BBC guided essay", text["guided"])}
      </div>
      <section id="questions"><h2>Past and specimen questions</h2><p>Open a question to read the passage alongside it or reveal thinking prompts. Tasks are reworded and the prompts draw on AQA’s marking criteria. The original AQA documents are linked on each card.</p><div class="questions">{questions}</div></section>
      <section id="plot"><h2>Plot at a glance</h2><ol class="plot">{plot}</ol></section>
      <section id="topics"><h2>Revise by topic</h2>{"".join(topics)}
        <details class="panel"><summary>Check your answer</summary><ul>{checklist}</ul></details>
      </section>
"""
    page(
        f"{slug}.html", text["title"], f'{text["author"]} · {text["section"]}',
        (("All subjects", "./"), ("English Literature", "english.html"), ("Exam questions", "#questions"),
         ("Plot", "#plot"), ("Topics", "#topics")), body,
        """<script>
function showLinkedQuestion() {
  const question = document.getElementById(location.hash.slice(1));
  if (question?.matches('details.question')) question.open = true;
}
addEventListener('hashchange', showLinkedQuestion);
showLinkedQuestion();

for (const pane of document.querySelectorAll('.question-reader')) {
  pane.addEventListener('toggle', () => {
    const reader = pane.querySelector('iframe');
    if (pane.open && !reader.hasAttribute('src')) reader.src = reader.dataset.src;
  });
}
</script>""",
    )


def build_english():
    for slug, text in TEXTS.items():
        build_text(slug, text)
        build_reader(slug, text)

    archive = []
    for exam in EXAMS:
        if exam[1] in {"2021", "2022", "specimen-2022"}:
            heading = f'{exam[0]} · papers split by text'
            cards = f"""<div class="actions">
              <a href="macbeth.html#exam-{exam[1]}">Macbeth · Paper 2, Q1</a>
              <a href="frankenstein.html#exam-{exam[1]}">Frankenstein · Paper 1N, Q5</a>
            </div>"""
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
        <h2>Past papers and specimens</h2>
        <p>For November 2021 and June 2022, use Paper 2 for Macbeth and Paper 1N for Frankenstein. The 2022 specimen reuses the June 2018 questions from both texts.</p>
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
