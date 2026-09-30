# CSS Gender Studies — Production Spec

This is the production bible for the Gender Studies set. **Read this file first in any new session.** It holds every
decision already made, so a session never has to re-derive them. Content blueprints for each topic live in
`content/MA/05_dossiers.gsm` (Part Four of the Master Anatomy: "What the Tn documents will carry").

---

## 0. Status tracker

| Code | Document | Source | Status |
|---|---|---|---|
| MA | The Master Anatomy | `content/MA/*.gsm` | ✅ built (≈30,000 words, 15 figures, 44 tables) |
| T1KB / T1QA | Gender Studies and the Social Construction of Gender | `content/T1/` | ✅ v2 (Standards v2) — KB ≈22,900 words (core ≈16,600 + 123 one-liners + MCQs + 3,900-word sheet), 20 figures; QA 16 answers + 1 note, all 1,000–1,070 (note 553), 34 figures; feeders `oneliners.gsm`, `rn_sheet.gsm`, `rn_plans.gsm`, `RN.gsm` (≈5,200), `facts.gsm` |
| T2KB / T2QA | Feminist Theories and Practice | `content/T2/` | ✅ Standards v2 — KB ≈22,300 words (core ≈16,700 + 128 one-liners + 26 MCQs + 3,700-word sheet), 25 figures; QA 6 answers + 2 notes, all 1,021–1,075 (notes 553–559), 16 figures; feeders `oneliners.gsm`, `rn_sheet.gsm`, `rn_plans.gsm`, `RN.gsm` (≈4,800), `facts.gsm` |
| T3KB / T3QA | Feminist Movements — the West, the United Nations and Pakistan | `content/T3/` | ✅ Standards v2 — KB ≈21,000 words (core ≈15,400 + 126 one-liners + 22 MCQs + 3,400-word sheet), 25 figures; QA 8 answers + 1 note + the 2023 repeat page, all 1,001–1,026 (note 542), 20 figures; feeders `oneliners.gsm`, `rn_sheet.gsm`, `rn_plans.gsm`, `RN.gsm`, `facts.gsm` |
| T4KB / T4QA | Gender and Development | `content/T4/` | ✅ Standards v2 — KB ≈23,000 words (core ≈17,000 + 126 one-liners + 17 MCQs + 3,900-word sheet), 29 figures; QA 16 answers + 3 notes, all 974–1,012 (notes 550–555), 39 figures; feeders `oneliners.gsm`, `rn_sheet.gsm`, `rn_plans.gsm`, `RN.gsm`, `facts.gsm` |
| T5KB / T5QA | Status of Women in Pakistan | `content/T5/` | ⬜ next |
| T6KB / T6QA | Gender and Governance | `content/T6/` | ⬜ |
| T7KB / T7QA | Gender-Based Violence and the Three Case Studies | `content/T7/` | ⬜ |
| FB | The Fact Book | `content/FB/main.gsm` (+ `content/Tn/facts.gsm`) | ⬜ after T7 |
| QA | The Question Answers — all seven | `content/QA/main.gsm` (includes `content/Tn/QA.gsm` bodies) | ⬜ after T7 |
| OL | The One-Liner and MCQ Bank | `content/OL/main.gsm` (+ `content/Tn/oneliners.gsm`) | ⬜ after T7 |
| RN | The Revision Notes — all seven | `content/RN/main.gsm` (+ `content/Tn/RN.gsm`) | ⬜ after T7 |
| PR | The Prediction Papers — Sets 1–3 | `content/PR/main.gsm` | ⬜ last |

Update this table when a document is finished.

## 1. The user's standing instructions (do not re-ask)

1. Gender Studies is a **separate subject**. The Islamic Studies and British History folders are only samples of
   quality; do not cross-reference or depend on them.
2. **Seven topics** (Heads I+II → T1; III → T2; IV → T3; V → T4; VI → T5; VII → T6; VIII+IX → T7). Every head covered
   comprehensively.
3. Reader is a **complete beginner**: simple English, every term defined on first use and used precisely.
4. **Word (.docx) only.** No PDFs — the user updates the contents fields and exports the PDFs themselves.
5. **KB length 15,000–19,000 words** (small ± margin; heavier topics longer — budgets in §6).
   **Each QA answer 1,000–1,300 words** (short notes 550–650 words each).
