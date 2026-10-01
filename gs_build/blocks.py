"""Python blocks: content generated from the data (called from GSM with  @py NAME args).

Each block receives the Builder (b) and string args. Add new blocks with @block("name").
"""
from collections import Counter, defaultdict

from engine import figures as F
from engine import style as S
from data import record as R
from data import topics as TP

REGISTRY = {}


def block(name):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


def _cache(name):
    S.CACHE.mkdir(parents=True, exist_ok=True)
    return S.CACHE / name


def _fmt(v):
    return "" if not v else (f"{v:g}" if v != 0.5 else "½").replace(".5", "½")


# ------------------------------------------------------------------ record figures
@block("heatmap_topics")
def heatmap_topics(b, *args):
    m = R.topic_year_matrix()
    rows = [f"T{t['n']} · {t['short']}" for t in TP.TOPICS]
    vals = [[m[(t['n'], y)] for y in R.YEARS] for t in TP.TOPICS]
    p = _cache("MA_heat_topics.png")
    F.fig_heatmap(rows, [str(y) for y in R.YEARS], vals, str(p), cmap_hex=S.PLUM,
                  row_colours=[t["colour"] for t in TP.TOPICS], fmt="{:g}")
    b.figure_file(p, width_in=6.5, caption="The heat map: visits to each topic, year by year (a full question = 1, a short-note part = ½).")


@block("heatmap_heads")
def heatmap_heads(b, *args):
    m = defaultdict(float)
    for d in R.items():
        heads = {R.HEAD_OF_FAMILY[f] for f in d["families"]}
        for h in heads:
            m[(h, d["year"])] += d["weight"] / len(heads)
    heads = list(TP.SYLLABUS_HEADS)
    rows = [f"{h}. {TP.SYLLABUS_HEADS[h]}" for h in heads]
    vals = [[round(m[(h, y)], 2) for y in R.YEARS] for h in heads]
    p = _cache("MA_heat_heads.png")
    F.fig_heatmap(rows, [str(y) for y in R.YEARS], vals, str(p), cmap_hex=S.TEAL, fmt="{:.2g}")
    b.figure_file(p, width_in=6.5, caption="The same record by the nine syllabus heads (a question touching two heads is shared between them).")


@block("topic_weights")
def topic_weights(b, *args):
    w = R.topic_weights()
    lines = [f"T{t['n']} · {t['short']}: {w[t['n']]:g}" + (" *" if w[t['n']] == max(w.values()) else "")
             for t in TP.TOPICS]
    b.figure("bars", "How much each topic weighs: total visits, 2016–2026 (the heaviest in coral).",
             lines + ["@colour plum", "@xlabel visits (full question = 1; short-note part = ½)"])


@block("mcq_weights")
def mcq_weights(b, *args):
    c = R.mcq_topic_matrix()
    lines = [f"T{t['n']} · {t['short']}: {sum(c[(t['n'], y)] for y in R.MCQ_YEARS)}" for t in TP.TOPICS]
    b.figure("bars", "The objective paper: the 140 recovered MCQs by topic (2016, 2018, 2019, 2023–2026).",
             lines + ["@colour teal", "@xlabel number of MCQs"])


@block("mcq_table")
def mcq_table(b, *args):
    c = R.mcq_topic_matrix()
    rows = ["Topic | " + " | ".join(str(y) for y in R.MCQ_YEARS) + " | Total | Share"]
    tot = sum(c.values())
    for t in TP.TOPICS:
        v = [c[(t['n'], y)] for y in R.MCQ_YEARS]
        rows.append(f"T{t['n']} · {t['short']} | " + " | ".join(str(x or "–") for x in v) +
                    f" | ^^{sum(v)}^^ | {100 * sum(v) / tot:.0f}%")
    rows.append("^^All^^ | " + " | ".join(f"^^{sum(c[(t['n'], y)] for t in TP.TOPICS)}^^" for y in R.MCQ_YEARS)
                + f" | ^^{tot}^^ | 100%")
    b.table("The 140 recovered MCQs, topic by year.", ["@widths 5,1,1,1,1,1,1,1,1.2,1.2"] + rows)


