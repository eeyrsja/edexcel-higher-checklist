#!/usr/bin/env python3
"""Build the Edexcel Higher revision checklist for GitHub Pages."""

import csv
import json
import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
CSV_PATH = ROOT / "CorbettMaths_Index.csv"
DESC_FILE = ROOT / "topic_descriptions.json"
CORBETT_SEARCH = "https://corbettmaths.com/?s="

SECTIONS = {
    'Number': [
        ('Adding Fractions', ['133']),
        ('One Quantity as a Fraction of Another', ['136']),
        ('Multiplying Fractions', ['142']),
        ('Dividing Fractions', ['134']),
        ('Reciprocal', ['145']),
        ('Ordering Fractions, Decimals & Percentages', ['131']),
        ('Decimals', ['90', '91', '92', '93', '94']),
        ('Use of a Calculator', ['352']),
        ('Estimation', ['215']),
        ('Best Buys', ['210']),
        ('Currency', ['214a']),
        ('Conversion Graphs', ['151', '152']),
        ('LCM / HCF', ['218', '219']),
        ('Product of Primes', ['223', '224']),
        ('Indices', ['172', '174']),
        ('Indices (fractional/negative)', ['173', '175']),
        ('Standard Form', ['300', '301', '302', '303']),
        ('Percentages of Amounts', ['234', '235', '238']),
        ('Percentage Change', ['233']),
        ('Simple Interest', ['236a']),
        ('Compound Interest', ['236']),
        ('Reverse Percentages', ['240']),
        ('Recurring Decimals to Fractions', ['96']),
        ('Ratio', ['270', '271', '271a', '271b', '271c']),
        ('Direct Proportion', ['254']),
        ('Inverse Proportion', ['255'], None, 'proportion: direct|proportion direct|direct & inverse'),
        ('Proportional Graphs', ['255b']),
        ('Proportion (application)', ['255c']),
        ('Limits of Accuracy', ['183', '184']),
        ('Surds', ['305', '306', '307', '308']),
        ('Product Rule for Counting', ['383']),
        ('Error Intervals', ['377', '280']),
    ],
    'Algebra': [
        ('Algebraic Notation', ['19']),
        ('Algebra Vocabulary', ['367a']),
        ('Collecting Like Terms', ['9']),
        ('Expanding Brackets', ['13', '14', '15']),
        ('Factorising', ['117']),
        ('Factorising Quadratics', ['118', '119', '120', '119a']),
        ('Algebraic Fractions', ['21', '22', '23', '24']),
        ('Sequences (nth term)', ['288', '289']),
        ('Diagram Sequences', ['290']),
        ('nth term (quadratics)', ['388a']),
        ('Substitution', ['20']),
        ('Equations', ['110', '113', '114', '115']),
        ('Changing the Subject', ['7', '8']),
        ('Inequalities', ['177', '178', '179']),
        ('Inequalities (Regions)', ['182']),
        ('Quadratic Inequalities', ['378']),
        ('Coordinates in Four Quadrants', ['84']),
        ('Linear Graphs', ['191', '186', '189', '194']),
        ('Midpoint of a Line', ['87']),
        ('Distance between 2 Points', ['185']),
        ('Real-life Linear Graphs', ['171a']),
        ('Parallel or Perpendicular Lines', ['198', '231']),
        ('Simultaneous Equations', ['295']),
        ('Non-linear Simultaneous Equations', ['298']),
        ('Graphical Simultaneous Equations', ['297']),
    ],
    'Geometry & Measures': [
        ('Geometry Notation & Diagrams', ['397', '28']),
        ('Properties of Triangles & Quadrilaterals', ['327', '2']),
        ('Angles in Parallel Lines', ['25', '39']),
        ('Scale Drawings & Maps', ['283']),
        ('Bearings', ['26', '27']),
        ('Angles in Polygons', ['32']),
        ('Constructions', ['78', '72', '79', '80', '70']),
        ('Loci', ['75', '76', '77']),
        ('Properties of 3D Shapes', ['3', '5']),
        ('Views (elevations)', ['354']),
        ('Area of a Trapezium', ['48']),
        ('Parts of a Circle', ['61']),
        ('Circumference', ['60']),
        ('Area of a Circle', ['40']),
        ('Arc Length', ['58']),
        ('Area of a Sector', ['46']),
        ('Area of Compound Shapes', []),
        ('Volume of a Cylinder', ['357']),
        ('Pythagoras', ['257', '259']),
        ('Trigonometry', ['329', '330', '331']),
        ('3D Trig and Pythagoras', ['259', '332']),
        ('Exact Trig Values', ['341']),
        ('Volume of a Prism', ['356']),
        ('Volume of Cone / Pyramid / Sphere', ['359-361']),
        ('Volume of a Frustum', ['360a']),
        ('Surface Area of a Prism', ['311']),
        ('Surface Area of Cone / Sphere', ['314', '313']),
        ('Metric Units (area/volume)', ['350', '351']),
        ('Translations', ['325']),
        ('Reflections', ['272']),
        ('Rotations', ['275']),
        ('Enlargements', ['104', '106', '107', '108']),
        ('Similar Shapes', ['292', '293a', '293b']),
        ('Circle Theorems', ['64', '65']),
        ('Sine Rule', ['333']),
        ('Cosine Rule', ['335', '336']),
        ('1/2abSinC (area of a triangle)', ['337']),
        ('Vectors', ['353']),
        ('Column Vectors', ['353a']),
        ('Travel Graphs', ['171', '173'], 'distance|timetable|velocity|travel|speed'),
        ('Speed, Distance, Time', ['299']),
        ('Density', ['384']),
        ('Pressure', ['385']),
        ('Geometric Proof', ['366']),
        ('Congruent Triangles', ['67']),
        ('Invariant Points', ['392']),
    ],
    'Probability & Statistics': [
        ('Frequency Trees', ['376']),
        ('Two-way Tables', ['319']),
        ('Pie Charts', ['163', '164'], 'pie|chart'),
        ('Scatter Graphs', ['165', '166'], 'scatter'),
        ('Histograms', ['157', '158', '159']),
        ('Frequency Polygons', ['155', '156']),
        ('Stem-and-Leaf', ['169', '170']),
        ('Cumulative Frequency', ['153', '154']),
        ('Box Plots', ['149']),
        ('Averages & Range', ['50']),
        ('Quartiles', ['57a', '57b']),
        ('Estimated Mean', ['55']),
        ('Combined Mean', ['53a']),
        ('Median (frequency table)', ['51', '52']),
        ('Modal Class (frequency table)', ['56a']),
        ('Probability', ['250']),
        ('Relative Frequency', ['248', '250']),
        ('Samples', ['281a']),
        ('Using Statistics to Describe a Population', ['57c']),
        ('Capture-Recapture', ['391']),
        ('Tree Diagrams', ['252']),
        ('Conditional Probability', ['247', '249']),
        ('Venn Diagrams', ['380']),
    ],
    'Higher Algebra & Functions': [
        ('Equation of a Circle', ['12']),
        ('Equation of a Tangent', ['372']),
        ('Instantaneous Rates of Change', ['390a']),
        ('Average Rates of Change', ['390b']),
        ('Area under a Curve', ['389']),
        ('Function Notation', []),
        ('Composite Functions', ['370']),
        ('Inverse Functions', ['369']),
        ('Quadratic Graphs', ['264']),
        ('Solving Quadratics Graphically', ['267c', '267d']),
        ('Sketching Quadratics', ['265', '265a']),
        ('Trigonometric Graphs', ['338', '339']),
        ('Cubic Graphs', ['344']),
        ('Reciprocal Graphs', ['346']),
        ('Exponential Graphs', ['345']),
        ('Geometric Sequences', ['375']),
        ('Algebraic Proof', ['365']),
        ('Quadratic Formula', ['267']),
        ('Completing the Square', ['10', '371']),
        ('Transformations of Graphs', ['323', '324']),
        ('Iteration', ['373', '373a', '373b']),
    ],
}


