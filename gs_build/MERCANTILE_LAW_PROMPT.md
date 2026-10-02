# Session prompt — CSS Mercantile Law study library

*Paste everything below this line into the new session, after uploading: (1) the reference folders `CSS Gender Studies/` and `gs_build/`, (2) the Mercantile Law past papers (descriptive and MCQs), and (3) the FPSC CSS syllabus for Mercantile Law.*

---

## 0. Who you are and what you are building

You are building a complete, examination-ready **study library for the CSS (FPSC, Pakistan) optional subject Mercantile Law**, as Word (.docx) volumes, for a candidate sitting **CE-2027 onwards**.

A finished library of exactly this kind already exists for **CSS Gender Studies**. I have uploaded it as your reference:

- **`CSS Gender Studies/`** holds the finished .docx volumes. Read several of them to see the target quality, layout, depth and tone.
- **`gs_build/`** holds the engine that produced them:
  - the Python build system (`build.py`, `engine/`, `blocks.py`, `preview.py`, `tools_wordcount.py`);
  - the markup sources (`content/…`);
  - the production bible, **`gs_build/SPEC.md`**.

**Your library must match the Gender Studies library in structure, standard, styling and process, with one deliberate change.** Every model answer, in every volume, must follow the format of the Gender Studies **Prediction Papers** (`gs_build/content/PR/s1/*.gsm`, `s2/`, `s3/`). Do not use the older format of the Gender Studies topic QA documents. The **answer maps** must also be clearer than in the Prediction Papers (see §7).

Word output only. Do **not** produce PDFs as deliverables; PDFs are used only to preview.

---

## 1. Inputs, and what to do first (before writing any content)

1. **Read `gs_build/SPEC.md` completely.**
   - It is the production bible: the markup language (GSM), the figure types, the boxes and cards, the blocks, the house style, the length floors and the lessons learned.
   - Everything in it applies here unless this prompt changes it.
2. **Read the engine**: `build.py`, `engine/markup.py`, `engine/figures.py`, `engine/docxkit.py`, `engine/fpsc.py`, `blocks.py`, `data/record.py`, `data/topics.py`, `content/OL/make_ol.py`.
3. **Read these as examples:**
   - one Prediction Paper answer (`content/PR/s2/q4.gsm`);
   - one KB chapter (`content/T7/kb/ch07_laws.gsm`);
   - a revision sheet (`content/T5/rn_sheet.gsm`);
   - a one-liner file (`content/T6/oneliners.gsm`);
   - `content/PR/set1.txt`, and the MA sources in `content/MA/`.
4. **Copy the engine** to a new folder **`ml_build/`**, rename codes and titles for Mercantile Law, and keep the engine working.
   - Do not edit `gs_build/` itself.
   - Output goes to **`CSS Mercantile Law/`**, with one subfolder per volume, named as in the Gender Studies library: `MA_Master Anatomy`, `T1_Topic I — …`, `QA_…`, `FB_…`, `OL_…`, `RN_…`, `PR_…`.
5. **Write `ml_build/SPEC.md`** — the Mercantile Law production bible.
   - Adapt the Gender Studies SPEC and add every rule in this prompt.
   - Keep it updated after every volume (status table, lessons learned).
6. **Build the question database** from the uploaded past papers:
   - `data/descriptive.json` (year, Q number, part, text, short-note flag);
   - `data/mcqs.json` (year, n, stem, four options, key).
   - Tag every item by topic, by question family and by command word (`data/record.py`, as in Gender Studies).
   - Record honestly which years' papers or MCQ sheets are missing. Never reconstruct a missing paper.
7. **Read the syllabus** and list every syllabus head and line exactly as FPSC prints it.
8. **Do not start writing volumes yet.**
   - First reply with: (a) the list of years and items recovered; (b) your proposed **topic grouping** (§3) with weights from the record; (c) the volume plan.
   - Then wait for my approval.

---

## 2. The library (same volumes as Gender Studies)

