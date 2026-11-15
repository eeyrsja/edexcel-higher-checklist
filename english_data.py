"""AQA 8702 question references and original revision material."""

AQA = "https://www.aqa.org.uk"
PMT = "https://pmt.physicsandmathstutor.com/download/English-Literature/GCSE/Past-Papers/AQA"
PMT_NOTES = "https://www.physicsandmathstutor.com/english-revision/gcse-aqa/"

# Each pair carries an exam topic and the location of the printed extract.
EXAMS = (
    ("June 2025", "2025", ("Macbeth’s ambition", "Act 1, Scene 7"), ("The importance of family", "Chapter 1")),
    ("June 2024", "2024", ("Lady Macbeth’s strength", "Act 1, Scene 7"), ("The effects of scientific ambition", "Chapter 4")),
    ("June 2023", "2023", ("How Macbeth changes", "Act 5, Scene 3"), ("Loneliness and isolation", "Chapter 17")),
    ("June 2022", "2022", ("Macbeth’s fears", "Act 3, Scene 1"), ("Victor’s relationship with the creature", "Chapter 10")),
    ("November 2021", "2021", ("Macbeth and Lady Macbeth’s relationship", "Act 2, Scene 2"), ("Victor as a victim of his own actions", "Letter 4")),
    ("November 2020", "2020", ("How Lady Macbeth changes", "Act 5, Scene 1"), ("Grief and loss", "Chapter 23")),
    ("June 2019", "2019", ("Macbeth as a violent character", "Act 1, Scene 2"), ("How others’ treatment affects the creature", "Chapter 15")),
    ("June 2018", "2018", ("Attitudes to the supernatural", "Act 1, Scene 3"), ("The creature as a victim deserving pity", "Chapter 24")),
    ("June 2017", "2017", ("Ambition", "Act 1, Scene 5"), ("Whether the creature is evil", "Chapter 20")),
    ("AQA specimen", "specimen", ("Lady Macbeth’s power", "Act 1, Scene 5"), ("Love and acceptance", "Chapter 15")),
)