# ------------------------------------------------------------------ record tables
@block("papers_glance")
def papers_glance(b, *args):
    rows = ["Year | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8"]
    by = defaultdict(dict)
    for d in R.items():
        key = d["q"]
        tag = f"T{d['topic']}"
        by[d["year"]][key] = (by[d["year"]].get(key, "") + ("/" if key in by[d["year"]] else "") + tag)
    for y in R.YEARS:
        rows.append(f"^^{y}^^ | " + " | ".join(by[y].get(q, "") for q in range(2, 9)))
    b.table("The eleven papers at a glance: which topic each question came from (a slash = a short-note question "
            "split between topics).", ["@widths 1.3,1,1,1,1,1,1,1.4", "@font 9.5"] + rows)


@block("repeat_engine")
def repeat_engine(b, minimum="3", maximum="99"):
    lo, hi = int(minimum), int(maximum)
    fc = R.family_counts()
    rows = ["Family | Topic | Times | Years asked"]
    top = {}
    for d in R.items():
        for f in d["families"]:
            top.setdefault(f, d["topic"])
    for f, v in sorted(fc.items(), key=lambda kv: (-len(kv[1]), kv[1][0][0])):
        if lo <= len(v) <= hi:
            yrs = ", ".join(str(y) for y, _ in v)
            rows.append(f"{R.FAMILIES[f]} | T{top[f]} | ^^{len(v)}^^ | {yrs}")
    b.table("", ["@widths 7,1,1,3.2"] + rows)


@block("beyond_table")
def beyond_table(b, *args):
    rows = ["Question | Topic | What it asked that the syllabus never names"]
    notes = {
        "2018-5": "Pakistan's global gender-gap ranking (the WEF Global Gender Gap Report)",
        "2018-8a": "Caroline Moser's practical and strategic gender needs (on the reading list, not in the syllabus)",
        "2020-4": "Gendered language",
        "2025-6": "Intersectionality as a theory",
        "2026-4": "The Global Gender Gap Report 2025 — a named, dated report",
        "2026-5": "Climate change, feminist environmentalism and ecofeminism; the 2022 floods and heat waves",
        "2026-7": "Intersectionality applied to rural, minority and disabled women in Pakistan",
        "2026-8a": "The digital gender gap — mobile internet use, 2024–2025",
    }
    for d in R.items():
        if d["beyond"]:
            rows.append(f"{R.label(d)} | T{d['topic']} | {notes.get(d['id'], R.FAMILIES[d['families'][0]])}")
    b.table("Beyond the syllabus: questions whose subject the syllabus does not name.", ["@widths 2.4,1,8"] + rows)


@block("leaks_table")
def leaks_table(b, *args):
    rows = ["Question | Home topic | Also needs | Why"]
    why = {
        "2017-4": "democracy and development need the status data of T5",
        "2018-4": "choosing a feminism for Pakistan needs the movement's history (T3)",
        "2018-5": "reasons for the ranking include the history of laws and the movement (T3)",
        "2018-6": "impacts of globalisation on Pakistani women need T5 data",
        "2018-8c": "government initiatives sit with the laws of T5",
        "2019-8a": "the suffragists are also the first wave (T3)",
        "2020-3": "colonial reformers are also the roots of the movement (T3)",
        "2024-6": "the 2016 Punjab Act is also women and law (T5)",
        "2025-6": "intersectionality begins with the question 'what is gender?' (T1)",
        "2025-8": "Malala is also the story of girls' education (T5)",
        "2026-2": "the transgender law is also women and law (T5)",
        "2026-4": "the gap report's political empowerment sub-index is T6",
        "2026-5": "ecofeminism is a theory (T2); flood impacts are status data (T5)",
        "2026-6": "the WAD critique is taught in T4",
        "2026-7": "intersectionality as a theory is taught in T2",
        "2026-8b": "masculinities are first taught in T1",
    }
    for d in R.items():
        if d["leaks"]:
            rows.append(f"{R.label(d)} | T{d['topic']} | " + ", ".join(f"T{x}" for x in d["leaks"]) +
                        f" | {why.get(d['id'], '')}")
    b.table("The leaks: questions that draw on two topics.", ["@widths 2.4,1.3,1.3,7"] + rows)