| Code | Volume | What it is |
|---|---|---|
| **MA** | The Master Anatomy | The subject from zero. Covers: the paper and its format, the syllabus mapped to topics, the full record of past papers (heat maps, question families, repeats, blind spots, command words), the MCQ record, method, a study plan, and appendices (including the FPSC paper format). Built first. |
| **TnKB** | Topic Knowledge Base (one per topic) | Everything for the topic, taught from zero in simple English (§5). |
| **TnQA** | Topic Question Answers (one per topic) | A model answer to **every** past descriptive question of the topic, including every short-note part, in the Prediction Paper format (§6–§7). |
| **FB** | The Fact Book — for law, call it **The Law Book** | Reference tables (§8). |
| **QA** | The Question Answers — compiled | All topics' model answers in one volume, with an index of questions by year (`@py qa_master_index`, `@include … :: Tn`, `@toc 1-1`, `compress: yes`). |
| **OL** | The One-Liner and MCQ Bank | Every one-liner, every past MCQ and new practice MCQs (§9). |
| **RN** | The Revision Notes | The whole subject for the last three weeks (§10). |
| **PR** | The Prediction Papers — Sets 1–3 | Three complete papers in exact FPSC format, with model answers (§11). |

**Order of work:**
1. MA.
2. Then **one topic at a time**: KB, then QA, then the feeders (`oneliners.gsm`, `rn_sheet.gsm`, `rn_figs.gsm`, `rn_plans.gsm`, `RN.gsm`, `facts.gsm`, `qa_eye.gsm`).
3. Then FB, compiled QA, OL, RN and PR — each only when I ask.

**"One thing at a time"** is a standing instruction. Do only the volume I ask for. Do not propagate changes into other volumes without asking first, and offer such changes at the end.

---

## 3. Topic design

- **Group the syllabus heads into topics** (about 6–9), as Gender Studies grouped 9 heads into 7 topics.
- Use the record to group them. Heads that are always asked together belong together, and heavy statutes may need a topic of their own.
- Keep `data/topics.py` as the single source of truth: number, title, syllabus heads, colour, budget.
- For each topic, the record must show:
  - visits (full question = 1, short-note part = ½);
  - MCQ count;
  - question families and repeats;
  - blind spots (syllabus lines never asked);
  - what is "due".
- **Likely statutes.** Confirm all of this against the uploaded syllabus — the syllabus wins. The CSS Mercantile Law syllabus is built around Pakistan's commercial statutes. These are typically:
  - the Contract Act 1872;
  - the Sale of Goods Act 1930;
  - the Partnership Act 1932 (and the Limited Liability Partnership Act 2017, if the syllabus or contemporary layer needs it);
  - the Negotiable Instruments Act 1881;
  - the Arbitration Act 1940;
  - company law (the Companies Act 2017, which replaced the Companies Ordinance 1984);
  - possibly insurance, carriage or other heads.
  Use **only** what the syllabus lists as chapters. Put related current law in the contemporary layer, labelled as such.

---

## 4. House style (applies to every volume)

- **Language:**
  - Simple English, short sentences, one idea per sentence. Speak to the reader ("you").
  - Explain every legal term the first time, in brackets or in the next sentence, then use it precisely.
  - Latin maxims (*caveat emptor*, *nemo dat quod non habet*, *consensus ad idem*, *quantum meruit*, …) are italicised, translated and explained.
- **Law, cited exactly:**
  - Every rule carries its **statute and section** (e.g. "s. 10, Contract Act 1872") and, where useful, a **leading case** (name, year, court, principle).
  - Sections are paraphrased faithfully. Quote the statutory words only where they are short and famous.
- **Evidence inside the point.** Put law and case cards inside the heading they prove. Each ends with a `->` line saying what it proves. Use the existing `::: law` and `::: case` cards:
  - `::: law Section 2(h) | Contract Act 1872` — the rule in plain words, plus an illustration.
  - `::: case Carlill v Carbolic Smoke Ball Co | Court of Appeal, 1893` — facts, held, principle.
- **Boxes:**
  - `simple` — the idea in one breath;
  - `example` — an "A agrees with B…" illustration, in the style of the statute's own illustrations;
  - `trap` — common confusions (void vs voidable; sale vs agreement to sell; holder vs holder in due course);
  - `pakistan` — Pakistani courts, practice, SECP, banking;
  - `eye` — what the examiner rewards;
  - `debate` / `balance` — critiques and reform debates;
  - `remember` — mnemonics and lists.
