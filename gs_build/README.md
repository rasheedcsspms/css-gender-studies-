# gs_build — the CSS Gender Studies document engine

Everything that produces the Word documents in `CSS Gender Studies/`.

- **Start here:** [`SPEC.md`](SPEC.md) — status, standing instructions, markup, templates, budgets, workflow.
- Build: `pip install python-docx matplotlib pillow` then `python3 gs_build/build.py MA` (or `T1KB`, `T1QA`, `all`).
- Preview (optional): `python3 gs_build/preview.py MA` → page images in `gs_build/.cache/preview/`.

```
gs_build/
  build.py            build a document by code (MA, T1KB, T1QA … FB, QA, OL, RN, PR)
  blocks.py           data-driven blocks (@py …): heat maps, record tables, past questions
  preview.py          LibreOffice → PDF → contact sheets, for visual checks
  tools_wordcount.py  word count of GSM files
  engine/             style.py (palette, boxes, cards) · docxkit.py (Word helpers) · markup.py (GSM parser) · figures.py
  data/               topics.py · record.py (tags) · descriptive.json · mcqs.json · facts_verified.md
  content/            GSM sources: MA/ (done), T1/ … T7/, FB/, QA/, OL/, RN/, PR/, TEST/ (syntax demo)
  templates/          KB and QA skeletons
  fonts/              Lato (SIL OFL) for figures
```
