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


def reading_blocks(slug, content):
    blocks = [block.strip() for block in re.split(r"\n\s*\n", content) if block.strip()]
    return blocks if slug == "macbeth" else [" ".join(block.split()) for block in blocks]


def locate_extract(blocks, extract):
    """Map the exam edition onto matching word positions in the reader edition."""
    from difflib import SequenceMatcher

    def tokens(value):
        return list(re.finditer(r"[^\W_]+", value.lower().replace("’", "'")))

    words = []
    positions = []
    for index, block in enumerate(blocks):
        for token in tokens(block):
            words.append(token[0])
            positions.append((index, token.start(), token.end()))
    exam = [token[0] for token in tokens(extract)]
    matches = SequenceMatcher(None, exam, words, autojunk=False).get_matching_blocks()
    substantial = [match for match in matches if match.size >= 3]
    matched = sum(match.size for match in matches)
    if not substantial or matched < len(exam) * 0.85:
        raise ValueError(f"Only {matched}/{len(exam)} extract words matched")
    first, last = substantial[0], substantial[-1]
    # Keep isolated matching words near the endpoints, but ignore stray matches
    # elsewhere in the chapter or scene.
    for match in matches:
        if match.b < first.b and first.b - match.b <= first.a - match.a + 3:
            first = match
    for match in reversed(matches[:-1]):
        if match.b > last.b and match.b - last.b <= match.a - last.a + 3:
            last = match
    i, start, _ = positions[first.b]
    j, _, end = positions[last.b + last.size - 1]
    return [[index, start if index == i else 0, end if index == j else len(blocks[index])]
            for index in range(i, j + 1)]