- **Figures — every chapter and every answer needs them.** Use the engine's types:
  - `flow` — formation of a contract; offer → acceptance → consideration → contract; the stages of a winding up;
  - `tree` — kinds of contracts: valid / void / voidable / illegal / unenforceable;
  - `compare` — sale vs agreement to sell; bill of exchange vs cheque; partnership vs company; void vs voidable;
  - `timeline` — revocation rules (s. 5) and times of communication (s. 4);
  - `mapping` — breach → remedy → section;
  - `grid` — rights of an unpaid seller;
  - `cycle`, `pyramid`, `matrix`, `spectrum` and `bars`, where they fit.
  - Tables do not count as figures.
- **Dense headings (standing instruction).** Give as many headings as possible:
  - `### 1.` main headings;
  - `#### i)` sub-headings under nearly every main heading;
  - `##### (a)` sub-sub-headings wherever a sub-heading holds two or more points.
  - Almost no paragraph should stand without a heading above it.
- **Facts current.**
  - The cover's "Facts current to" date comes from front matter `updated:`.
  - Keep `data/facts_verified.md` with every checked fact and its source: current status of each Act, amendment years, SECP rules, recent landmark judgments.

---

## 5. Topic Knowledge Base (TnKB) — the standard

**Hard length floors (from a user complaint, "you are decreasing lengths slowly. do this carefully"):**
- KB total ≥ **22,000 words**, with a teaching core (chapters) ≥ **16,500**;
- revision sheet ≥ **3,500** counted words;
- one-liners ≥ **120**.
- Draft long. Check with `tools_wordcount.py` and top up before you build. Never let a later topic come out shorter than earlier ones.

**Parts:**
- **Part Zero — front.**
  - At-a-glance box: syllabus heads, weight, question families, what is due.
  - How to use the KB.
  - Key terms table (term, meaning, example).
  - The statutes and sections of the topic at a glance.
- **Chapters.** One per syllabus line or cluster, taught **section by section**:
  - each chapter opens with a lead naming the past questions it answers;
  - each rule has a `law` card, an `example` box (A–B illustration) and, where relevant, a `case` card;
  - add `trap` boxes for confusions and a `pakistan` box for Pakistani practice;
  - add at least one figure, a comparison table where useful, and an `eye` box giving the model structure for the past questions that chapter answers.
- **Part Two — debates and the contemporary layer.**
  - Reform debates (e.g. a new arbitration law; consumer protection; e-contracts under the Electronic Transactions Ordinance 2002; dishonoured cheques and s. 489-F PPC).
  - Recent amendments and leading recent judgments — all verified.
- **Part Three — the record.**
  - Every past question of the topic (`@py topic_questions N`).
  - Families, repeats and blind spots.
  - Five likely questions.
- **Part Four — the one-liner bank.**
  - About **120+** numbered one-liners in MCQ style, key words bold and dates highlighted.
  - Mark ones already asked "(MCQ 2019)".
  - Every past MCQ of the topic with its key (`@py mcqs_topic N`).
- **Part Five — the revision sheet** (`rn_sheet.gsm`, ≥3,500 words).
  - One `##` section per chapter.
  - Bullets of the form "**term** = meaning (s. X; *Case*, year)".
  - Each line makes complete sense on its own, and each section ends with a "**line to take**".

---

## 6. Model answers — the format for EVERY answer (TnQA, compiled QA, PR)

Follow the **Gender Studies Prediction Paper answers** exactly (`gs_build/content/PR/s1/q2.gsm` is the template), with the improvements below.

**Lengths (floors checked with `tools_wordcount.py --answer`):**
- full answers **1,100–1,400 words** of model-answer prose; floor **1,050**;
- short notes **580–650**; floor **580**.
- Draft at about 1,250 words, then top up any answer below the floor with **substance** (a section, a case, an illustration, an exception), never padding.

**Structure of each answer file (`content/Tn/qa/NN.gsm`):**

