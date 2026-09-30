"""The examiner's record, tagged: every descriptive item 2016–2026 by topic, family, command word and leaks.

A full question counts as 1 visit; a short-note part counts as 0.5.
TAGS[id] = (topic, [families], command words, [leak topics], beyond_syllabus)
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
YEARS = list(range(2016, 2027))
MCQ_YEARS = [2016, 2018, 2019, 2023, 2024, 2025, 2026]

FAMILIES = {
    "DISCIPLINE": "Gender Studies as a discipline — meaning, need, scope",
    "GS_VS_WS": "Women's Studies versus Gender Studies",
    "MULTI": "The multidisciplinary nature of Gender Studies",
    "AUTONOMY": "The autonomy versus integration debate",
    "STATUS_PK": "Status of Gender / Women's Studies in Pakistan",
    "CONSTRUCTION": "Social construction of gender — theories; deconstructing 'gender'",
    "SEX_GENDER": "Sex versus gender; is sex socially constructed; nature versus nurture",
    "MASC_FEM": "Masculinities, femininities and gender roles",
    "QUEER_TRANS": "Queer theory and transgender rights",
    "LANGUAGE": "Gendered language",
    "INTERSECT": "Intersectionality",
    "FEMINISM_SCHOOLS": "What is feminism; schools of feminism compared",
    "RADICAL": "Radical feminism",
    "MARXIST": "Marxist / socialist feminism",
    "PSYCHO": "Psychoanalytic feminism",
    "POSTMODERN": "Postmodern feminism",
    "FEM_FOR_PK": "Which feminism suits Pakistan",
    "WAVES": "The waves of Western feminism and their influence on Pakistan",
    "PK_MOVEMENT": "The women's movement in Pakistan",
    "APWA_WAF": "APWA and WAF",
    "NGO": "NGO-isation of the women's movement",
    "COLONIAL_CAP": "Colonial and capitalist perspectives of gender",
    "DEV_THEORIES": "Gender analysis of development theories",
    "MODERNIZATION": "Modernisation (and dependency) theory",
    "STRUCT_FUNC": "Structural functionalism",
    "GLOBALIZATION": "Globalisation and gender",
    "SAPS": "Gender critique of Structural Adjustment Policies",
    "WID_WAD_GAD": "WID, WAD and GAD",
    "PGN_SGN": "Practical and strategic gender needs",
    "CLIMATE": "Gender, climate change and ecofeminism",
    "HEALTH": "Women's health in Pakistan",
    "EMPLOYMENT": "Women and paid employment",
    "GENDER_GAP": "Pakistan and the Global Gender Gap",
    "LAW_RIGHTS": "Women, law and human rights",
    "DIGITAL": "The digital gender gap",
    "QUOTA": "Political quotas for women",
    "PARTICIPATION": "Women's political participation",
    "REPRESENTATIVES": "Women as representatives / politicians",
    "LEADERSHIP": "Women in leadership",
    "SUFFRAGE": "The suffragist movement",
    "GBV_FORMS": "GBV — forms, sites and strategies to eliminate it",
    "GBV_THEORY": "GBV — causes, theories, power and control",
    "GBV_LAW": "GBV — laws and state initiatives",
    "HONOUR": "Honour killing",
    "MASC_VAW": "Masculinities and violence against women",
    "CASE_MM": "Case study — Mukhtaran Mai",
    "CASE_SOC": "Case study — Sharmeen Obaid-Chinoy",
    "CASE_MALALA": "Case study — Malala Yousafzai",
}

T = True
F = False
TAGS = {
    "2016-2": (1, ["STATUS_PK", "AUTONOMY"], "write a note; give your views", [], F),
    "2016-3": (7, ["GBV_FORMS"], "what are; how", [], F),
    "2016-4": (6, ["QUOTA"], "pros and cons; give your views", [], F),
    "2016-5": (3, ["PK_MOVEMENT"], "write a note; strengths and weaknesses", [], F),
    "2016-6": (1, ["CONSTRUCTION"], "what are", [], F),
    "2016-7": (2, ["FEMINISM_SCHOOLS", "RADICAL", "MARXIST"], "what is; how different", [], F),
    "2016-8": (4, ["WID_WAD_GAD"], "critically review", [], F),
    "2017-2": (1, ["DISCIPLINE", "GS_VS_WS"], "define and discuss; differentiate", [], F),
    "2017-3": (7, ["GBV_FORMS"], "what are; in your opinion", [], F),
    "2017-4": (6, ["PARTICIPATION"], "comment", [5], F),
    "2017-5": (5, ["HEALTH"], "what is; how could", [], F),
    "2017-6": (4, ["GLOBALIZATION"], "discuss", [], F),
    "2017-7": (1, ["AUTONOMY"], "write a comprehensive note", [], F),
    "2017-8a": (7, ["HONOUR"], "short note", [], F),
    "2017-8b": (4, ["WID_WAD_GAD"], "short note", [], F),
    "2018-2": (1, ["GS_VS_WS", "STATUS_PK"], "what are; substantiate; highlight", [], F),
    "2018-3": (1, ["SEX_GENDER"], "write a comprehensive essay", [], F),
    "2018-4": (2, ["FEM_FOR_PK"], "what type(s)", [3], F),
    "2018-5": (5, ["GENDER_GAP", "LAW_RIGHTS"], "what reasons", [3], T),
    "2018-6": (4, ["GLOBALIZATION"], "what are the impacts", [5], F),
    "2018-7": (6, ["PARTICIPATION"], "do you think", [], F),
    "2018-8a": (4, ["PGN_SGN"], "short note", [], T),
    "2018-8b": (3, ["APWA_WAF"], "short note", [], F),
    "2018-8c": (7, ["GBV_LAW"], "short note", [5], F),
    "2019-2": (1, ["DISCIPLINE", "GS_VS_WS", "STATUS_PK"], "differentiate; trace", [], F),
    "2019-3": (3, ["WAVES"], "outline and explain; discuss", [], F),
    "2019-4": (4, ["MODERNIZATION", "DEV_THEORIES"], "explain; critically analyse", [], F),
    "2019-5": (4, ["GLOBALIZATION"], "discuss", [], F),
    "2019-6": (5, ["EMPLOYMENT"], "discuss", [], F),
    "2019-7": (7, ["GBV_FORMS", "CASE_MM"], "explain", [], F),
    "2019-8a": (6, ["SUFFRAGE"], "short note", [3], F),
    "2019-8b": (2, ["POSTMODERN"], "short note", [], F),
    "2019-8c": (4, ["STRUCT_FUNC"], "short note", [], F),
    "2020-2": (1, ["CONSTRUCTION", "SEX_GENDER"], "how do you deconstruct", [], F),
    "2020-3": (4, ["COLONIAL_CAP"], "how did", [3], F),
    "2020-4": (1, ["LANGUAGE"], "what does this imply; explain", [], T),
    "2020-5": (6, ["LEADERSHIP"], "is this useful or inappropriate", [], F),
    "2020-6": (5, ["LAW_RIGHTS"], "critically evaluate", [], F),
    "2020-7": (7, ["GBV_THEORY"], "comment", [], F),
    "2020-8": (7, ["CASE_SOC"], "discuss", [], F),
    "2021-2": (1, ["AUTONOMY"], "discuss in detail", [], F),
    "2021-3": (1, ["MASC_FEM", "SEX_GENDER"], "discuss", [], F),
    "2021-4": (2, ["MARXIST"], "discuss", [], F),
    "2021-5": (2, ["PSYCHO"], "give a detailed analysis", [], F),
    "2021-6": (4, ["MODERNIZATION"], "discuss and elaborate", [], F),
    "2021-7": (4, ["WID_WAD_GAD"], "critically analyse", [], F),
    "2021-8": (6, ["QUOTA"], "rethink and discuss", [], F),
    "2022-2": (1, ["MULTI"], "discuss in detail", [], F),
    "2022-3": (2, ["FEMINISM_SCHOOLS"], "describe", [], F),
    "2022-4": (3, ["WAVES"], "shed light", [], F),
    "2022-5": (6, ["REPRESENTATIVES"], "in your opinion", [], F),
    "2022-6": (3, ["PK_MOVEMENT"], "discuss in detail", [], F),
    "2022-7": (4, ["COLONIAL_CAP"], "what are; explain", [], F),
    "2022-8": (4, ["SAPS"], "discuss in detail", [], F),
    "2023-2": (1, ["STATUS_PK", "AUTONOMY"], "write a note; give your views", [], F),
    "2023-3": (1, ["GS_VS_WS", "MULTI"], "differentiate; discuss in detail", [], F),
    "2023-4": (1, ["MASC_FEM"], "define; in your opinion", [], F),
    "2023-5": (3, ["WAVES"], "outline and explain; discuss", [], F),
    "2023-6": (4, ["COLONIAL_CAP"], "write a detailed note", [], F),
    "2023-7": (5, ["HEALTH"], "elucidate; what measures", [], F),
    "2023-8": (7, ["GBV_FORMS"], "define; explain; devise", [], F),
    "2024-2": (5, ["HEALTH"], "discuss", [], F),
    "2024-3": (4, ["COLONIAL_CAP"], "write a note; throw light", [], F),
    "2024-4": (3, ["WAVES", "PK_MOVEMENT"], "write in detail; compare", [], F),
    "2024-5": (4, ["DEV_THEORIES"], "give a critical gender analysis", [], F),
    "2024-6": (7, ["GBV_LAW", "GBV_FORMS"], "what is; what forms; what are", [5], F),
    "2024-7": (6, ["PARTICIPATION", "QUOTA"], "is it; what obstacles; what impact", [], F),
    "2024-8a": (1, ["SEX_GENDER"], "short note", [], F),
    "2024-8b": (2, ["RADICAL"], "short note", [], F),
    "2025-2": (7, ["GBV_THEORY"], "what are; how", [], F),
    "2025-3": (4, ["GLOBALIZATION", "DEV_THEORIES"], "critically evaluate", [], F),
    "2025-4": (3, ["WAVES"], "discuss", [], F),
    "2025-5": (6, ["QUOTA"], "elaborate", [], F),
    "2025-6": (2, ["INTERSECT"], "give a detailed analysis", [1], T),
    "2025-7": (4, ["WID_WAD_GAD"], "critically analyse; discuss", [], F),
    "2025-8": (7, ["CASE_MALALA"], "critically examine and evaluate", [5], F),
    "2026-2": (1, ["QUEER_TRANS", "CONSTRUCTION"], "critically examine; how", [5], F),
    "2026-3": (3, ["PK_MOVEMENT"], "trace; how", [], F),
    "2026-4": (5, ["GENDER_GAP"], "evaluate; identify", [6], T),
    "2026-5": (4, ["CLIMATE"], "critically analyse", [2, 5], T),
    "2026-6": (3, ["NGO", "WID_WAD_GAD"], "critically examine", [4], F),
    "2026-7": (5, ["INTERSECT"], "using … examine", [2], T),
    "2026-8a": (5, ["DIGITAL"], "short note", [], T),
    "2026-8b": (7, ["MASC_VAW"], "short note", [1], F),
}

# the heads each question answers, for the syllabus-head heat map
HEAD_OF_FAMILY = {
    "DISCIPLINE": "I", "GS_VS_WS": "I", "MULTI": "I", "AUTONOMY": "I", "STATUS_PK": "I",
    "CONSTRUCTION": "II", "SEX_GENDER": "II", "MASC_FEM": "II", "QUEER_TRANS": "II", "LANGUAGE": "II",
    "INTERSECT": "III", "FEMINISM_SCHOOLS": "III", "RADICAL": "III", "MARXIST": "III", "PSYCHO": "III",
    "POSTMODERN": "III", "FEM_FOR_PK": "III",
    "WAVES": "IV", "PK_MOVEMENT": "IV", "APWA_WAF": "IV", "NGO": "IV",
    "COLONIAL_CAP": "V", "DEV_THEORIES": "V", "MODERNIZATION": "V", "STRUCT_FUNC": "V", "GLOBALIZATION": "V",
    "SAPS": "V", "WID_WAD_GAD": "V", "PGN_SGN": "V", "CLIMATE": "V",
    "HEALTH": "VI", "EMPLOYMENT": "VI", "GENDER_GAP": "VI", "LAW_RIGHTS": "VI", "DIGITAL": "VI",
    "QUOTA": "VII", "PARTICIPATION": "VII", "REPRESENTATIVES": "VII", "LEADERSHIP": "VII", "SUFFRAGE": "VII",
    "GBV_FORMS": "VIII", "GBV_THEORY": "VIII", "GBV_LAW": "VIII", "HONOUR": "VIII", "MASC_VAW": "VIII",
    "CASE_MM": "IX", "CASE_SOC": "IX", "CASE_MALALA": "IX",
}


def items():
    data = json.loads((HERE / "descriptive.json").read_text(encoding="utf-8"))
    for d in data:
        t, fams, cmd, leaks, beyond = TAGS[d["id"]]
        d.update(topic=t, families=fams, command=cmd, leaks=leaks, beyond=beyond,
                 weight=0.5 if d["short"] else 1.0)
    return data


def mcqs():
    return json.loads((HERE / "mcqs.json").read_text(encoding="utf-8"))


def topic_year_matrix():
    m = defaultdict(float)
    for d in items():
        m[(d["topic"], d["year"])] += d["weight"]
    return m


def topic_weights():
    c = Counter()
    for d in items():
        c[d["topic"]] += d["weight"]
    return c


def family_counts():
    """family -> list of (year, id)"""
    out = defaultdict(list)
    for d in items():
        for f in d["families"]:
            out[f].append((d["year"], d["id"]))
    return out


def by_topic(n):
    return [d for d in items() if d["topic"] == n]


def label(d):
    """'CSS 2019 · Q3' or 'CSS 2019 · Q8(b)'."""
    return f"CSS {d['year']} · Q{d['q']}" + (f"({d['part']})" if d["part"] else "")


if __name__ == "__main__":
    ids = {d["id"] for d in items()}
    assert ids == set(TAGS), set(TAGS) ^ ids
    print("weights:", dict(sorted(topic_weights().items())))
    print("total visits:", sum(topic_weights().values()))
    fc = family_counts()
    for f, v in sorted(fc.items(), key=lambda kv: -len(kv[1])):
        print(f"{len(v):2d}  {f:16s} {[y for y, _ in v]}")


# MCQ topic tags: one digit (topic 1-7) per question, in paper order
MCQ_TOPICS = {
    2016: "32725153666255363576",
    2018: "51323151611341446555",
    2019: "33442265713553572644",
    2023: "71411741121213754112",
    2024: "25312235664757146211",
    2025: "21212142223344437763",
    2026: "16412313222472431352",
}


def mcqs_tagged():
    out = []
    for m in mcqs():
        m = dict(m)
        m["topic"] = int(MCQ_TOPICS[m["year"]][m["n"] - 1])
        out.append(m)
    return out


def mcq_topic_matrix():
    c = defaultdict(int)
    for m in mcqs_tagged():
        c[(m["topic"], m["year"])] += 1
    return c