CHECKLIST_URL = 'https://corbettmaths.com/wp-content/uploads/2021/12/Edexcel-Higher-Checklist.pdf'

SPEC_PDF_URL = ("https://qualifications.pearson.com/content/dam/pdf/GCSE/mathematics/"
                "2015/specification-and-sample-assesment/gcse-maths-2015-specification.pdf")

SECTION_CLASS = {
    "Number": "s-num",
    "Algebra": "s-alg",
    "Geometry & Measures": "s-geo",
    "Probability & Statistics": "s-stat",
    "Higher Algebra & Functions": "s-halg",
}

RESOURCE_TYPES = {
    "Practice Questions": ("Questions", "q", "CorbettMaths"),
    "Textbook Exercise": ("Exercises", "t", "CorbettMaths"),
    "Answers": ("Answers", "a", "CorbettMaths"),
    "1CM Paper": ("Questions", "q", "1st Class Maths"),
    "1CM Solutions": ("Answers", "a", "1st Class Maths"),
}


# Topics whose worksheets do not exist on corbettmaths (video only)
VIDEO_ONLY = {
    "Geometric Proof": "https://corbettmaths.com/2019/12/31/geometric-proof-video/",
}


def spec_key(sid):
    m = re.match(r"^([A-Z])(\d+)$", sid)
    return (m.group(1), int(m.group(2))) if m else (sid, 0)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def esc(s: str) -> str:
    # escape for attributes; leave & alone so existing entities pass through
    return str(s).replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def expand_videos(tokens):
    out = []
    for tok in tokens:
        m = re.match(r"^(\d+)-(\d+)$", tok)
        if m:
            out += [str(n) for n in range(int(m.group(1)), int(m.group(2)) + 1)]
        else:
            out.append(tok)
    return out


def build_link_pills(files):
    """Group resource links by provider and label variations of each resource."""
    by_category = {}
    for file in files:
        by_category.setdefault(file["category"], []).append(file)

    by_provider = {"CorbettMaths": [], "1st Class Maths": []}
    for category, matches in by_category.items():
        label, css_class, provider = RESOURCE_TYPES[category]
        titles = [file["topic"] for file in matches]
        prefix = os.path.commonprefix(titles)
        for file in sorted(matches, key=lambda f: (len(f["topic"]), f["file"])):
            title = file["topic"]
            rest = title[len(prefix):]
            splits_word = prefix and prefix[-1].isalnum() and rest and rest[0].isalnum()
            suffix = (title if splits_word else rest).strip(" :;-–()")
            text = label if not suffix else f'{label}<span class="sfx">&thinsp;·&thinsp;{esc(suffix)}</span>'
            href = esc(file["source_url"])
            pill = (f'<a class="pill {css_class}" href="{href}" target="_blank" rel="noopener"'
                    f' title="{esc(title)} ({esc(category)})">{text}</a>')
            by_provider[provider].append((category in {"Answers", "1CM Solutions"}, pill))
    return "".join(
        resource_group(provider, "".join(pill for _, pill in sorted(links, key=lambda link: link[0])))
        for provider, links in by_provider.items()
        if links
    )


def resource_group(label, links):
    return (f'<div class="resource-group"><span class="resource-label">{label}</span>'
            f'<div class="resource-links">{links}</div></div>')


def video_link(name, url, timestamp="", provider="1st Class Maths"):
    label = esc(name)
    if timestamp:
        seconds = 0
        for unit in timestamp.split(":"):
            seconds = seconds * 60 + int(unit)
        url += f"&amp;t={seconds}s"
        label += f' <span class="chapter-time">{timestamp}</span>'
    return (f'<a class="pill watch" href="{esc(url)}" target="_blank" rel="noopener" '
            f'data-watch-title="{esc(name)}" data-watch-provider="{esc(provider)}">'
            f'<span aria-hidden="true">▶</span> {label}</a>')


def video_resource_groups(videos_by_provider):
    return "".join(
        resource_group(provider, "".join(links))
        for provider, links in videos_by_provider.items()
    )


