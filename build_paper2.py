"""Render the two selected AQA Paper 2 revision pages."""

import json
from html import escape

from build import ROOT
from english_data import PMT_NOTES
from english_paper2 import (
    ANTHOLOGY, INSPECTOR, INSPECTOR_ARGUMENTS, POEMS, POETRY, POETRY_ARGUMENTS,
    SERIES, SPEC, paper2_sources,
)

EXAM_QUESTIONS = json.loads((ROOT / "paper2_exam_questions.json").read_text(encoding="utf-8"))
PDF_PAGES = json.loads((ROOT / "paper2_pdf_pages.json").read_text(encoding="utf-8"))
POEM_TEXTS = json.loads((ROOT / "paper2_poems.json").read_text(encoding="utf-8"))

OPEN_LINKED_DETAILS = """<script>
function openLinkedDetails() {
  const target = document.getElementById(location.hash.slice(1));
  if (target instanceof HTMLDetailsElement) target.open = true;
}
addEventListener('hashchange', openLinkedDetails);
openLinkedDetails();
</script>"""


def exam_cards(render_body, poetry, external, question_markup):
    cards = []
    for year, series in SERIES:
        component, paper, mark_scheme = paper2_sources(year, poetry)
        subject = "poetry" if poetry else "inspector"
        qp_page, ms_page = PDF_PAGES[year][subject]
        title, body = render_body(year, component, question_markup)
        cards.append(f"""<details class="question" id="exam-{year}">
          <summary>{escape(series)} · {escape(title)}</summary>
{body.rstrip()}
          <div class="actions references">
            {external("Original question paper", f"{paper}#page={qp_page}")}
            {external("Official mark scheme", f"{mark_scheme}#page={ms_page}")}
          </div>
        </details>""")
    index = "".join(f'<li><a href="#exam-{year}">{escape(series)}</a></li>' for year, series in SERIES)
    return (f'<ul class="exam-index" aria-label="Jump to an exam series">{index}</ul>'
            f'<div class="questions">{"".join(cards)}</div>')


def thinking_prompt(prompt, argument):
    return f"""<details class="marking-notes">
      <summary>Thinking prompt and example argument</summary>
      <p>{escape(prompt)}</p>
      <p><strong>One possible argument</strong> · {escape(argument)}</p>
    </details>"""


def inspector_body(year, component, question_markup):
    questions = []
    marks = "[30 marks] · AO4 [4 marks]" if component == "2" else "[30 marks]"
    for number, ((topic, _, prompt), argument) in enumerate(
        zip(INSPECTOR[year], INSPECTOR_ARGUMENTS[year], strict=True), 1
    ):
        questions.append(f"""<section>
          <h3>Question {number:02d} · {escape(topic)}</h3>
          <div class="practice">{question_markup(EXAM_QUESTIONS[year]["inspector"][number - 1])}<p><strong>{marks}</strong></p></div>
          {thinking_prompt(prompt, argument)}
        </section>""")
    return " or ".join(question[0] for question in INSPECTOR[year]), (
        f"<p>8702/{component} · Choose one question</p>" + "".join(questions)
    )


def poetry_body(year, component, question_markup):
    named, focus, partner, prompt = POETRY[year]
    poem, other = POEMS[named][0], POEMS[partner][0]
    number = "25" if component == "2" else "01"
    return f"{poem} · {focus}", f"""
      <p>8702/{component} · Question {number}</p>
      <div class="practice">{question_markup(EXAM_QUESTIONS[year]["poetry"])}<p><strong>[30 marks]</strong></p></div>
      <div class="actions">
        <a href="#poem-{named}">Read {escape(poem)}</a>
        <a href="#poem-{partner}">Possible comparison · {escape(other)}</a>
      </div>
      {thinking_prompt(prompt, POETRY_ARGUMENTS[year])}"""


def build_paper2(page, external, question_markup):
    navigation = (("All subjects", "./"), ("English Literature", "english.html"))
    specification = external("AQA set texts and anthology", SPEC + "/subject-content/modern-texts-and-poetry")
    page("an-inspector-calls.html", "An Inspector Calls", "J. B. Priestley · AQA Paper 2, Section A",
         (*navigation, ("Exam questions", "#questions"), ("Acts", "#acts")), f"""
      <div class="actions">
        {external("Script and publisher preview", "https://www.concordtheatricals.co.uk/s/12689/an-inspector-calls")}
        {external("PMT revision notes", PMT_NOTES + "an-inspector-calls/")}
        {specification}
      </div>
      <section id="questions">
        <h2>Past and specimen questions</h2>
        <p>Choose one whole-play essay. The paper gives you two options without a printed extract.</p>
        {exam_cards(inspector_body, False, external, question_markup)}
      </section>
      <section id="acts">
        <h2>Read the play by act</h2>
        <ol class="plot">
          <li><strong>Act 1</strong> · The engagement dinner gives way to the Inspector’s inquiry. Birling and Sheila describe how their decisions affected Eva.</li>
          <li><strong>Act 2</strong> · Gerald explains his relationship with Daisy. Mrs Birling defends the charity’s decision, then learns who the father is.</li>
          <li><strong>Act 3</strong> · Eric describes his actions. After the Inspector leaves, the family argues over what his identity changes. A phone call reopens the inquiry.</li>
        </ol>
      </section>""", OPEN_LINKED_DETAILS)

    poem_cards = []
    for index, (title, author, pdf_page, note) in enumerate(POEMS):
        verse = f'<blockquote class="exam-extract"><pre>{escape(POEM_TEXTS[str(index)])}</pre></blockquote>'
        poem_cards.append(f"""<details class="topic-card" id="poem-{index}">
          <summary>{escape(title)} · {escape(author)}</summary>
          <p>{escape(note)}</p>
{verse}
          <div class="actions">{external("Read in the AQA anthology", f"{ANTHOLOGY}#page={pdf_page}")}</div>
        </details>""")
    poem_index = "".join(f'<li><a href="#poem-{i}">{escape(poem[0])}</a></li>' for i, poem in enumerate(POEMS))
    page("love-and-relationships.html", "Love and Relationships", "AQA Paper 2, Section B · Anthology poetry",
         (*navigation, ("Exam questions", "#questions"), ("All 15 poems", "#poems")), f"""
      <div class="actions">
        {external("AQA anthology", ANTHOLOGY)}
        {external("PMT poetry notes", PMT_NOTES + "love-and-relationships/")}
        {specification}
      </div>
      <section id="questions">
        <h2>Past and specimen questions</h2>
        <p>AQA prints one named poem. Compare it with another poem from this cluster, using what you remember.</p>
        {exam_cards(poetry_body, True, external, question_markup)}
      </section>
      <section id="poems">
        <h2>All 15 poems</h2>
        <p>Open a poem to read it in full and find a revision prompt.</p>
        <ul class="exam-index" aria-label="Jump to a poem">{poem_index}</ul>
        {"".join(poem_cards)}
      </section>""", OPEN_LINKED_DETAILS)
