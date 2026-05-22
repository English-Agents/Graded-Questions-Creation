---
name: foundation-question-gen
description: "Use this skill to generate English assessment questions for the English
  Foundation course. Trigger when the user mentions Foundation course, wants to generate
  questions for topics like Noun Vs Main Verb, Parts of Speech, Tenses, Articles,
  Prepositions, Conjunctions, or any Module 1–7 topic of the Foundation programme.
  The skill uploads reading material and sample questions for a topic, calls the
  generation API, and downloads the result as an Excel file."
---

# English Foundation — Question Generation Skill

This skill generates Grammar & Vocabulary and Writing assessment questions for the
**English Foundation** course using topic reading material (Markdown) and reference
sample questions (CSV) as inputs. Output is an Excel (.xlsx) file.

---

## Course Map

**English Foundation** — 7 Modules, 27 Topics

### Module 1 — Parts of Speech

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 1 | Noun Vs Main Verb | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 2 | Noun: Number and Collection | Grammar & Vocabulary | 2 | Fill in the blanks, Sentence Conversion |
| 3 | Countable and Uncountable Nouns | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |

### Module 2 — Verbs and Pronouns

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 4 | Verb Forms and Noun + Helping Verb Agreement | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 5 | Possessive Noun: Apostrophe and Of Form | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 6 | Pronouns: People and Things | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 7 | Possessive Pronouns | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |

### Module 3 — Adjectives and Articles

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 8 | Real Time Session 1 | Writing | 3 | Short functional writing |
| 9 | Adjectives: Identification, Application and Degree | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 10 | Articles: A / An and The | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |

### Module 4 — Prepositions and Question Words

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 11 | Prepositions | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 12 | Question Words | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 13 | Adverbs | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |

### Module 5 — Conjunctions and Tenses

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 14 | Real Time Session 2 | Writing | 3 | Short functional writing |
| 15 | Contractions and Interjections | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 16 | Conjunctions | Grammar & Vocabulary | 3 | Fill in the blanks, Sentence arrangement, Sentence Conversion |
| 17 | Tenses Possession | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |

### Module 6 — Present Simple

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 18 | Present Simple 1 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 19 | Present Simple 2 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 20 | Present Simple 3 | Grammar & Vocabulary | 3 | Sentence arrangement, Jumbled Sentences |
| 21 | Present Simple 4 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 22 | Present Simple: Scenario Application | Grammar & Vocabulary | 3 | Sentence arrangement, Sentence Conversion |

### Module 7 — Past Simple

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 23 | Past Simple 1 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 24 | Past Simple 2 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 25 | Past Simple 3 | Grammar & Vocabulary | 3 | Sentence arrangement, Jumbled Sentences |
| 26 | Past Simple 4 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 27 | Past Simple: Scenario Application | Grammar & Vocabulary | 3 | Sentence arrangement, Sentence Conversion |

---

## Workflow

Follow these four steps in order for each topic you want to generate questions for.

### Step 1 — Find the topic ID

```bash
curl http://localhost:8000/api/content/topics
```

Look up the `id` for the topic you want. The Foundation course topics are seeded in
the same order as the Course Map above (topic_id=1 → "Noun Vs Main Verb", etc.).

---

### Step 2 — Upload reading material

Place the topic's reading material (Markdown, PDF, DOCX, or TXT) in:
```
courses/foundation/module_N/topic_N/material/<topic-name>.md
```

Then upload it:
```bash
curl -X POST http://localhost:8000/api/content/material \
  -F "topic_id=<id>" \
  -F "file=@courses/foundation/module_1/topic_1/material/noun_vs_main_verb.md"
```

The file is chunked (512 tokens, 50-token overlap) and stored in ChromaDB for retrieval.

---

### Step 3 — Upload sample questions CSV

Use the sample CSV format at `assets/sample_questions.csv` as a reference.
Upload the file:

```bash
curl -X POST http://localhost:8000/api/content/samples \
  -F "topic_id=<id>" \
  -F "file=@courses/foundation/module_1/topic_1/reference_questions/sample_questions.csv"
```

---

### Step 4 — Generate questions

Replace the values with the correct topic_id, question_type, and difficulty:

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": 1,
    "skill": "Grammar & Vocabulary",
    "marks": 2,
    "question_type": "Fill in the blanks",
    "difficulty": "medium",
    "count": 10
  }'
```

This returns `{"job_id": "...", "status": "queued"}`.

Poll status:
```bash
curl http://localhost:8000/api/generate/<job_id>
```

---

### Step 5 — Export to Excel

```bash
curl "http://localhost:8000/api/export/questions?topic_id=<id>" \
  -o foundation_topic_<id>.xlsx
```

Or export the entire Foundation course at once:
```bash
curl "http://localhost:8000/api/export/questions" -o foundation_all.xlsx
```

---

## Sample CSV Format

The file at `assets/sample_questions.csv` shows the expected format.

Column order:
```
skill, marks, question_type, difficulty, text, answer_key,
option_a, option_b, option_c, option_d, bloom_level
```

Rows starting with `#` are treated as comments and skipped.

---

## Difficulty Distribution (Default per Topic)

| Difficulty | Target Questions |
|---|---|
| easy | 10 |
| medium | 15 |
| hard | 5 |

For Writing topics (Real Time Sessions): easy=5, medium=10, hard=5.

---

## Excel Output Columns

The generated Excel file contains these columns:

| Column | Description |
|---|---|
| Course | English Foundation |
| Module | Module name |
| Topic | Topic name |
| Skill | Grammar & Vocabulary / Writing |
| Marks | 2 or 3 |
| Question Type | Fill in the blanks / Error correction / etc. |
| Difficulty | easy / medium / hard |
| Bloom Level | K1 Remember … K6 Create |
| Question Text | The full question |
| Answer Key | Correct answer or model answer |
| Option A–D | MCQ options (if applicable) |
| Validation Status | approved / rejected / pending |

Approved questions are highlighted green; rejected questions are highlighted red.
