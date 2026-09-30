#!/usr/bin/env python3
"""One-off: read the two past-paper .docx files and write descriptive.json and mcqs.json.

Re-run only if the past-paper files change:  python3 gs_build/data/extract_papers.py
"""
import json
import re
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
PP = HERE.parents[1] / "CSS Gender Studies" / "CSS_GS_PP_Gender Studies_Past Papers"


def paras(name):
    return [(p.style.name, p.text.strip()) for p in docx.Document(PP / name).paragraphs if p.text.strip()]


def descriptive():
    out, year = [], None
    for st, tx in paras("CSS_GS_PP_D_2015-2026.docx"):
        if st == "GS Annual":
            year = int(tx.split()[-1])
        m = re.match(r"Q\. No\. (\d)\.\s+(.*?)\s+\(20\)$", tx)
        if st == "GS Question" and m and year:
            q, text = int(m.group(1)), m.group(2)
            if "short note" in text.lower() and "(a)" in text:
                stem, _, rest = text.partition("(a)")
                rest = re.sub(r"\(10 marks each\)", "", "(a)" + rest)
                bits = re.split(r"\(([a-c])\)\s*", rest)[1:]
                for letter, ptxt in zip(bits[0::2], bits[1::2]):
                    out.append(dict(id=f"{year}-{q}{letter}", year=year, q=q, part=letter,
                                    stem=stem.strip().rstrip(":").strip(),
                                    text=ptxt.strip().rstrip(";.").strip(), short=True))
            else:
                out.append(dict(id=f"{year}-{q}", year=year, q=q, part="", stem="", text=text, short=False))
    return out


def mcqs():
    out, year, cur = [], None, None
    for st, tx in paras("CSS_GS_PP_MCQS_2015-2026.docx"):
        if st == "GS Annual":
            year = int(tx.split()[-1])
        elif st == "GS MCQ Stem":
            n, _, stem = tx.partition(" ")
            cur = dict(year=year, n=int(n.rstrip(".")), stem=stem.strip(), options=[], answer="")
            out.append(cur)
        elif st == "GS Option" and cur:
            cur["options"].append(re.sub(r"^\([A-D]\)\s*", "", tx))
        elif st == "GS Answer" and cur:
            cur["answer"] = tx.replace("Answer:", "").strip()
    return out


if __name__ == "__main__":
    d, m = descriptive(), mcqs()
    (HERE / "descriptive.json").write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
    (HERE / "mcqs.json").write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(d), "descriptive items;", len(m), "MCQs")
