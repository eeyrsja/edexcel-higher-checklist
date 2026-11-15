"""AQA 8702 modern drama and anthology poetry resources."""

from english_data import PMT

SPEC = "https://www.aqa.org.uk/subjects/english/gcse/english-8702/specification"
ANTHOLOGY = "https://filestore.aqa.org.uk/resources/english/AQA-8702-TG-POEMS.PDF"
SERIES = (
    ("2025", "June 2025"), ("2024", "June 2024"), ("2023", "June 2023"),
    ("2022", "June 2022"), ("2021", "November 2021"), ("2020", "November 2020"),
    ("2019", "June 2019"), ("2018", "June 2018"), ("2017", "June 2017"),
    ("specimen", "AQA specimen · set 1"), ("specimen-2022", "AQA specimen · 2022 format"),
)


def paper2_sources(year, poetry=False):
    split = year in {"2021", "2022", "specimen-2022"}
    component = ("1P" if poetry else "1M") if split else "2"
    folder = "Paper-1" if split else "Paper-2"
    if year == "specimen":
        prefix = "Specimen"
    elif year == "specimen-2022":
        prefix = "Specimen%20%282022%29"
    else:
        prefix = f"June%20{year}"
    suffix = f"%20-%20{component}" if split else ""
    urls = tuple(f"{PMT}/{folder}/{kind}/{prefix}%20{kind}{suffix}.pdf" for kind in ("QP", "MS"))
    return component, *urls

# Topic, original question summary, and an independent line of argument to test.
INSPECTOR = {
    "2025": (
        ("Gerald and Sheila", "How does their engagement change during the play?", "Compare the celebration and the returned ring with Gerald offering it again. Is the ending a reconciliation, or do the two now want different things?"),
        ("Power", "How does Priestley show who has power and how it is used?", "Consider how employers, customers and charity committees exercise different kinds of power. What changes when the Inspector takes control of the room?"),
    ),
    "2024": (
        ("Mrs Birling and class", "What does Mrs Birling reveal about social class?", "Compare how she judges Eva’s use of the Birling name with how she responds to Eric. Is class a principle for her, or a means of protecting her position?"),
        ("The Inspector and social change", "How does the Inspector make the case for a different society?", "Compare his questioning of individuals with his final address. What can the audience take from the final phone call even if his identity remains uncertain?"),
    ),
    "2023": (
        ("Women’s lives", "What does the play suggest about the positions and choices available to women?", "Compare Eva’s limited choices with Sheila’s growing independence. Where does class make a greater difference than gender alone can explain?"),
        ("Generational responses", "How do older and younger characters respond differently to the Inspector?", "Compare the family’s reactions after the Inspector leaves. Does Gerald fit neatly into either group, and what does that do to your argument?"),
    ),
    "2022": (
        ("Eric and society", "What does Eric learn about society during the evening?", "Look at how Eric talks about money, his parents and Eva after the revelations. Which change shows a broader understanding, and which might be personal remorse?"),
        ("Inequality and tragedy", "To what extent does inequality cause the tragedy?", "Follow Eva from employment to the charity committee. Which losses of choice come from social position, and where do individual decisions still matter?"),
    ),
    "2021": (
        ("Gerald and responsibility", "What does Gerald’s behaviour reveal about responsibility?", "Compare his account of helping Daisy with his later efforts to establish the Inspector’s identity. Is accepting responsibility the same as admitting what happened?"),
        ("An unfair society", "How far does Priestley depict a society organised unfairly?", "Set the opening celebration against Eva’s situation. Who gets to decide whether she deserves work, shelter or help, and how is that inequality staged?"),
    ),
    "2020": (
        ("Mr Birling and self-interest", "How far is Birling concerned only with his own interests and his family’s?", "Compare Birling’s advice at dinner with what he wants to protect after the inquiry. Is he defending his family, his reputation, or both?"),
        ("Irresponsible men", "How far are the men in the play shown to evade responsibility?", "Compare Birling, Gerald and Eric. Where do they use their position to avoid consequences, and which of them is willing to live with what he has learned?"),
    ),
    "2019": (
        ("Selfishness and its effects", "What are the consequences of selfish choices in the play?", "Trace two different choices about Eva. How does the order in which Priestley reveals them turn private decisions into a pattern?"),
        ("Sheila’s lessons", "What does Sheila learn about herself and society?", "Compare Sheila’s response to losing her temper at the shop with her later warnings to the family. How does her role in the dialogue change?"),
    ),
    "2018": (
        ("Eric’s change", "How far do Eric’s attitudes to himself and others change?", "Compare his evasiveness at dinner with his willingness to face responsibility at the end. What can a change in attitude repair, and what can it never undo?"),
        ("Social class", "Why does social class matter in the play?", "Who can order, dismiss or refuse someone, and who cannot answer back? Consider why Priestley places those decisions in a comfortable dining room."),
    ),
    "2017": (
        ("Mrs Birling", "How far does Priestley make Mrs Birling unlikeable?", "Compare her confidence at the charity committee with the revelation that follows her judgement of the father. Can you explain her certainty without endorsing it?"),
        ("The Inspector’s proposals", "What changes to society does the Inspector encourage?", "Look at his questioning and final speech. How does the contrast with Birling’s opening advice invite the audience to choose between two ways of living?"),
    ),
    "specimen": (
        ("Sheila’s development", "What changes Sheila, and how does Priestley show the change?", "Compare Sheila’s words at the engagement, during the inquiry and after it. How does she move from being questioned to questioning her family?"),
        ("Responsibility", "How does the play explore responsibility for other people?", "Consider why the family’s relief before the final phone call matters. What changes if responsibility depends on proof rather than on what they did?"),
    ),
}
INSPECTOR["specimen-2022"] = INSPECTOR["2018"]