6. **Revision Notes more detailed than the Islamic Studies sample**: ≈4,500 words per topic.
7. The evidence volume is a **Fact Book** (FB): all facts, dates, stats, laws, reports, thinkers, cases — up to date.
8. Better than the samples in every way; comprehensive; current to the latest data.

## 2. Build

```bash
pip install python-docx matplotlib pillow            # engine
python3 gs_build/build.py MA                          # or T1KB T1QA … or all
# optional visual check (LibreOffice Writer + PyMuPDF):
apt-get install -y --no-install-recommends libreoffice-writer fonts-crosextra-carlito
pip install pymupdf
python3 gs_build/preview.py T1KB                      # -> gs_build/.cache/preview/T1KB_NN.png (4 pages per sheet)
```

- `build.py` prints the **word count**, figure count and captioned-table count. Use it to hit the budgets.
- Outputs go to `CSS Gender Studies/<folder>/<file>.docx` (names come from `data/topics.py`; never hand-name files).
- Figures are cached in `gs_build/.cache/` (git-ignored) by content hash.
- `content/TEST/main.gsm` exercises every block and figure type — a living syntax demo. `python3 gs_build/build.py TEST`.

## 3. GSM — the markup (full reference)

```
---                                   front matter (first lines of main.gsm)
code: T1KB
title: The Knowledge Base
subtitle: Topic 1 · Gender Studies and the Social Construction of Gender
header: T1 Knowledge Base                (running header text)
gives: item one; item two; item three    (cover-page bullets, ';'-separated)
---
@toc                                  contents page (Word field; user updates it)
@include file.gsm                     splice another file (paths relative to this file)
%% comment                            ignored
# Heading 1   (new page)  ## H2  ### H3  #### H4  ##### H5
plain lines → one paragraph (blank line ends it)
- bullet   /   "  - " level 2   /   "    - " level 3
1. numbered paragraph (also i. ii. / a) b))
> lead paragraph (italic intro)
@pagebreak
@py NAME arg …                        python block from blocks.py
```

Inline: `**key term**` (bold green — use for terms the reader must define) · `==1972==` (bold navy — dates/numbers to
memorise) · `^^bold^^` · `*italic*` (titles of books).

Blocks open with `::: kind …` and close with a line `:::`.

| Kind | Head syntax | Renders |
|---|---|---|
| Boxes | `::: simple` · `::: trap \| Title` | shaded box with label; `simple example trap eye debate pakistan remember balance islam note glance update method` |
| Cards | `::: thinker Name \| descriptor` | evidence card; `define thinker quote data law case report` |
| Table | `::: table \| Caption` then `@widths 3,7` `@font 9` `@header off` `@firstbold on`; rows `a \| b \| c`; ` // ` = line break in a cell | caption above; header row coloured |
| Figure | `::: fig TYPE \| Caption` + spec lines (§4) | PNG, auto-sized, numbered caption |

Inside boxes/cards: plain lines form paragraphs; `- ` bullets; `1. ` numbered; `-> point` = the bold arrow line
("what this proves") — **every evidence card ends with a `->` line**.

## 4. Figure templates (spec lines; options start with `@`)

| Type | Items | Options |
|---|---|---|
| `mindmap` (answer map) | `(1) Heading: point; point; point` | `@ask ① LIMB` (repeat), `@note text` |
| `flow` | `Title: sub text` | `@dir across\|down`, `@per 4`, `@colour teal` |
| `timeline` | `1848: label`; `== Group name` starts a band | `@layout horizontal\|vertical` (auto: >8 items or groups → vertical) |
| `bars` | `Label: 42` (trailing ` *` = highlight) | `@unit %`, `@max 100`, `@sort`, `@colour`, `@xlabel` |
| `compare` | `## Column` then `- item` | `@vs vs`, `@c1 plum` … |
| `tree` | first line = root; `- Child: desc`; `  - grandchild` | `@per 4` |
| `grid` | `Title: text` (or `Title: a; b; c` → bullets) | `@cols 3`, `@colour` |
| `cycle` | `Title: text` | `@centre text` |
| `spectrum` | `0-100: label` | `@left`, `@right` |
| `venn` | 2–3 × `Label: text` | `@centre text` |
| `pyramid` | top→bottom `Title: text` | |
| `matrix` (2×2) | 4 × `Title: text` (TL, TR, BL, BR) | `@x label`, `@y label` |
| `mapping` | `left label => right label` | `@left title`, `@right title` |

Any figure: `@width 5.5` forces the width in inches (default: natural size, max 6.5).

