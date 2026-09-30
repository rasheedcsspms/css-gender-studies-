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

total = 0
for f in sys.argv[1:]:
    _, lines = read_source(Path(f))
    b = Builder(K.new_document(), "WC", blocks=blocks.REGISTRY)
    b.run(lines)
    total += b.words
    print(f"{b.words:7,}  {f}")
if len(sys.argv) > 2:
    print(f"{total:7,}  total")