# Named poem index, comparison focus, suggested partner index, and a comparison to test.
POETRY = {
    "2025": (9, "feelings about growing up", 7, "Both poets look back at childhood from adulthood. How do the reversal at the end of Follower and the parent’s final reflection in Walking Away make growing up feel different?"),
    "2024": (4, "powerful feelings about love", 3, "Hardy’s bleak memory makes love feel injurious; Barrett Browning’s expanding vines make it feel consuming. How do the endings complicate the idea that powerful love is always desirable?"),
    "2023": (11, "relationships between parents and children", 9, "Duffy imagines a parent’s life before the child, while Heaney looks up to a parent and later reverses their roles. What does each time shift change about the speaker’s view?"),
    "2022": (3, "the power of love", 12, "One speaker longs to replace thoughts with presence; the other finds closeness after silence. Where do natural images show love changing what the speakers do?"),
    "2021": (6, "strong feelings in romantic relationships", 2, "Both poems give a man the speaking voice while a woman’s experience is mediated through it. How does each poet give the reader reason to question what the man calls love?"),
    "2020": (7, "family relationships", 10, "Both poems link love to letting go. How do the orbit image in Walking Away and the measuring tape in Mother, any distance give separation a different emotional shape?"),
    "2019": (12, "romantic feelings", 4, "A shared landscape reflects distance in both poems. How does the movement towards contact in Winter Swans differ from the way Hardy returns to the landscape in memory?"),
    "2018": (13, "romantic love", 3, "The shopkeeper values private time over business, while the sonnet speaker values presence over imagination. How does each voice make the beloved seem more valuable than the alternative?"),
    "2017": (10, "growing up", 7, "Both poets use images of distance. What difference does it make that Armitage writes from the child’s viewpoint while Day Lewis writes from the parent’s?"),
    "specimen": (9, "attitudes towards a parent", 11, "Heaney remembers trying to follow a skilled father; Duffy imagines looking back at a mother’s lost freedom. Where does admiration sit alongside guilt or discomfort in each poem?"),
}
POETRY["specimen-2022"] = POETRY["2018"]

# PDF page numbers count the cover. These are the 15 poems in AQA's cluster.
POEMS = (
    ("When We Two Parted", "Lord Byron", 3, "Secrecy, betrayal and grief. Notice how the ending returns to the silence and tears of the opening."),
    ("Love’s Philosophy", "Percy Bysshe Shelley", 4, "Desire and persuasion. Do the natural pairings make the speaker’s argument convincing, or show how much he wants it to be?"),
    ("Porphyria’s Lover", "Robert Browning", 5, "Possession and control. What should you question about the speaker’s account of Porphyria’s feelings?"),
    ("Sonnet 29 – ‘I think of thee!’", "Elizabeth Barrett Browning", 7, "Desire and presence. Track what happens when the speaker imagines thoughts as vines and asks for the real person instead."),
    ("Neutral Tones", "Thomas Hardy", 8, "Disillusionment and memory. How does the winter setting change when it returns at the end?"),
    ("Letters from Yorkshire", "Maura Dooley", 9, "Distance and connection. How do the two kinds of work in the poem help you understand what the letters bridge?"),
    ("The Farmer’s Bride", "Charlotte Mew", 10, "Fear, desire and unequal power. What does the farmer’s account reveal that he himself may fail to see?"),
    ("Walking Away", "Cecil Day Lewis", 12, "Parenthood and separation. Why does the child’s movement away come back to the parent so many years later?"),
    ("Eden Rock", "Charles Causley", 13, "Family, memory and loss. What do the ordinary picnic details do to the uncertainty of the final crossing?"),
    ("Follower", "Seamus Heaney", 14, "Admiration and changing dependence. Who follows whom at the beginning and the end?"),
    ("Mother, any distance", "Simon Armitage", 15, "Attachment and independence. Could the measuring tape represent freedom as well as restraint?"),
    ("Before You Were Mine", "Carol Ann Duffy", 16, "Memory and a parent’s independence. How does the daughter’s imagined version of her mother’s past complicate the title?"),
    ("Winter Swans", "Owen Sheers", 17, "Conflict and reconciliation. Where does the movement of the swans start to change the way the couple move?"),
    ("Singh Song!", "Daljit Nagra", 18, "Romantic love and private identity. What does the contrast between the shop and the couple’s private world say about what they value?"),
    ("Climbing My Grandfather", "Andrew Waterhouse", 20, "Family attachment and discovery. Why might the extended climbing image make the speaker’s closeness feel earned?"),
)