## 5. Data and python blocks

- `data/descriptive.json`, `data/mcqs.json` — extracted from the past-paper .docx files (`data/extract_papers.py`).
- `data/record.py` — `TAGS` (topic, families, command words, leaks, beyond-syllabus) for all 84 items; `FAMILIES`;
  `MCQ_TOPICS`; helpers `items()`, `by_topic(n)`, `label(d)`, `mcqs_tagged()`.
- `data/topics.py` — the seven topics (titles, heads, colours, budgets, folder/file names).
- `data/facts_verified.md` — facts already checked on the web, with sources (reuse; refresh only the volatile ones).

Blocks (`@py NAME args`):

| Block | Use |
|---|---|
| `question 2019-3` / `question 2024-8a` | prints the past question exactly as set in a box (QA documents) |
| `qa_index N` | table of all questions answered in TnQA |
| `topic_questions N` | every past question of topic N (KB Part Three) |
| `mcqs_topic N` | every past MCQ of topic N with keys (KB Part Four; OL) |
| `heatmap_topics`, `heatmap_heads`, `topic_weights`, `mcq_weights`, `mcq_table`, `papers_glance`, `repeat_engine MIN MAX`, `beyond_table`, `leaks_table`, `command_words`, `appendix_a`, `mapping_heads`, `family_docs` | record analytics (MA; reuse in PR/RN) |

## 6. House style (applies to every document)

- **Voice:** simple English, short sentences, one idea per sentence; explain every term the first time (bold green
  `**term**`), and use terms precisely thereafter. Speak to the reader ("you").
- **Evidence inside the point:** thinker / data / law / case / report / quote cards sit *inside* the heading they prove,
  each ending with a `->` line saying what it proves. Data always carries **source + year**.
- **Every chapter** has: at least one `simple` box, at least one `example`, a `trap` or `eye` where useful, the
  **Pakistan angle**, and at least one figure.
- **Balance** on sensitive questions (religion and women's rights, Aurat March, transgender law, "Western" feminism,
  NGO-isation, quotas): state neutrally → each side fairly → anchor in the Constitution (Arts. 25, 34, 35; 2A, 31, 227),
  CEDAW/SDGs and evidence → practical way forward. Never mock any side. Islamic perspective: accurate, brief,
  respectful; no verse/hadith unless certain.
- **Nothing invented:** no fabricated quotations or statistics; flag doubtful "facts" instead of repeating them.
- **Spellings:** Malala Yousafzai; Sharmeen Obaid-Chinoy; Mukhtaran Mai (also "Mukhtar Mai"); Simone de Beauvoir;
  Kimberlé Crenshaw; Raewyn (R. W.) Connell; Zia-ul-Haq; Ra'ana Liaquat Ali Khan.
- **Colours** are automatic per topic (`data/topics.py`); do not hard-code.

## 6a. Standards v2 — the user's review of Topic 1 (these OVERRIDE §7–§8 wherever they differ)

1. **One-liners** (`content/Tn/oneliners.gsm`): about **120**, **numbered** (`1. …`, continuous across groups), grouped
   under `### A · …` sub-headings by chapter. Written **in the style of the past MCQs** — analytic, one fact or
   distinction per line, "which is NOT / incorrect" traps included, past-MCQ facts tagged "(MCQ 2018)". **Bold every
   key word, name and date**: `**term**` (terms and names), `==1949==` (dates, numbers), `***italic-bold***` for
   Urdu/Latin terms and titles. KB Part Four = intro + `@include ../oneliners.gsm` + `@py mcqs_topic N` (past MCQs
   stay in the KB).
2. **Revision sheet** (`content/Tn/rn_sheet.gsm`, ≈3,500–4,000 words): the topic for **exam night**, one `##` section
   per chapter, bullets of the form "**term** = meaning in a few words"; every thinker with their idea and year, every
   date with its event, every law with its key section — **each line must make complete sense on its own**. Included
   by KB Part Five (`kb/p5_revision.gsm`) **and** by the RN volume. `content/Tn/RN.gsm` = H1 + glance box +
   `@include rn_sheet.gsm` + `@include rn_plans.gsm` (answer plans for every past question; RN only).
3. **Language:** simpler — short sentences, everyday words, every technical term explained in brackets or the next
   sentence; quotations followed by an "In simple words:" arrow line.