```
# Answer N · <Short title of the question> (CSS 2019)
@py question 2019-3

## The answer map
::: fig mindmap | The answer map: every branch is one numbered heading of the model answer below.
@note <the answer's thesis and verdict in 1–2 complete sentences — see §7>
@ask <the question in its own words, KEY TERMS IN CAPITALS, line 1>
@ask <line 2 if needed>
(1) <Heading 1 text>: <complete point>; <complete point>
(2) …
:::

## Decoding the question
<command words and what each demands; the limbs of the question; for a problem question, the legal ISSUES and
the sections that govern them; how to divide the time>

## The model answer
### 1. Introduction
#### i) Definition            (statutory definition with section number)
#### ii) The argument         (your answer in two or three sentences — the verdict up front)
### 2. …                       (headings taken from the question's own words)
#### i) …
##### (a) …
… at least one non-table figure besides the map …
### N. Conclusion
#### i) …  #### ii) The verdict

## Why this answer scores
- 4–6 bullets: limbs answered, sections and cases cited, figure, Pakistani practice, judgement.
```

**Content rules for law answers:**
1. **Introduction.**
   - i) the **statutory definition with its section**;
   - ii) **the argument or answer** stated up front — e.g. "The statement is correct: every contract is an agreement, but an agreement becomes a contract only when the essentials of s. 10 are present."