@block("command_words")
def command_words(b, *args):
    words = ["discuss", "critically", "explain", "what", "write a note", "differentiate", "define", "evaluate",
             "analy", "short note", "your view", "opinion", "trace", "outline", "comment", "elaborate",
             "describe", "compare", "examine", "how"]
    c = Counter()
    for d in R.items():
        cmd = d["command"].lower()
        for w in words:
            if w in cmd:
                c[w] += 1
    pretty = {"analy": "analyse / analysis", "what": "what (is / are)", "your view": "give your views",
              "opinion": "in your opinion", "critically": "critically (examine / analyse / evaluate / review)"}
    lines = [f"{pretty.get(w, w)}: {n}" for w, n in c.most_common(12)]
    b.figure("bars", "The command words the examiner uses most (a question can use several).",
             lines + ["@colour navy", "@xlabel appearances in 84 question items, 2016–2026"])


@block("topic_questions")
def topic_questions(b, n):
    """Table of every past question of a topic (for dossiers and KB Part Three)."""
    n = int(n)
    rows = ["Year · Q | The question (as set) | Family"]
    for d in R.by_topic(n):
        txt = d["text"] if not d["short"] else f"Short note: {d['text']}"
        rows.append(f"^^{d['year']}^^ · Q{d['q']}{('(' + d['part'] + ')') if d['part'] else ''} | {txt} | "
                    + "; ".join(R.FAMILIES[f] for f in d["families"]))
    b.table(f"Every question the examiner has set on T{n}, 2016–2026.", ["@widths 1.5,8.5,3", "@font 9"] + rows)


@block("appendix_a")
def appendix_a(b, *args):
    by = defaultdict(list)
    for d in R.items():
        by[d["year"]].append(d)
    for y in R.YEARS:
        b.heading(2, f"CSS {y}")
        rows = ["Q | The question | Topic · family"]
        for d in by[y]:
            q = f"Q{d['q']}" + (f"({d['part']})" if d["part"] else "")
            txt = d["text"] if not d["short"] else f"Short note — {d['text']}"
            rows.append(f"^^{q}^^ | {txt} | T{d['topic']} · " + "; ".join(R.FAMILIES[f] for f in d["families"]))
        b.table("", ["@widths 1.1,9.6,3.3", "@font 9"] + rows)


@block("mapping_heads")
def mapping_heads(b, *args):
    lines = ["@left The nine syllabus heads", "@right The seven topics of these notes"]
    for t in TP.TOPICS:
        for h in t["heads"]:
            lines.append(f"{h}. {TP.SYLLABUS_HEADS[h]} => T{t['n']} · {t['short']}")
    b.figure("mapping", "From nine syllabus heads to seven topics: nothing is dropped, nothing is split.", lines)


