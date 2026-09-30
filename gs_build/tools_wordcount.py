#!/usr/bin/env python3
"""Word count of one or more GSM files, counted exactly as build.py counts (tables, boxes, captions included).

    python3 gs_build/tools_wordcount.py content/T1/qa/01.gsm content/T1/qa/02.gsm
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import docxkit as K          # noqa: E402
from engine.markup import Builder, read_source   # noqa: E402
import blocks                              # noqa: E402

def answer_only(lines):
    """Keep only the lines under '## The model answer' (up to the next '## ')."""
    out, keep = [], False
    for ln in lines:
        if ln.startswith("## "):
            keep = ln.strip().lower().startswith("## the model answer")
            continue
        if keep and not ln.startswith("@py"):
            out.append(ln)
    return out


args = sys.argv[1:]
only = "--answer" in args
args = [a for a in args if a != "--answer"]
total = 0
for f in args:
    _, lines = read_source(Path(f))
    if only:
        lines = answer_only(lines)
    b = Builder(K.new_document(), "WC", blocks=blocks.REGISTRY)
    b.run(lines)
    total += b.words
    print(f"{b.words:7,}  {f}")
if len(args) > 1:
    print(f"{total:7,}  total")