2. **Headings come from the question's own words.** Every limb of the question gets its own `###` heading.
3. **Every main heading carries at least one of:** a **section**, a **case**, or an **illustration** (A–B example). Cite sections in the text, e.g. "(s. 25(1))".
4. **Exceptions and qualifications** get their own sub-headings. Examiners in law reward exceptions (s. 25's three exceptions to "no consideration, no contract"; the exceptions to *nemo dat*).
5. **Problem / case-based questions** use **IRAC** as the main headings:
   - **1. The facts in short**;
   - **2. The legal issues** (one sub-heading per issue);
   - **3. The law** (sections and cases, one sub-heading per rule);
   - **4. Application** (each issue applied to the facts);
   - **5. Decision and remedies** (who wins, what remedy, under which section);
   - plus a figure — a flow of the transaction or a mapping of breach → remedy.
6. **Pakistan.** Wherever relevant, add Pakistani practice: Pakistani superior-court positions (only verified ones), SECP, banking practice, recent amendments.
7. **Conclusion** restates the verdict and, for reform-type questions, gives a way forward.
8. **At least one figure besides the answer map.** Prefer flow, compare, tree or mapping. A table may appear in addition but does not count.
9. **Short notes**:
   - same format, five or six headed points;
   - map with 5–6 branches;
   - one figure.
10. **Exact repeats** are answered once, with a `note` box at the second occurrence. Near-repeats are answered separately, so the candidate learns to re-cut knowledge.

---

## 7. The answer map — the stricter standard (the main change from Gender Studies)

**The problem to fix.** In the Gender Studies Prediction Papers, many branches were labels rather than statements: "(9) Integration and its risk: dilution", or "(1) Introduction: yes — as accountable allies, not leaders". An examiner glancing at the map could not tell what was being claimed. **From now on, the map alone must answer the question.** An examiner who reads only the map, and nothing else, must understand the full answer and its verdict.

**Rules:**
1. **`@note` states the answer, not instructions.**
   - Write it as the thesis and verdict in one or two complete sentences, with the governing section.
   - **Bad:** "Define a contract, explain its essentials and evaluate the statement."
   - **Good:** "A contract is an agreement enforceable by law (s. 2(h)); every contract is an agreement, but an agreement becomes a contract only if it has the essentials of s. 10 — so the statement is true."
2. **`@ask`** reproduces the question in its own words, with the **key terms in CAPITALS**. Use up to two lines.
3. **8–12 branches** for a full answer (5–6 for a short note).
   - Branch *n* is heading *n* of the model answer: same number, and the **title is the heading text verbatim**.
   - The last branch is the conclusion, and states the verdict.
4. **Each branch has 2–3 points, and each point is a complete, self-explanatory statement** of about 7–15 words. It carries the substance: the rule, the section or case, and the result.
   - **Never** write a bare label, a single word, "etc.", an undefined abbreviation, or a point that only makes sense after reading the answer.
5. **Problem questions:** branches follow facts → issues → law → application → decision.
   - Each point states the legal conclusion, e.g. "B may recover damages for loss arising naturally from breach (s. 73)."
6. **Engine syntax:** `(n) Title: point; point; point`.
   - The **first colon** separates the title from the points, so put no other colon in the title.
   - Separate points with semicolons, so put **no semicolons inside a point**.
   - Keep each point under about 90 characters so it wraps cleanly.
   - Check every map in the preview. If 12 branches × 3 points crowd the figure, adjust the figure's width or font in `engine/figures.py` for all maps, rather than shortening the points.
   - Make the figure text-wrapper treat "s. 29", "ss. 26–28" and "Art. 25" as unbreakable (e.g. a non-breaking space), so a section number never starts a new line on its own. Tested: a 10-branch, 2-point map of this kind fits on one page with the current engine.

**Bad branch → good branch:**

| Bad (label) | Good (complete sense) |
|---|---|
| `(4) Consideration: essential` | `(4) Lawful consideration — s. 2(d) and s. 25: Each party must give something of value in return; Without consideration an agreement is void, subject to s. 25 exceptions` |
| `(6) Exceptions` | `(6) Exceptions to "no consideration, no contract" — s. 25: A registered written promise made out of natural love and affection binds; A promise to compensate a past voluntary service binds; A written promise to pay a time-barred debt binds` |
| `(9) Minor's agreement: void` | `(9) A minor's agreement is void from the beginning: Mohori Bibee v Dharmodas Ghose (1903) held it void, not voidable; Money advanced to a minor on a mortgage cannot be recovered` |
| `(12) Conclusion` | `(12) Conclusion — the statement is true: Every contract rests on an agreement of offer and acceptance; Only agreements meeting all s. 10 essentials are enforceable as contracts` |

**A complete example map** (for "Define a contract. 'All contracts are agreements but all agreements are not contracts.' Discuss."):

```
::: fig mindmap | The answer map: every branch is one numbered heading of the model answer below.
@note A contract is an agreement enforceable by law (s. 2(h), Contract Act 1872); every contract begins as an agreement, but only an agreement with all the essentials of s. 10 is enforceable — so the statement is true.
@ask DEFINE a CONTRACT. "ALL CONTRACTS ARE AGREEMENTS but ALL AGREEMENTS ARE NOT CONTRACTS."
@ask DISCUSS with reference to the ESSENTIALS of a valid contract.
(1) Introduction — a contract is an enforceable agreement: Section 2(h) defines a contract as an agreement enforceable by law; Contract = agreement + enforceability, so the statement holds
(2) What an agreement is — s. 2(e): Every promise or set of promises forming consideration is an agreement; An accepted proposal becomes a promise under s. 2(b)
(3) Why every contract is an agreement: No contract can arise without offer and acceptance between parties; Enforceability is added to an agreement, never created without one
(4) Why every agreement is not a contract: Social and domestic agreements lack intention to create legal relations; Balfour v Balfour (1919) — a husband's allowance promise was not enforceable
(5) Essential 1 — free consent of competent parties: Parties must be of majority age and sound mind (s. 11); Consent must be free of coercion, undue influence, fraud and mistake (s. 14)
(6) Essential 2 — lawful consideration and object: Consideration and object must not be forbidden, fraudulent or immoral (s. 23); Without consideration the agreement is void, subject to s. 25 exceptions
(7) Essential 3 — not expressly declared void: Agreements in restraint of marriage, trade or legal proceedings are void (ss. 26–28); Wagering agreements are void under s. 30
(8) Essential 4 — certainty and possibility: Vague terms make an agreement void (s. 29); An agreement to do an impossible act is void (s. 56)
(9) Agreements that fall short: Void agreements have no legal effect from the start; Voidable contracts bind until the aggrieved party rescinds them (s. 2(i))
(10) Conclusion — the statement is true: Agreement is the genus and contract the species; Only agreements meeting all s. 10 essentials become enforceable contracts
:::
```

---

## 8. The Law Book (FB)

Front matter, plus these tables. Mark volatile items ★ and refresh them just before finalising.
1. **Master timeline** of the statutes and amendments, with years.
2. **Section index**: every important section → its rule in one line → topic.
3. **Case index**: case, court, year, principle, topic. Only verified cases.
4. **Definitions index**: statutory definitions with sections.
5. **Latin maxims**: maxim, translation, meaning, where used.
6. **Comparison tables**: void/voidable/illegal; sale/agreement to sell; bill/note/cheque; partnership/LLP/company; arbitration/litigation.
7. **Remedies map**: breach → remedy → section.
8. **Numbers and periods**: time limits, notice periods, minimum members.
9. **Per-topic sections**: `@include ../Tn/facts.gsm` under "# Topic n ·" headings.

---

## 9. The One-Liner and MCQ Bank (OL)

Structure:
- How to use;
- the objective paper (`@py mcq_table`, `@py mcq_weights`, what the record shows, a technique flow figure, a trap box, an anchor-sections box);
- then per topic:
  - `## The one-liners` (`@include ../Tn/oneliners.gsm`);
  - `## The past MCQs, with answers` (`@py mcqs_quiz n`);
  - `## Practice MCQs, with answers` (`@include practice_Tn.gsm`).

**MCQ format (user instruction):**
- After each MCQ comes its four options, **none of them bold**.
- **Then, on a separate line straight after, the correct answer in bold**, followed by a one-line reason:
  `Ans: ^^Answer: (C) Thirty days^^ — s. X allows …`
- There is no separate key section.
- Practice MCQs are written in `content/OL/src/Tn.txt` (`Q:` / `A:` / `K:` format). `make_ol.py` balances the key letters across A–D.
  - Write 30–38 per topic, on facts no past MCQ has asked.
  - Include some "None of these" and "Both A and B" keys.
- Explanations of past keys go in `content/OL/src/past_notes.txt` (`YEAR.N | note`). Flag doubtful published keys honestly.
- Check with the PDF that no stem is split from its options or its answer across a page break.

---

## 10. The Revision Notes (RN)

- **Front matter:**
  - how to use (cover, recall, check);
  - a topics table;
  - a **three-week timetable**;
  - "The Paper at a Glance": weights, heat map, time plan, the frame of a scoring answer, the **due list**, and a **cross-topic links** table (e.g. "free consent" from the Contract Act reused in sale, partnership and arbitration agreements).
- **Per topic** (`content/Tn/RN.gsm`):
  - glance box;
  - `@include rn_sheet.gsm`;
  - `@include rn_figs.gsm` — **four key diagrams** redrawn simply, each followed by "**Draw it in:**" naming the past questions it serves, with years checked against the record;
  - `@include rn_plans.gsm` — an answer plan for **every** past question.

---

## 11. The Prediction Papers (PR)

- **Three complete papers**, each rendered by `engine/fpsc.py` from `content/PR/setN.txt`. Adapt the subject line to **MERCANTILE LAW**.
- Each paper is an exact replica of the FPSC paper:
  - the Roll Number box and the four-line heading;
  - the TIME ALLOWED / TOTAL MARKS lines;
  - the printed NOTE;
  - Part-I: Q. No. 1, twenty MCQs, "(20×1=20)";
  - Part-II: Q. No. 2–8, attempt any four, "(20)" at the right margin, short notes "(10+10)".
- **Check the uploaded past papers** for FPSC's actual wording, option lettering and any problem-question layout, and match them. Keep the option lettering consistent across the MA appendix, the OL and the PR.
- **The sets:**
  - **Set 1** — the most probable paper.
  - **Set 2** — difficult: about **70% difficult, 30% medium**, in both the MCQs and Part II. Record the split in a `%%` comment.
  - **Set 3** — mixed.
- Every set covers Topic 1 and the heaviest topics. Across the sets, every blind spot and the contemporary layer must appear. Include **problem (case-based) questions** in proportion to the record.
- **After each paper:**
  - "Part I Explained" (`@py pr_mcq_answers N`), with the answer in bold after each MCQ;
  - then a model answer to **every** Part-II item, including **all** short notes of an "any TWO" question, in the §6–§7 format.
- **Front matter:**
  - how to use;
  - "How the Papers Were Set": a table giving the topic and the reason for every item;
  - topic coverage bars;
  - a blind-spot coverage table.
- **Layout checks:** Part-II must fit on its page or break cleanly with Q. No. 8 kept together, and no "**********" line may sit alone on a page.

---

## 12. Legal accuracy — non-negotiable

1. **Never invent a section number, a case, a citation, a date or a holding.**
   - Verify sections against the statute text, preferably the official Pakistan Code (pakistancode.gov.pk), the SECP for company law, or the Act's PDF.
   - Record each verification in `data/facts_verified.md`.
2. **Cases:**
   - Use the established leading cases taught in Pakistani and South Asian law courses: English, Indian and Pakistani cases whose names, years and principles you can confirm.
   - Cite a Pakistani reporter citation (PLD / SCMR / CLC / YLR) **only if verified**. Otherwise give the case name and principle without a citation, or state the principle without a case.
3. **Currency:**
   - Check whether each Act is still in force and what has amended it (e.g. the Companies Act 2017 replaced the Companies Ordinance 1984).
   - Say so where the syllabus names an older law.
4. **Where authorities differ, or the law is unsettled**, say so in a `balance` box and give the defensible position.
5. **Web access:** some news sites block fetching. Use search summaries, or download PDFs and extract the text (fitz / pymupdf).

---

## 13. Process rules learned in the Gender Studies build (follow all)

- **Floors are floors.**
  - Answers ≥1,050 (notes ≥580) by `--answer` count.
  - KB ≥22,000 (core ≥16,500); sheet ≥3,500; one-liners ≥120.
  - Draft long; top up with substance; recount before every build.
- **One thing at a time.** Finish, verify and deliver one volume, then stop and wait.
- **After building each volume:**
  1. Run `python3 build.py CODE`, then `python3 preview.py CODE`.
  2. Look at several preview sheets, including the cover, contents, a figure page, an answer map and the last page.
  3. Scan the PDF for split MCQs, orphan headings and cropped figures.
  4. Fix what you find.
  5. Update `ml_build/SPEC.md` (status row and lessons).
  6. Commit with a clear message, push, and send me the .docx with SendUserFile.
- **Large volumes:**
  - Use `compress: yes` in the front matter if a .docx approaches **30 MB** (the file-send limit).
  - Use `@toc 1-1` for long compiled volumes.
- **Tables:** the header row must not start with an empty cell.
- **Tree sub-items** are indented with two spaces (`  - `).
- **`compare` is a figure** (`::: fig compare | …`), not a box.
- **Mindmap `@note` wraps automatically**, so keep it to two sentences.
- **Lists in boxes** use `1.` / `- ` lines.
- **Wording:**
  - Never write "obviously" or "simply".
  - Never quote a line unless its wording is established.
  - Avoid filler; every sentence carries a rule, a reason, an example or a judgement.
- **Report honestly.**
  - If a check fails or a fact cannot be verified, say so and soften or remove the claim.
  - At the end of each volume, list anything uncertain.

---

## 14. Per-answer checklist (run before accepting any answer)

1. Does the **map alone** answer the question, with a verdict in `@note` and the last branch?
2. Is every branch title identical to its numbered heading, with 2–3 complete-sense points each?
3. Does the answer have all four sections — question box, map, decoding, model answer — plus "Why this answer scores"?
4. Does every limb of the question have its own `###` heading?
5. Are the headings dense: `i)` under nearly every `###`, and `(a)` wherever a sub-heading holds two or more points?
6. Does every main heading carry a section, case or illustration, and are all of them verified?
7. Do exceptions have their own sub-headings?
8. Is there at least one figure besides the map?
9. Is there a Pakistani angle where relevant?
10. Are there 1,050–1,400 words (notes 580–650) by `tools_wordcount.py --answer`?

---

## 15. Your first reply in this session

Do §1 steps 1–7, then reply with:
1. the papers and MCQ sheets recovered, by year, and anything missing;
2. the syllabus heads, exactly as printed;
3. your proposed topic grouping, with visits and MCQ counts per topic, and the reasoning;
4. the volume plan and the order of work;
5. any adaptation of the engine you intend: subject name, colours, the FPSC subject line, map width for longer points.

Then wait for my approval before writing the Master Anatomy.