def dr_frost_practice_group(skills):
    links = "".join(
        f'<a class="pill q" href="https://www.drfrost.org/explorer.php?ssid={int(skill["practice_id"])}"'
        f' target="_blank" rel="noopener">{esc(skill["name"])} &nearr;</a>'
        for skill in skills
    )
    return resource_group("Dr Frost online practice", links) if links else ""


def study_panel(name, description, watch, practice):
    description_html = f'<p class="study-description">{esc(description)}</p>' if description else ""
    groups = "".join(
        f'<div class="study-group"><h3>{label}</h3>{resources}</div>'
        for label, resources in (("Watch", watch), ("Practise", practice))
        if resources
    )
    return (
        f'<details class="study"><summary><span class="tname">{esc(name)}</span>'
        f'<span class="study-action">Study</span></summary><div class="study-body">'
        f'{description_html}<div class="study-groups">{groups}</div></div></details>'
    )


EDEXCEL_CSS = """
:root{--ink:#192e3c;--muted:#63747d;--line:#dde5e5;--teal:#087f74}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:100px}
body{margin:0;background:#f5f7f6;color:var(--ink);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--teal)}
button,input{font:inherit}
button,a,input,summary{-webkit-tap-highlight-color:transparent}
:focus-visible{outline:3px solid #079b8d;outline-offset:4px}
.wrap{max-width:1440px;padding:24px 36px 48px;margin:auto}
.hero{
  display:grid;
  grid-template-columns:minmax(0,1fr) minmax(175px,230px);
  align-items:center;
  gap:20px 32px;
  padding:24px 28px;
  border:1px solid #cfdfdc;
  border-radius:16px;
  background:linear-gradient(115deg,#fbfdfb,#e9f5f1 70%,#e7f1f8);
}
.hero-title{display:flex;align-items:center;gap:14px}
.hero-logo{display:block;width:36px;height:36px;object-fit:contain;flex:none}
.eyebrow{font-size:10px;letter-spacing:.12em;font-weight:750;text-transform:uppercase}
.hero h1{font-size:clamp(25px,3.4vw,40px);line-height:1.12;letter-spacing:-.035em;margin:0;font-weight:750}
.hero-progress{padding-left:22px;border-left:1px solid #cbdedb}
.past-papers-link{display:inline-block;margin-top:8px;font-weight:650}
.prog-label{color:#30565a;font-size:13px;font-weight:650;font-variant-numeric:tabular-nums;margin:0 0 7px}
.prog-track{height:6px;background:#c8dddb;border-radius:9px;overflow:hidden}
.prog-fill{height:100%;width:0;background:#087f74;border-radius:9px;transition:width .25s}
.workspace{display:grid;grid-template-columns:210px minmax(0,1fr);gap:32px;margin-top:24px;align-items:start}
.sidebar{position:sticky;top:26px;max-height:calc(100vh - 52px);overflow:auto;padding:6px 1px}
.eyebrow{color:var(--muted);margin:0 0 13px}
.jump{display:flex;flex-direction:column;gap:6px}
.jump a{display:grid;grid-template-columns:25px 1fr auto;align-items:center;gap:9px;text-decoration:none;color:#4d626d;padding:11px 10px;border:1px solid transparent;border-radius:8px;font-size:12px;font-weight:600;line-height:1.4}
.jump a:hover{background:#eaf0ee}
.jump a.active{color:#1e534a;background:#e6f0eb;border-color:#d2e3da}
.nav-num{color:var(--sec);font-size:11px;font-variant-numeric:tabular-nums}
.nav-count{font-size:10px;color:#687e83;font-weight:500}
.sidebar-resources{margin-top:18px;padding:14px 10px 0;border-top:1px solid var(--line)}
.sidebar-resources summary{cursor:pointer;color:#4d626d;font-size:12px;font-weight:650}
.sidebar-resources a{display:block;margin:11px 0;font-size:12px;color:#4d626d;text-decoration:none}
.sidebar-resources a:hover{text-decoration:underline;color:var(--teal)}
.save-note{margin:25px 10px 0;color:#6a7d81;font-size:11px;line-height:1.7}
.save-note b{display:block;color:#52686d;font-weight:600}
main{min-width:0}
.toolbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:10px;padding:12px 0;background:#f5f7f6;border-bottom:1px solid var(--line)}
.search{flex:1;position:relative;min-width:0}
.search svg{position:absolute;top:50%;left:14px;transform:translateY(-50%);color:#6d8088;pointer-events:none}
.search input{width:100%;height:44px;background:#fff;border:1px solid #d2dedd;border-radius:8px;padding:10px 48px 10px 41px;color:var(--ink);font-size:13px}
.search input:focus{outline:2px solid #76b8aa;outline-offset:1px}
.search kbd{position:absolute;right:13px;top:12px;border:1px solid #dce4e3;border-radius:4px;color:#7a8b90;font:11px/18px inherit;padding:0 5px;pointer-events:none}
.tools{display:flex;gap:7px}
.btn{cursor:pointer;background:#fff;border:1px solid #d2dedd;color:#455e69;padding:11px 13px;border-radius:8px;font-size:12px;white-space:nowrap}
.btn:hover{background:#edf3f0;border-color:#a8bdb6}
.btn.on{background:#1e534a;color:#fff;border-color:#1e534a}
.btn.danger{background:transparent;border-color:transparent;color:#687c82}
.btn.danger:hover{background:#fceeee;color:#a23636}
.list-intro{display:flex;align-items:baseline;justify-content:space-between;gap:15px;margin:25px 0 9px}
.list-intro h2{font-size:20px;letter-spacing:-.5px;margin:0;font-weight:700}
.result-count{color:var(--muted);font-size:12px}
.legend{margin:0 0 22px;border-bottom:1px solid var(--line);padding-bottom:16px;color:var(--muted);font-size:12px}
.legend summary{cursor:pointer;width:fit-content}
.legend-content{display:flex;flex-wrap:wrap;gap:14px 20px;padding-top:14px;font-size:11px;align-items:center}
.legend-content>span{display:flex;align-items:center;gap:6px}
.s-num{--sec:#ad6851}.s-alg{--sec:#397b9c}.s-geo{--sec:#30806e}.s-stat{--sec:#9a762d}.s-halg{--sec:#79649b}
.sec{margin:28px 0 0;scroll-margin-top:20px}
.sec-head{display:flex;gap:14px;align-items:center;margin-bottom:12px}
.sec-head h2{font-size:17px;letter-spacing:-.25px;font-weight:700;margin:0;display:flex;align-items:center;gap:10px}
.sec-head h2:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--sec,#7d9098);flex:none}
.sec-meta{margin-left:auto;font-size:11px;color:var(--muted);text-align:right}
.sec-done{font-weight:650;color:var(--teal)}
.topics{list-style:none;padding:0;margin:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.topic{display:grid;grid-template-columns:20px minmax(0,1fr);column-gap:14px;margin:0;padding:0 18px;border-bottom:1px solid #e8eded;scroll-margin-top:100px}
.topic:last-child{border-bottom:0}
.topic:hover{background:#fafcfb}
.topic input[type=checkbox]{width:18px;height:18px;accent-color:var(--teal);margin:15px 0 0;cursor:pointer}
.study>summary{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:48px;padding:8px 2px;cursor:pointer;list-style:none}
.study>summary::-webkit-details-marker{display:none}
.tname{font-size:14px;font-weight:650;line-height:1.5}
.study-action{display:inline-flex;align-items:center;gap:8px;flex:none;padding:4px 8px;border:1px solid #dce7e1;border-radius:6px;color:#326357;font-size:12px;font-weight:650}
.study-action::after{content:"";width:6px;height:6px;border:solid currentColor;border-width:0 1px 1px 0;transform:rotate(45deg);margin:0 2px 3px}
.study[open] .study-action::after{transform:rotate(225deg);margin:3px 2px 0}
.study[open] .study-action,.study>summary:hover .study-action{background:#e7f2ec;border-color:#cbded3}
.study-body{margin:0 0 14px;padding:14px 16px;border:1px solid #dfeae5;border-radius:8px;background:#f6faf8}
.study-description{margin:0 0 12px;color:#435e56;font-size:13px}
.study-groups{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px}
.study-group{min-width:0;padding:12px;border:1px solid #e0eae5;border-radius:7px;background:#fff}
.study-group h3{margin:0 0 8px;font-size:14px}
.resource-group+.resource-group{margin-top:10px}
.resource-label{display:block;margin-bottom:4px;font-size:11px;color:#52686d;font-weight:650}
.resource-links{display:flex;flex-wrap:wrap;gap:5px}
.pill{display:inline-block;text-decoration:none;border-radius:5px;font-size:11px;font-weight:600;line-height:1.5;padding:5px 8px;border:1px solid transparent;overflow-wrap:anywhere;transition:background .15s}
.pill:hover{filter:brightness(.95);text-decoration:underline;text-underline-offset:2px}
.pill .sfx{font-weight:400}
.pill.q{color:#285e8e;background:#edf4fa;border-color:#dce8f2}
.pill.t{color:#286b52;background:#edf6ef;border-color:#dcebdd}
.pill.a{color:#70578f;background:#f4eff8;border-color:#e7def1}
.pill.watch{color:#8e3034;background:#fff1f1;border-color:#f0d6d8}
.watch>span[aria-hidden]{margin-right:3px;font-size:9px}
.chapter-time{margin-left:3px;font-variant-numeric:tabular-nums;font-weight:500;white-space:nowrap}
.video-dock{position:fixed;inset:auto 16px max(16px,env(safe-area-inset-bottom)) auto;z-index:11;width:min(480px,calc(100% - 32px));max-height:calc(100dvh - 32px);overflow:auto;margin:0;padding:0;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);box-shadow:0 12px 40px #162d3970}
.video-head,.video-foot{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 13px;font-size:12px}
.video-head h2{margin:0;font-size:14px;line-height:1.35}
.video-head button{flex:none;padding:4px 10px;font-size:18px;line-height:1.25}
.video-dock iframe{display:block;width:100%;min-height:200px;aspect-ratio:16/9;border:0;background:#162d39}
.video-foot a{font-weight:650}
.pill.miss{color:#92632c;background:#fff8e9;border:1px dashed #d7bd8b}
.topic.done{background:#f1f8f4}
.topic.done .tname{color:#658178;text-decoration:line-through;text-decoration-color:#a6c5b5}
.empty-state{padding:45px 24px;text-align:center;border:1px dashed #c9d8d2;border-radius:12px;background:#fff;color:var(--muted)}
.empty-state h3{font-size:17px;color:var(--ink);margin:0 0 7px}
.empty-state p{margin:0;font-size:13px}
.coverage{border-top:1px solid var(--line);padding-top:28px;margin-top:40px}
.cov-note{font-size:12px;color:var(--muted);line-height:1.8}
.cov-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:14px;margin:18px 0}
.cov-box,.cov-details{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.cov-box h3{font-size:13px;margin:0 0 10px}
.cov-box ul,.speclist{list-style:none;padding:0;margin:0}
.cov-box li{font-size:12px;padding:8px 0;border-top:1px solid #e9eeee;color:#5b7078}
.gapbox{border-top:3px solid #d3b877}.extrabox{border-top:3px solid #92b9cb}
.gap-resources{margin-top:8px}
.cov-details summary{font-size:12px;font-weight:600;cursor:pointer}
.speclist{max-height:540px;overflow:auto;margin-top:15px}
.speclist li{display:grid;grid-template-columns:40px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--line);font-size:12px;color:#5b7078}
.speclist b{color:var(--ink);font-family:ui-monospace,monospace}
.sl-links a{display:inline-block;margin:4px 12px 0 0}.gaptag{color:#946b2f}
footer{margin-top:48px;border-top:1px solid var(--line);padding-top:20px;color:var(--muted);font-size:10px;line-height:1.8}
footer code{font-size:10px}
@media(max-width:1100px){.wrap{padding:24px}.workspace{grid-template-columns:175px minmax(0,1fr);gap:22px}}
@media(max-width:760px){html{scroll-padding-top:145px}.wrap{padding:18px 16px 32px}.hero{padding:18px 20px;column-gap:20px}.hero-progress{padding-left:16px}.workspace{display:flex;flex-direction:column;gap:14px;margin-top:20px}.sidebar{position:static;max-height:none;width:100%;padding:0;overflow:visible}.sidebar>.eyebrow,.sidebar-resources,.save-note{display:none}.jump{flex-direction:row;flex-wrap:wrap;gap:5px}.jump a{display:flex;padding:7px 10px;font-size:11px;background:#fff;border-color:var(--line);gap:7px}.nav-count{display:none}main{width:100%}.toolbar{flex-wrap:wrap;gap:8px;padding:10px 0}.search{flex-basis:100%}.search kbd{display:none}.btn{padding:8px 11px}.tools{width:100%}.list-intro{margin-top:20px}.list-intro h2{font-size:18px}.sec-head{align-items:baseline;flex-wrap:wrap;gap:5px}.sec-head h2{font-size:16px}.sec-meta{font-size:10px}.topic{padding:0 12px;column-gap:10px;scroll-margin-top:150px}.study-body{padding:10px}.study-group{padding:10px}.coverage .sec-meta{margin-left:18px;text-align:left}}
@media(max-width:760px){.sidebar .sidebar-resources{display:block;margin:12px 0 0;padding:8px 0 0}.sidebar-resources a{font-size:11px}}
@media(max-width:620px){
  .hero{grid-template-columns:1fr;gap:12px;padding:16px}
  .hero-title{gap:10px}
  .hero-logo{width:29px;height:29px}
  .hero-progress{padding:10px 0 0;border-left:0;border-top:1px solid #cbdedb}
}
@media print{.video-dock{display:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
@media print{body{background:#fff;font-size:11px}.sidebar,.toolbar,.legend,.empty-state,footer{display:none}.wrap{padding:0;max-width:none}.hero{background:#fff;color:#000;border:1px solid #aaa;display:block;padding:16px}.hero-progress{display:none}.workspace{display:block}.topic{break-inside:avoid;padding:0 10px}.study-action{display:none}.topics{overflow:visible}.sec{break-inside:auto}.sec-head{break-after:avoid}.speclist{max-height:none;overflow:visible}}
"""