4. **Answer maps:** every point is a **short phrase that makes complete sense** to an examiner (6–14 words), e.g.
   "Pakistan founded five Women's Studies centres in 1989" — never a bare date or name. 3–4 points per branch.
5. **Model answers:** two levels of headings — `### 1. Introduction` … and `#### i) Definition` … under each.
   The introduction always has `i) Definition` (simple), background/origin, the Pakistani context, and the argument.
   Every sub-heading = one point in a short paragraph (2–4 sentences) with **key words in bold**. Big parts of a
   question (e.g. "the autonomy/integration debate") get their own main heading with many sub-headings (origin →
   definition + simple example → case for each → risks → view). **At least one figure besides the answer map**
   (compare / flow / cycle / tree / spectrum / grid / venn / pyramid), plus a table where useful.
   Length 1,000–1,300 words (short notes 550–650) — check with `tools_wordcount.py --answer`.
6. **KB length:** teaching core (Parts Zero–Three) 15,000–19,000 words; with one-liners, past MCQs and the revision
   sheet the file is ≈22,000–24,000 words — accepted by the user.

## 7. The Knowledge Base (TnKB) — skeleton and budgets

Copy `templates/KB_skeleton.gsm` to `content/Tn/KB.gsm` and fill it. Chapter plans: MA Part Four (the dossier table
"TnKB — chapter plan"). Structure:

1. `@toc`; **How to Use This Document** (what the topic covers; how the document is built; reading order) — ~500 words
2. **Part Zero — The ABC** — key-terms table (25–35 terms, ★ for must-define), the topic on one page (figure), background
3. **Part One — the chapters** — one chapter per syllabus line and per past-question family (MA dossier plan). Headings
   up to 5 levels; each chapter 900–1,800 words; cards inside points; ≥1 figure per chapter; 10–18 figures total
4. **Part Two — Contemporary Debates** — the topic's list in MA §2.4, each with a `balance` or `debate` box and latest data
5. **Part Three — The Examiner's Record** — `@py topic_questions N`; what the record reveals; five likely questions
   (not solved)
6. **Part Four — The One-Liner Bank** — `@include oneliners.gsm` (40–80 one-liners, table `Fact | Answer`) and
   `@py mcqs_topic N`
7. **Part Five — The Revision Sheet** — the topic on 3–4 pages (short tables and a couple of figures)

Also write, while the topic is fresh (these feed the compiled volumes):
- `content/Tn/oneliners.gsm` — the one-liner table (included by KB Part Four and by OL)
- `content/Tn/facts.gsm` — the topic's Fact Book section: tables of dates, laws (with sections), data (source+year),
  thinkers & books, conferences/reports, cases (included by FB)
- `content/Tn/RN.gsm` — the topic's Revision Notes chapter, ≈4,500 words (included by RN)

| Topic | KB budget | QA answers |
|---|---|---|
| T1 | ≈18,500 | 16 full + 1 note |
| T2 | ≈17,500 | 6 full + 2 notes |
| T3 | ≈17,000 | 9 full (2019-3 = 2023-5 answered once) + 1 note |
| T4 | ≈19,000 | 16 full + 3 notes |
| T5 | ≈17,000 | 8 full + 1 note |
| T6 | ≈16,000 | 8 full + 1 note |
| T7 | ≈18,000 | 9 full + 3 notes |

KB word counts as printed by `build.py` include tables, boxes and captions (the one-liner/MCQ tables of Part Four
count too); aim for the budget ± 1,000.

## 8. The Question Answers (TnQA) — skeleton

Copy `templates/QA_skeleton.gsm`. Order answers as `@py qa_index N` lists them (chronological within topic). Each answer:

```
# Answer k · <short title> (CSS YYYY)
@py question YYYY-Q
## The answer map
::: fig mindmap | The answer map: every branch is one numbered heading of the model answer below.
@note one line on the strategy
@ask ① LIMB ONE …
(1) Introduction: …
…
:::
## Decoding the question
(command words, limbs, what each demands — 80–150 words)
## The model answer
### (1) Introduction          ← definitions + context + thesis
### (2) … headings from the question's own words; (i)/(ii) and (a)/(b) below; evidence cards inside;
         one figure or table; Pakistan angle; counter-argument
### (n) Conclusion            ← judgement + way forward + weighty last line
## Why this answer scores
(4–6 bullets)
```