@block("family_docs")
def family_docs(b, *args):
    """The family of documents diagram."""
    import matplotlib
    cv = F.Canvas(11.0)
    W = 11.0
    cv.rect(3.4, 0.1, 4.2, 0.85, fc=S.PLUM, ec=S.PLUM, r=0.12)
    cv.text(W / 2, 0.22, "MA · The Master Anatomy", 14, "FFFFFF", bold=True, ha="center")
    cv.text(W / 2, 0.55, "the map — read first", 10.5, S.tint(S.PLUM, 0.7), italic=True, ha="center")
    bw, gap, x0 = 1.42, 0.12, 0.25
    for i, t in enumerate(TP.TOPICS):
        x = x0 + i * (bw + gap)
        c = t["colour"]
        cv.line([(W / 2, 0.95), (x + bw / 2, 1.55)], S.GREY, 1.2, arrow=True)
        cv.rect(x, 1.6, bw, 0.72, fc=c, ec=c)
        cv.text(x + bw / 2, 1.8, f"T{t['n']}KB", 13, "FFFFFF", bold=True, ha="center")
        cv.text(x + bw / 2, 2.07, "Knowledge Base", 8.5, S.tint(c, 0.7), ha="center")
        cv.rect(x, 2.45, bw, 0.72, fc="FFFFFF", ec=c, lw=2)
        cv.text(x + bw / 2, 2.63, f"T{t['n']}QA", 13, c, bold=True, ha="center")
        cv.text(x + bw / 2, 2.9, "Question Answers", 8.5, c, ha="center")
    cv.text(W / 2, 3.45, "compiled at the end from all seven topics", 11, S.SLATE, italic=True, ha="center")
    comp = [("FB", "The Fact Book", S.CORAL), ("QA", "Question Answers", S.BLUE), ("OL", "One-Liners & MCQs", S.GOLD),
            ("RN", "Revision Notes", S.TEAL), ("PR", "Prediction Papers", S.ROSE)]
    bw2, g2 = 1.95, 0.18
    for i, (code, name, c) in enumerate(comp):
        x = 0.25 + i * (bw2 + g2)
        cv.rect(x, 3.8, bw2, 0.95, fc=S.tint(c, 0.88), ec=c, lw=2)
        cv.text(x + bw2 / 2, 3.95, code, 14, c, bold=True, ha="center")
        cv.text(x + bw2 / 2, 4.32, name, 10, c, bold=True, ha="center")
    p = _cache("MA_family.png")
    cv.render(4.95, str(p))
    b.figure_file(p, width_in=6.5, caption="The family of documents: one map, fourteen topic documents, five compiled volumes.")


# ------------------------------------------------------------------ QA helpers
@block("question")
def question(b, qid, *args):
    """Print a past question exactly as set, from the database:  @py question 2019-3   (or 2024-8a)."""
    d = next(x for x in R.items() if x["id"] == qid)
    txt = d["text"] if not d["short"] else f"{d['stem']}: {d['text']}"
    b.box("glance", f"{R.label(d)}  ·  20 marks" if not d["short"] else f"{R.label(d)}  ·  10 marks",
          [txt])


@block("qa_index")
def qa_index(b, n):
    """Table listing the answers in a TnQA document, in order."""
    n = int(n)
    rows = ["No. | Question | Year · Q | Family"]
    for i, d in enumerate(R.by_topic(n), 1):
        rows.append(f"{i} | {d['text'][:140] + ('…' if len(d['text']) > 140 else '')} | {R.label(d)} | "
                    + "; ".join(R.FAMILIES[f] for f in d["families"]))
    b.table(f"The questions answered for Topic {n}, in the order they were set.", ["@widths 0.8,8.2,2.4,2.6", "@font 9"] + rows)


@block("mcqs_topic")
def mcqs_topic(b, n):
    """All past MCQs of a topic, with keys (for KB Part Four and the OL volume)."""
    n = int(n)
    rows = ["Year | Question | Key"]
    for m in R.mcqs_tagged():
        if m["topic"] == n:
            rows.append(f"{m['year']} · {m['n']} | {m['stem']} | {m['answer']}")
    b.table(f"Every recovered MCQ on T{n}, with its key.", ["@widths 1.6,7.6,4.8", "@font 9"] + rows)


@block("qa_master_index")
def qa_master_index(b, *args):
    """Every past question by year, with the topic and answer number it has in the compiled QA volume."""
    num = {}
    for t in TP.TOPICS:
        for i, d in enumerate(R.by_topic(t["n"]), 1):
            num[d["id"]] = (t["n"], i)
    by = defaultdict(list)
    for d in R.items():
        by[d["year"]].append(d)
    for y in R.YEARS:
        if not by[y]:
            continue
        b.heading(2, f"CSS {y}")
        rows = ["Q | The question | Answer"]
        for d in sorted(by[y], key=lambda x: (x["q"], x["part"])):
            q = f"Q{d['q']}" + (f"({d['part']})" if d["part"] else "")
            txt = d["text"] if not d["short"] else f"Short note — {d['text']}"
            txt = txt[:170] + ("…" if len(txt) > 170 else "")
            t, i = num[d["id"]]
            rows.append(f"^^{q}^^ | {txt} | T{t} · Answer {i}")
        b.table(f"CSS {y}: every question and where it is answered.", ["@widths 1.1,10.3,2.6", "@font 9"] + rows)