EDEXCEL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edexcel Higher GCSE Maths</title>
<style>/*__CSS__*/</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="hero-title">
      <img class="hero-logo" src="sjalogo.png" width="36" height="36" alt="SJA monogram">
      <h1>Edexcel Higher GCSE Maths</h1>
    </div>
    <div class="hero-progress">
      <p class="prog-label" id="progText">0 of __N_TOPICS__ topics complete</p>
      <div class="prog-track" role="progressbar" aria-label="Revision progress" aria-valuemin="0" aria-valuemax="__N_TOPICS__" aria-valuenow="0"><div class="prog-fill" id="progFill"></div></div>
      <a class="past-papers-link" href="past-papers.html">Past papers →</a>
    </div>
  </header>
  <div class="workspace">
    <aside class="sidebar" aria-label="Revision navigation">
      <p class="eyebrow">Explore topics</p>
      <nav class="jump" aria-label="Topic sections">__JUMP__</nav>
      <details class="sidebar-resources">
        <summary>Revision booklets &amp; links</summary>
        <a href="__PDF_URL__" target="_blank" rel="noopener">Original checklist PDF ↗</a>
        __BOOKLET__
        __WALKTHROUGHS__
        <a href="__VIDEO_SOURCE__" target="_blank" rel="noopener">1st Class Maths Edexcel resources ↗</a>
        <a href="#speccoverage">Specification coverage ↓</a>
      </details>
      <p class="save-note"><b>Pick up where you left off.</b>Your ticks are saved automatically in this browser.</p>
    </aside>
    <main id="checklist">
      <div class="toolbar">
        <div class="search">
          <svg aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
          <input id="q" aria-label="Search topics and resources" type="search" placeholder="Search topics and resources…" autocomplete="off">
          <kbd aria-hidden="true">/</kbd>
        </div>
        <div class="tools">
          <button class="btn" id="hideDone" aria-pressed="false" title="Hide topics you have already ticked off">Hide completed</button>
          <button class="btn" id="withVideo" aria-pressed="false"__VIDEO_FILTER_HIDDEN__>With videos</button>
        </div>
      </div>
      <div class="list-intro"><h2>Your revision checklist</h2><span class="result-count" id="resultCount" role="status">__N_TOPICS__ topics</span></div>
      <details class="legend"><summary>How to use this checklist</summary>
        <div class="legend-content">
          <span>Open Study to see what a topic covers, watch a video or practise.</span>
          <span>On Dr Frost, select the skill, then choose Practise and Start.</span>
          <span>Videos are matched to Edexcel GCSE Maths Higher (1MA1). <a href="#speccoverage">See specification coverage</a></span>
          <span id="localVideoNote" hidden>For the corner player, open the checklist through a web server. From a local file, videos open on YouTube.</span>
          <span>Tick a topic to mark it complete. Your ticks stay in this browser.</span>
          <button class="btn danger" id="reset" title="Clear all ticks">Reset ticks</button>
        </div>
      </details>
      <div class="empty-state" id="emptyState" hidden><h3>No topics to show</h3><p>Try a different search or clear a filter.</p></div>
      __SECTIONS__
      __COVERAGE__
    </main>
  </div>
  <footer>Worksheets © corbettmaths.com · Exam papers &amp; solutions © 1st Class Maths · Videos from 1st Class Maths and Dr Frost Maths.<br>Worksheet links open the publishers’ original resources. <a href="__PDF_URL__" target="_blank" rel="noopener">Original CorbettMaths Edexcel checklist</a> &middot; <a href="https://corbettmaths.com/more/about/terms-of-use/" target="_blank" rel="noopener">CorbettMaths terms</a>.</footer>