- **The model answer itself = 1,000–1,300 words** (map, decoding and "why it scores" are extra).
- Short-note questions: one `# Answer` with `@py question YYYY-8a` and `@py question YYYY-8b`, each note 550–650 words.
- Exact repeat (2019-3 / 2023-5): answer once; add a `note` box at the second occurrence.
- Measure: build and read the count; or write each answer in its own file `content/Tn/qa/NN.gsm` and include them
  (makes counting per answer easy: `python3 gs_build/tools_wordcount.py content/T1/qa/01.gsm`).

## 9. Compiled volumes

- **QA**: `content/QA/main.gsm` = front matter + `@toc` + one H1 part per topic that `@include`s `../Tn/qa/*.gsm`.
- **OL**: front matter + per topic `@include ../Tn/oneliners.gsm` + `@py mcqs_topic N` + new practice MCQs
  (`content/OL/practice_Tn.gsm`, 25–40 per topic, weighted to lines the objective paper has not touched).
- **RN**: front matter + per topic `@include ../Tn/RN.gsm` (≈4,500 words each).
- **FB**: front matter + master timeline + per topic `@include ../Tn/facts.gsm` + a "numbers card" + an index of laws
  and a thinkers index. Refresh volatile data (see `data/facts_verified.md`) just before finalising.
- **PR**: three sets exactly in FPSC format (MA Appendix B); 20 MCQs + Q.2–Q.8; keys; full model answers. Cover all
  Tier 3 blind spots at least once; T1, T4, T7 in every set.

## 10a. Lessons from Topic 1 (apply from T2 on)

- **Write answers longer than feels necessary.** First drafts of T1 model answers came out at ~800–950 words;
  every one needed topping up. Draft each model answer with 10–13 headings of 100–130 words each, and check with
  `python3 gs_build/tools_wordcount.py --answer content/Tn/qa/*.gsm` (counts only "## The model answer").
- KB chapters drafted at ~1,000–1,500 words each; with Parts Zero–Five the T1 KB landed at ≈18,600 — the chapter
  plan in the MA dossier is the right size (11 chapters + Parts). Use `tools_wordcount.py content/Tn/kb/*.gsm`.
- File layout that worked: `content/Tn/KB.gsm` (front matter + includes), `kb/00_front.gsm`, `kb/chNN_*.gsm`,
  `kb/p2_debates.gsm`, `kb/p3_record.gsm`, `kb/p4_oneliners.gsm` (includes `../oneliners.gsm` + `@py mcqs_topic N`),
  `kb/p5_revision.gsm`; `QA.gsm` + `qa/NN.gsm` (one answer per file, in `qa_index` order).
- Each QA answer: `# Answer k · Title (CSS YYYY)`, `@py question ID`, map (mindmap), decoding, model answer
  (with one table or card inside), "Why this answer scores".
- Verify unfamiliar facts before writing; never attribute specific claims to a reading-list author you have not read
  (use a `remember`/`note` box instead of a `thinker` card).


- **Lessons from Topic 2.** Inline markup: `***x***` is bold-italic (green), and `*italic*` may now sit inside `**bold**` (the parser was fixed in T2; before that, `***x***` printed a stray asterisk). `fig matrix` is a 2×2 quadrant — exactly four items, one sentence each (points joined by `;` run together). `fig mapping` uses `=>`, not `->`. Drafted answers again ran short (800–960); top up with "In simple words", "An example" and "The reply" sub-headings.
- **Lessons from Topic 3.** A table's header row must not begin with an empty cell (` | A | B`) — the parser drops it; write `Aspect | A | B`. Exact repeats (2019/2023) get a short "refresh" page so answer numbers still match `qa_index`. The `--answer` count excludes figures and tables: draft each answer at 3–4 sentences per sub-heading or it lands near 800.

## 10. Workflow for one topic (the cheap path)

1. Read this SPEC, `data/facts_verified.md`, and the topic's dossier in `content/MA/05_dossiers.gsm`.
2. `python3 -c "…R.by_topic(N)…"` or `@py topic_questions N` to see the questions.
3. Verify only the facts not already in `facts_verified.md` (web search); append new ones there with sources.
4. Write `content/Tn/KB.gsm` chapter by chapter (multiple files + `@include` if long), then `oneliners.gsm`,
   `facts.gsm`, `RN.gsm`.
5. Write `content/Tn/QA.gsm` (+ `qa/NN.gsm`).
6. `python3 gs_build/build.py TnKB TnQA`; check words; `python3 gs_build/preview.py TnKB` and look at 2–3 sheets.
7. Update §0, commit, push.
