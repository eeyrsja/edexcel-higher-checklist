"""Prepare public domain literary texts for the searchable readers."""

import re

ROMAN = (
    "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII "
    "XIX XX XXI XXII XXIII XXIV"
).split()

SOURCES = {
    "macbeth": "https://www.gutenberg.org/ebooks/1533",
    "frankenstein": "https://www.gutenberg.org/ebooks/42324",
}


def number(roman):
    return ROMAN.index(roman) + 1


def reading_anchor(location):
    return location.lower().replace(", ", "-").replace(" ", "-")


def read_sections(path):
    raw = path.read_text(encoding="utf-8-sig")
    body = raw.split("*** START OF THE PROJECT GUTENBERG EBOOK ", 1)[1]
    body = body.split("***", 1)[1].split("*** END OF THE PROJECT GUTENBERG EBOOK", 1)[0]
    if path.stem == "macbeth":
        pattern = r"^(?:ACT ([IVX]+)|SCENE ([IVX]+)\. .*|Dramatis Personæ) *$"
        # Start after the source table of contents.
        start = body.index("Dramatis Personæ")
    else:
        pattern = r"^(?:INTRODUCTION\.|LETTER ([IVX]+)\.|CHAPTER ([IVX]+)\.|WALTON, _in continuation_\.) *$"
        start = body.index("INTRODUCTION.")
    body = body[start:]
    matches = list(re.finditer(pattern, body, re.MULTILINE))
    act = 0
    sections = []
    for index, match in enumerate(matches):
        group1, group2 = match.groups()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[match.end():end].strip()
        if path.stem == "macbeth":
            if group1:
                act = number(group1)
                continue
            if group2:
                title = f"Act {act}, Scene {number(group2)}"
                content = match[0].split(". ", 1)[1] + "\n\n" + content
            else:
                title = "Characters"
        elif group1:
            title = f"Letter {number(group1)}"
        elif group2:
            title = f"Chapter {number(group2)}"
        else:
            title = "Walton’s continuation" if match[0].startswith("WALTON") else "Introduction"
        sections.append((reading_anchor(title), title, content))
    return sections