</div>
<dialog class="video-dock" id="videoDock" aria-labelledby="videoTitle">
  <div class="video-head">
    <h2 id="videoTitle"></h2>
    <button class="btn" id="closeVideo" type="button" aria-label="Close video">×</button>
  </div>
  <div id="videoFrame"></div>
  <div class="video-foot"><span id="videoProvider"></span><a id="videoExternal" target="_blank" rel="noopener">Open on YouTube ↗</a></div>
</dialog>
<script>
//__JS__
</script>
</body>
</html>
"""

JS = """
const KEY = 'edexcel-checklist-done';
let store = JSON.parse(localStorage.getItem(KEY) || '{}');
const topics = [...document.querySelectorAll('li.topic')];
let hideDone = false;

function apply(li) {
  const matched = li.dataset.match !== '0';
  li.hidden = !matched || (hideDone && li.classList.contains('done'));
}

function refresh() {
  const done = topics.filter(t => t.classList.contains('done')).length;
  const progress = document.querySelector('.prog-track');
  document.getElementById('progText').textContent =
    done + ' of ' + topics.length + ' topics complete';
  document.getElementById('progFill').style.width = (done / topics.length * 100) + '%';
  progress.setAttribute('aria-valuenow', done);
}

topics.forEach(li => {
  const name = li.dataset.name;
  if (store[name]) { li.classList.add('done'); li.querySelector('input').checked = true; }
  li.dataset.match = '1';
  li.querySelector('input').addEventListener('change', e => {
    li.classList.toggle('done', e.target.checked);
    store[name] = e.target.checked;
    localStorage.setItem(KEY, JSON.stringify(store));
    refresh(); apply(li);
  });
});