TEXTS = {
    "macbeth": {
        "title": "Macbeth", "author": "William Shakespeare", "section": "Section A · 34 marks",
        "reading": "https://www.folger.edu/explore/shakespeares-works/macbeth/read/",
        "guided": "https://www.bbc.co.uk/bitesize/guides/zwgdnbk/revision/1",
        "plot": (
            ("Act 1", "The witches predict Macbeth’s rise. Duncan names Malcolm heir. Lady Macbeth persuades Macbeth to go through with the murder."),
            ("Act 2", "Macbeth kills Duncan and is shaken by what he has done. Duncan’s sons flee and Macbeth becomes king."),
            ("Act 3", "Macbeth arranges Banquo’s murder. Fleance escapes. Banquo’s ghost disrupts the banquet."),
            ("Act 4", "The apparitions give Macbeth confidence. He orders the killing of Macduff’s family while Macduff joins Malcolm."),
            ("Act 5", "Lady Macbeth sleepwalks and dies. Malcolm’s army advances using branches from Birnam Wood. Macduff kills Macbeth."),
        ),
        "topics": (
            ("Ambition and kingship", "Compare Macbeth weighing up Duncan’s murder (1.7) with his fear of Banquo (3.1). His soliloquies show how getting the crown changes what he wants from power.", "How does Shakespeare present ambition as a threat to good kingship?", ("2017", "2025", "2022")),
            ("Lady Macbeth and gender", "Compare Lady Macbeth’s appeal to the spirits (1.5), her challenge to Macbeth (1.7) and her fragmented speech while sleepwalking (5.1). Track who controls each scene.", "How does Shakespeare present changes in Lady Macbeth’s power?", ("specimen", "2024", "2020", "2021")),
            ("Guilt and fear", "Compare Macbeth’s reaction to his bloody hands (2.2) with Lady Macbeth’s imagined bloodstain (5.1). Explain what the recurring image reveals at each point.", "How does Shakespeare use images of blood to show the effects of guilt?", ("2022", "2020", "2021")),
            ("The supernatural", "Compare Banquo’s caution about the witches (1.3) with Macbeth’s confidence after the apparitions (4.1). Consider how the audience hears a warning where Macbeth hears reassurance.", "How does Shakespeare use the supernatural to test characters’ judgement?", ("2018",)),
            ("Violence and Macbeth’s change", "Compare the Captain praising Macbeth’s fighting (1.2) with Macbeth ordering the deaths of Macduff’s family (4.1). Ask what makes violence seem admirable in one scene and tyrannical in the other.", "How does Shakespeare change the audience’s view of Macbeth’s violence?", ("2019", "2023")),
        ),
    },
    "frankenstein": {
        "title": "Frankenstein", "author": "Mary Shelley · 1831 edition", "section": "Section B · 30 marks",
        "reading": "https://www.gutenberg.org/ebooks/42324",
        "guided": "https://www.bbc.co.uk/bitesize/guides/zxpydmn/revision/1",
        "plot": (
            ("Walton’s letters", "An explorer writes to his sister about his Arctic expedition and his encounter with Victor. The letters frame the novel."),
            ("Chapters 1–5", "Victor describes his family and education, then secretly creates a living being and recoils from it."),
            ("Chapters 6–10", "Victor returns home after William’s death. Justine is executed, and the creature confronts Victor in the mountains."),
            ("Chapters 11–16", "The creature describes learning from the De Laceys, being rejected and turning towards revenge."),
            ("Chapters 17–20", "The creature asks for a companion. Victor starts making one, then destroys it."),
            ("Chapters 21–24", "Victor loses Clerval, Elizabeth and his father. His pursuit of the creature takes him to the Arctic, where Walton resumes the story."),
        ),
        "topics": (
            ("Science, ambition and responsibility", "Compare Victor imagining a new species (ch. 4) with his flight from the creature (ch. 5) and Walton’s decision to turn back (ch. 24). Notice how Victor narrates his hopes after knowing the outcome.", "How does Shelley show the difference between discovery and responsibility?", ("2024", "2021")),
            ("Isolation and belonging", "Compare the creature’s effort to approach the De Laceys (ch. 15) with his demand for a companion (ch. 17). Use his own narration to examine how Shelley builds sympathy.", "How does Shelley present isolation as a force that changes people?", ("2023", "2019", "specimen")),
            ("Family and loss", "Compare Victor’s account of family life (ch. 1) with his grief after Elizabeth’s death (ch. 23). Consider how affection also makes characters vulnerable.", "How does Shelley show the importance of family through what characters lose?", ("2025", "2020")),
            ("The creature, prejudice and revenge", "Compare the creature seeking kindness from the blind De Lacey (ch. 15) with his final account of his actions (ch. 24). Look at the tension between sympathy and responsibility.", "How does Shelley make the reader question who deserves sympathy?", ("2019", "2018", "2017")),
            ("Victor and the creature", "Compare their confrontation in the mountains (ch. 10) with Victor destroying the companion (ch. 20). Track how each character justifies what he owes to the other.", "How does Shelley present Victor and the creature as both enemies and alike?", ("2022", "2017", "2021")),
        ),
    },
}


def paper_links(year, text):
    """Return the question and mark scheme for the text's actual component."""
    if year == "specimen":
        return "8702/1", f"{PMT}/Paper-1/QP/Specimen%20QP.pdf", "https://filestore.aqa.org.uk/resources/english/AQA-87021-SMS.PDF"
    if year == "2024":
        url = f"{AQA}/files/sample-papers-and-mark-schemes.2024.June.AQA-87021"
        return "8702/1", f"{url}-QP-JUN24_PDF", f"{url}-MS-JUN24_PDF"
    if year == "2023":
        url = "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-87021"
        return "8702/1", f"{url}-QP-JUN23.PDF", f"{url}-MS-JUN23.PDF"
    split = year in {"2021", "2022"}
    paper = "2" if split and text == "macbeth" else "1"
    novel = split and text == "frankenstein"
    suffix = "%20-%201N" if novel else ""
    component = "8702/1N" if novel else f"8702/{paper}"
    base = f"{PMT}/Paper-{paper}"
    return component, f"{base}/QP/June%20{year}%20QP{suffix}.pdf", f"{base}/MS/June%20{year}%20MS{suffix}.pdf"