INSPECTOR_ARGUMENTS = {
    "2025": ("The engagement begins as reassurance of social and family stability, but Sheila’s refusal to settle the question at the end shows how differently the two understand what has happened.",
             "Priestley makes institutional power visible through Eva’s limited options, then shifts the power onstage to a visitor who controls what the family can see and when."),
    "2024": ("Mrs Birling’s authority rests on social distinction, but the revelation about Eric exposes the limits of the moral judgements she makes on that basis.",
             "The Inspector turns an apparently private investigation into a public argument about responsibility, and the final call keeps that argument alive after he leaves."),
    "2023": ("Priestley shows that women’s choices are constrained by both class and gender: Sheila can come to recognise injustice, while Eva’s efforts to resist have material consequences.",
             "Sheila and Eric accept moral responsibility independently of the Inspector’s official status, while their parents are more willing to treat the absence of proof as absolution."),
    "2022": ("Eric begins to see why having money and status gives him obligations, although his new awareness arrives too late to help Eva.",
             "The play treats inequality as a system that makes Eva vulnerable to repeated setbacks, while showing the choices through which individuals sustain that system."),
    "2021": ("Gerald shows that taking practical action for somebody can coexist with using power over them, and that telling the truth can fall short of accepting lasting responsibility.",
             "Eva is repeatedly judged by people insulated from the consequences of their own decisions, making unfairness visible in everyday institutions."),
    "2020": ("Birling’s desire to protect his family frequently overlaps with his desire to preserve his standing; when those interests conflict, the play tests how generous his concern really is.",
             "The men use position, money and reputation to avoid accountability in different ways, but Eric’s response at the end makes the group less uniform."),
    "2019": ("Each selfish act can look small when explained in isolation, but the sequence of disclosures shows how the acts accumulate into harm.",
             "Sheila learns to connect her private behaviour with its social consequences, and her increasing confidence in challenging the family makes that lesson visible onstage."),
    "2018": ("Eric moves from discomfort and evasion towards accepting his part in what happened, although the play leaves the practical value of that change open.",
             "Social class determines who can exercise judgement and who has to endure its effects, and Priestley’s dining-room setting keeps that imbalance in view."),
    "2017": ("Mrs Birling’s unexamined certainty can repel an audience, especially when her judgement rebounds on her own family.",
             "The Inspector argues for social improvement by replacing Birling’s ethic of individual self-interest with the idea that choices impose obligations to others."),
    "specimen": ("The investigation changes Sheila from a participant in an engagement celebration into someone who can interrogate the assumptions supporting that celebration.",
                 "The ending tests whether responsibility depends on the authority of the person asking the questions, or on the actions already admitted."),
}
INSPECTOR_ARGUMENTS["specimen-2022"] = INSPECTOR_ARGUMENTS["2018"]

POETRY_ARGUMENTS = {
    "2025": "Both poets treat growing up as a shift in dependence. Heaney’s ending reverses who follows whom, while Day Lewis measures parental love by the willingness to let a child leave.",
    "2024": "Both poems make love difficult to escape. Hardy’s circular return to the pond suggests lasting injury, while Barrett Browning’s sonnet turns obsessive thought into a demand for closeness.",
    "2023": "Both poems reshape a parent through memory. Duffy imagines the freedom her mother had before parenthood, while Heaney uses a reversal to reconsider his own dependence.",
    "2022": "Both poets show love changing what the lovers do. Barrett Browning’s speaker asks for contact outright, while Sheers lets the change emerge through movement and touch.",
    "2021": "Both poems let a male speaker talk about love while exposing a woman’s vulnerability. Mew leaves fear visible through the farmer’s account, while Browning’s speaker insists on an interpretation the reader has reason to doubt.",
    "2020": "Both poems join affection with separation. The father in Walking Away accepts that love requires letting go, while the child in Mother, any distance ends poised between support and independence.",
    "2019": "Both poets give a landscape emotional force. Sheers lets the walk open a route back to intimacy, while Hardy makes a past scene return as evidence of disillusionment.",
    "2018": "Both poems place the beloved above an alternative measure of value. Nagra uses the shop’s language of price, while Barrett Browning distinguishes the lover’s presence from the speaker’s thoughts.",
    "2017": "Both poems measure growing up through physical distance. Armitage emphasises the child’s uncertainty at the threshold, while Day Lewis looks back at a separation the parent has learned to interpret.",
    "specimen": "Heaney and Duffy both admire a parent while reconsidering what the child’s presence means, but Heaney stages a reversal in dependence while Duffy imagines a life the child never witnessed.",
}
POETRY_ARGUMENTS["specimen-2022"] = POETRY_ARGUMENTS["2018"]