document.getElementById('q').addEventListener('input', e => {
  const s = e.target.value.trim().toLowerCase();
  topics.forEach(li => {
    const hit = !s || li.dataset.name.includes(s)
      || (li.dataset.videos || '').includes(s)
      || (li.dataset.spec || '').includes(s)
      || li.textContent.toLowerCase().includes(s);
    li.dataset.match = hit ? '1' : '0';
    apply(li);
  });
});

document.getElementById('hideDone').addEventListener('click', e => {
  hideDone = !hideDone;
  e.currentTarget.classList.toggle('on', hideDone);
  topics.forEach(apply);
});

document.getElementById('reset').addEventListener('click', () => {
  if (!confirm('Clear all completed ticks?')) return;
  store = {};
  localStorage.removeItem(KEY);
  topics.forEach(li => {
    li.classList.remove('done');
    li.querySelector('input').checked = false;
  });
  refresh();
});

document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    document.getElementById('q').focus();
  }
});

refresh();
"""

EDEXCEL_JS = """
// Keep the workspace summary and navigation in sync with the shared checklist.
const checklistSections = [...document.querySelectorAll('section.sec:not(.coverage)')];
const videoFilter = document.getElementById('withVideo');
let withVideo = false;
function updateWorkspace() {
  topics.forEach(li => {
    apply(li);
    if (withVideo && !li.querySelector('.watch')) li.hidden = true;
  });
  const visible = topics.filter(t => !t.hidden).length;
  document.getElementById('resultCount').textContent =
    visible === topics.length ? topics.length + ' topics' : visible + ' of ' + topics.length + ' topics';
  document.getElementById('emptyState').hidden = visible !== 0;
  checklistSections.forEach(sec => {
    sec.hidden = ![...sec.querySelectorAll('li.topic')].some(t => !t.hidden);
    const completed = sec.querySelectorAll('li.topic.done').length;
    sec.querySelector('.sec-done').textContent = completed ? ' · ' + completed + ' done' : '';
  });
  document.getElementById('hideDone').setAttribute('aria-pressed', hideDone);
}
document.getElementById('q').addEventListener('input', updateWorkspace);
document.getElementById('hideDone').addEventListener('click', updateWorkspace);
document.getElementById('reset').addEventListener('click', updateWorkspace);
videoFilter.addEventListener('click', () => {
  withVideo = !withVideo;
  videoFilter.classList.toggle('on', withVideo);
  videoFilter.setAttribute('aria-pressed', withVideo);
  updateWorkspace();
  updateNavigation();
});
topics.forEach(li => li.querySelector('input').addEventListener('change', updateWorkspace));
const navLinks = [...document.querySelectorAll('.jump a')];
let navigationQueued = false;
function updateNavigation() {
  const visibleSections = checklistSections.filter(sec => !sec.hidden);
  let current = visibleSections[0];
  visibleSections.forEach(sec => { if (sec.getBoundingClientRect().top <= 160) current = sec; });
  navLinks.forEach(link => {
    const active = current && link.hash === '#' + current.id;
    link.classList.toggle('active', !!active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  navigationQueued = false;
}
document.addEventListener('scroll', () => {
  if (!navigationQueued) { navigationQueued = true; requestAnimationFrame(updateNavigation); }
}, {passive: true});
document.getElementById('q').addEventListener('input', updateNavigation);
document.getElementById('hideDone').addEventListener('click', updateNavigation);
updateWorkspace();
updateNavigation();

const videoDock = document.getElementById('videoDock');
const videoTitle = document.getElementById('videoTitle');
const videoProvider = document.getElementById('videoProvider');
const videoFrame = document.getElementById('videoFrame');
const videoExternal = document.getElementById('videoExternal');
const closeVideo = document.getElementById('closeVideo');
let videoTrigger;
if (location.protocol === 'file:') {
  // YouTube requires an HTTP referrer for embedded playback.
  document.getElementById('localVideoNote').hidden = false;
} else if (typeof videoDock.show === 'function') {
  document.querySelectorAll('a[data-watch-title]').forEach(link => {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const watch = new URL(link.href);
      const id = watch.searchParams.get('v');
      if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) return;
      event.preventDefault();
      videoTrigger = link;
      if (!videoDock.open || videoExternal.href !== link.href) {
        const embed = new URL('https://www.youtube-nocookie.com/embed/' + id);
        embed.searchParams.set('autoplay', '1');
        embed.searchParams.set('playsinline', '1');
        const timestamp = parseInt(watch.searchParams.get('t'), 10);
        if (timestamp > 0) embed.searchParams.set('start', timestamp);
        const frame = document.createElement('iframe');
        frame.title = link.dataset.watchProvider + ' video: ' + link.dataset.watchTitle;
        frame.referrerPolicy = 'strict-origin-when-cross-origin';
        frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
        frame.allowFullscreen = true;
        frame.src = embed.href;
        videoTitle.textContent = link.dataset.watchTitle;
        videoProvider.textContent = link.dataset.watchProvider;
        videoExternal.href = link.href;
        videoFrame.replaceChildren(frame);
      }
      if (!videoDock.open) videoDock.show();
      closeVideo.focus({preventScroll: true});
    });
  });
  function dismissVideo() {
    const restoreFocus = videoDock.contains(document.activeElement);
    videoDock.close();
    videoFrame.replaceChildren();
    if (restoreFocus && videoTrigger?.offsetParent) videoTrigger.focus({preventScroll: true});
  }
  closeVideo.addEventListener('click', dismissVideo);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && videoDock.open) dismissVideo();
  });
}
"""


def build_page(spec_map, by_video, all_files, descriptions, papers_by_topic=None,
               booklet=None, videos_by_topic=None, walkthroughs=(), video_source="",
               dr_frost_practice_by_topic=None):
    papers_by_topic = papers_by_topic or {}
    videos_by_topic = videos_by_topic or {}
    dr_frost_practice_by_topic = dr_frost_practice_by_topic or {}
    topic_ids = {}
    for sid, info in spec_map.items():
        for tp in info.get("topics", []):
            topic_ids.setdefault(tp, []).append(sid)
    topic_ids = {tp: sorted(ids, key=spec_key) for tp, ids in topic_ids.items()}

    sections_html, jump_html = [], []
    all_topic_names = []
    n_topics = n_watch = 0

    for section, topics in SECTIONS.items():
        items = []
        sec_total = sec_linked = 0
        for t in topics:
            name, videos = t[0], t[1]
            keep = t[2] if len(t) > 2 else None
            expanded = expand_videos(videos)
            sec_total += 1
            n_topics += 1

            files = []
            for v in expanded:
                files += by_video.get(v, [])
            # topic-name fallback when a video number found nothing
            if not files:
                key = norm(name)
                for row in all_files:
                    tp = norm(row["topic"])
                    if tp and (key.startswith(tp) or tp.startswith(key)):
                        files.append(row)
            # alias fallback: a topic reusing another topic's worksheets
            if not files and len(t) > 3 and t[3]:
                rx = re.compile(t[3], re.I)
                files = [f for f in all_files if rx.search(str(f["topic"]))]

            # optional keyword filter: one video number can cover several topics
            if keep:
                rx = re.compile(keep, re.I)
                files = [f for f in files if rx.search(str(f["topic"]))]

            # drop duplicate "(2)" download copies whose base file also exists
            dup_base = set()
            for file in files:
                m = re.match(r"^(.*) \(\d+\)\.pdf$", file["file"])
                if m:
                    dup_base.add(m.group(1) + ".pdf")
            unique, seen = [], set()
            for file in files:
                if file["file"] in seen or file["file"] in dup_base:
                    continue
                seen.add(file["file"])
                unique.append(file)

            dataname = esc(name.lower())
            datavideos = esc(" ".join(expanded))
            dataspec = esc(" ".join(topic_ids.get(name, [])).lower())
            anchor = f'id="topic-{norm(name)}" '

            desc = descriptions.get(name, "")
            all_topic_names.append(name)

            resources = unique + papers_by_topic.get(name, [])
            if resources:
                sec_linked += 1
                pills = build_link_pills(resources)
            elif name in VIDEO_ONLY:
                label = "Watch on CorbettMaths"
                pills = (f'<a class="pill miss" href="{VIDEO_ONLY[name]}" target="_blank" '
                         f'rel="noopener">{label} &nearr;</a>')
            else:
                label = "Find a worksheet"
                pills = (f'<a class="pill miss" href="{CORBETT_SEARCH}{quote(name)}" target="_blank" '
                         f'rel="noopener">{label} &nearr;</a>')

            watch = video_resource_groups(videos_by_topic.get(name, {}))
            n_watch += bool(watch)
            if not resources and name in VIDEO_ONLY:
                watch += resource_group("CorbettMaths", pills)
                pills = ""
            pills += dr_frost_practice_group(dr_frost_practice_by_topic.get(name, ()))
            body = study_panel(name, desc, watch, pills)

            missing_class = "" if resources else " missing"
            items.append(
                f'<li class="topic{missing_class}" {anchor}data-name="{dataname}" data-videos="{datavideos}"'
                f' data-spec="{dataspec}">'
                f'<input type="checkbox" aria-label="Mark {esc(name)} as completed">'
                f'{body}</li>'
            )

        sec_id = norm(section)
        sections_html.append(
            f'<section class="sec {SECTION_CLASS[section]}" id="{sec_id}">'
            f'<div class="sec-head"><h2>{esc(section)}</h2>'
            f'<span class="sec-meta">{sec_linked}/{sec_total} with worksheets'
            f'<span class="sec-done"></span></span></div>'
            f'<ul class="topics">{"".join(items)}</ul></section>'
        )
        jump_html.append(
            f'<a class="{SECTION_CLASS[section]}" href="#{sec_id}">'
            f'<span class="nav-num">{len(jump_html) + 1:02d}</span>'
            f'<span>{esc(section)}</span><span class="nav-count">{sec_total}</span></a>'
        )

    # ---------------- spec coverage section (boards with a spec map only)
    coverage_html = ""
    if spec_map:
        gaps = [sid for sid in spec_map if not spec_map[sid]["topics"]]
        extras = [n for n in all_topic_names if n not in topic_ids]
        gap_items = []
        for sid in sorted(gaps, key=spec_key):
            resources = video_resource_groups(videos_by_topic.get(sid, {}))
            resources += dr_frost_practice_group(dr_frost_practice_by_topic.get(sid, ()))
            gap_links = f'<div class="gap-resources">{resources}</div>' if resources else ""
            gap_items.append(f'<li><b>{sid}</b> &mdash; {esc(spec_map[sid]["text"])}{gap_links}</li>')
        extra_items = "".join(
            f'<li><a href="#topic-{norm(n)}">{esc(n)}</a> &mdash; not matched to any spec statement'
            f' (useful practice, but not required by the spec)</li>'
            for n in extras
        )
        gap_box = (
            f'<div class="cov-box gapbox"><h3>In the spec but missing from the checklist'
            f' ({len(gaps)})</h3><ul>{"".join(gap_items)}</ul></div>' if gaps else ""
        )
        extra_box = (
            f'<div class="cov-box extrabox"><h3>On the checklist but not in the spec'
            f' ({len(extras)})</h3><ul>{extra_items}</ul></div>' if extras else ""
        )
        spec_rows = []
        for sid in sorted(spec_map, key=spec_key):
            info = spec_map[sid]
            if info["topics"]:
                links = "".join(
                    f'<a href="#topic-{norm(t)}">{esc(t)}</a>' for t in info["topics"]
                )
                spec_rows.append(
                    f'<li><b>{sid}</b><span>{esc(info["text"])}<br>'
                    f'<span class="sl-links">{links}</span></span></li>'
                )
            else:
                spec_rows.append(
                    f'<li class="gap"><b>{sid}</b><span>{esc(info["text"])}<br>'
                    f'<em class="gaptag">no matching checklist topic</em></span></li>'
                )
        coverage_issues = (
            f'<div class="cov-grid">{gap_box}{extra_box}</div>' if gaps or extras else ""
        )
        coverage_counts = f'{len(spec_map) - len(gaps)}/{len(spec_map)} statements mapped'
        if gaps:
            coverage_counts += f' &middot; {len(gaps)} missing'
        if extras:
            coverage_counts += f' &middot; {len(extras)} unmatched topics'
        coverage_html = (
            f'<section class="sec coverage" id="speccoverage">'
            f'<div class="sec-head"><h2>Edexcel specification coverage</h2>'
            f'<span class="sec-meta">{coverage_counts}</span></div>'
            f'<p class="cov-note">Topics above are mapped against the '
            f'<a href="{SPEC_PDF_URL}" target="_blank" rel="noopener">Pearson Edexcel GCSE (9&ndash;1)'
            f' Mathematics specification</a> &mdash; Higher tier content, pages 24&ndash;32 '
            f'(statements N1&ndash;N16, A1&ndash;A25, R1&ndash;R16, G1&ndash;G25, P1&ndash;P9, S1&ndash;S6).</p>'
            f'{coverage_issues}'
            f'<details class="cov-details"><summary>Show all {len(spec_map)} spec statements'
            f' and the topics they map to</summary>'
            f'<ul class="speclist">{"".join(spec_rows)}</ul></details>'
            f'</section>'
        )
    booklet_stat = (
        f'<a href="{esc(booklet["url"])}" target="_blank" rel="noopener">'
        '1st Class Maths Higher booklet (PDF) ↗</a>'
        if booklet else ""
    )

    page = (
        EDEXCEL_TEMPLATE
        .replace("/*__CSS__*/", EDEXCEL_CSS)
        .replace("//__JS__", JS + EDEXCEL_JS)
        .replace("__SECTIONS__", "".join(sections_html))
        .replace("__COVERAGE__", coverage_html)
        .replace("__VIDEO_FILTER_HIDDEN__", " hidden" if n_watch == n_topics else "")
        .replace("__BOOKLET__", booklet_stat)
        .replace("__WALKTHROUGHS__", "".join(video_link(v["name"], v["url"]) for v in walkthroughs))
        .replace("__VIDEO_SOURCE__", esc(video_source))
        .replace("__JUMP__", "".join(jump_html))
        .replace("__N_TOPICS__", str(n_topics))
        .replace("__PDF_URL__", CHECKLIST_URL)
    )

    out = ROOT / "docs" / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"Built {out.relative_to(ROOT)} with {n_topics} topics")


def main():
    by_video, all_files = {}, []
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            by_video.setdefault(row["video_no"], []).append(row)
            all_files.append(row)

    descriptions = json.loads(DESC_FILE.read_text(encoding="utf-8"))
    spec_map = json.loads((ROOT / "edexcel_spec_map.json").read_text(encoding="utf-8"))
    papers_by_topic, videos_by_topic = {}, {}
    papers = json.loads((ROOT / "1stclassmaths_papers.json").read_text(encoding="utf-8"))
    for paper in papers["papers"]:
        links = [
            {"file": paper[kind]["file"], "source_url": paper[kind]["url"],
             "topic": paper["name"], "category": category}
            for kind, category in (("exam", "1CM Paper"), ("sol", "1CM Solutions"))
        ]
        for topic in paper["topics"]:
            papers_by_topic.setdefault(topic, []).extend(links)
            if paper.get("video"):
                videos_by_topic.setdefault(topic, {}).setdefault("1st Class Maths", []).append(
                    video_link(paper["name"], paper["video"])
                )
    for walkthrough in papers["walkthroughs"]:
        for chapter in walkthrough["chapters"]:
            link = video_link(chapter["name"], walkthrough["url"], chapter["time"])
            for topic in chapter["topics"]:
                videos_by_topic.setdefault(topic, {}).setdefault("1st Class Maths", []).append(link)

    frost = json.loads((ROOT / "dr_frost_videos.json").read_text(encoding="utf-8"))
    dr_frost_practice_by_topic = {}
    for topic, videos in frost["topics"].items():
        dr_frost_practice_by_topic[topic] = [video for video in videos if video.get("practice_id")]
        if videos:
            videos_by_topic.setdefault(topic, {})["Dr Frost Maths"] = [
                video_link(video["name"], f'https://www.youtube.com/watch?v={video["id"]}',
                           provider="Dr Frost Maths")
                for video in videos
            ]

    build_page(spec_map, by_video, all_files, descriptions,
               papers_by_topic=papers_by_topic, booklet=papers["booklet_higher"],
               videos_by_topic=videos_by_topic, walkthroughs=papers["walkthroughs"],
               video_source=papers["source"], dr_frost_practice_by_topic=dr_frost_practice_by_topic)


if __name__ == "__main__":
    main()
