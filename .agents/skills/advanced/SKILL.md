---
name: advanced-question-gen
description: "Use this skill to generate English assessment questions for the English
  Advanced course. Trigger when the user mentions Advanced course, wants questions
  for topics like Future Simple, Continuous Tenses, Modal Verbs, Perfect Tenses,
  Punctuation, Articulation, or any Module 1–4 topic of the Advanced programme.
  The skill uploads reading material and sample questions for a topic, calls the
  generation API, and downloads the result as an Excel file."
---

# English Advanced — Question Generation Skill

This skill generates Grammar & Vocabulary and Writing assessment questions for the
**English Advanced** course using topic reading material (Markdown) and reference
sample questions (CSV) as inputs. Output is an Excel (.xlsx) file.

---

## Course Map

**English Advanced** — 4 Modules, 22 Topics

### Module 1 — Future Simple

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 1 | Future Simple 1 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 2 | Future Simple 2 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 3 | Future Simple: Scenario Application | Grammar & Vocabulary | 3 | Sentence Conversion, Sentence arrangement |
| 4 | Tenses Ability | Grammar & Vocabulary | 3 | Sentence Conversion, Error correction |

### Module 2 — Continuous Tenses and Modals

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 5 | Real Time Session 3 | Writing | 3 | Short functional writing |
| 6 | Tenses Continuous | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 7 | Scenario Application: Simple and Continuous Tenses | Grammar & Vocabulary | 3 | Sentence Conversion, Sentence arrangement |
| 8 | Modal Verbs | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |

### Module 3 — Perfect Tenses

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 9 | Present Perfect Tense | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 10 | Present Perfect Continuous Tense | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 11 | Present Perfect and Perfect Continuous Application | Grammar & Vocabulary | 3 | Sentence Conversion, Sentence arrangement |
| 12 | Past Perfect | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 13 | Past Perfect Continuous | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 14 | Past Perfect and Past Perfect Continuous Application | Grammar & Vocabulary | 3 | Sentence Conversion, Sentence arrangement |

### Module 4 — Future Perfect and Writing

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 15 | Future Perfect | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 16 | Future Perfect Continuous | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 17 | Question Making with Question Words | Grammar & Vocabulary | 2 | Fill in the blanks, Sentence Conversion, Error correction |
| 18 | Question Making with Question Verbs | Grammar & Vocabulary | 2 | Fill in the blanks, Sentence Conversion |
| 19 | Real Time Session 4 | Writing | 3 | Short functional writing |
| 20 | Punctuation | Grammar & Vocabulary | 2 | Error correction, Fill in the blanks |
| 21 | Articulation | Writing | 3 | Short functional writing |
| 22 | Written Practice | Writing | 5 | Essay writing, Story writing |

---

## Workflow

### Step 1 — Find the topic ID

```bash
curl http://localhost:8000/api/content/topics
```

Advanced course topics are seeded after Foundation (topic IDs continue from where Foundation ends).

---

### Step 2 — Upload reading material

```bash
curl -X POST http://localhost:8000/api/content/material \
  -F "topic_id=<id>" \
  -F "file=@courses/advanced/module_1/topic_1/material/<topic-name>.md"
```

---

### Step 3 — Upload sample questions CSV

```bash
curl -X POST http://localhost:8000/api/content/samples \
  -F "topic_id=<id>" \
  -F "file=@courses/advanced/module_1/topic_1/reference_questions/sample_questions.csv"
```

See `assets/sample_questions.csv` for the column format.

---

### Step 4 — Generate questions

Example for a Grammar & Vocabulary topic:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Grammar & Vocabulary",
    "marks": 2,
    "question_type": "Fill in the blanks",
    "difficulty": "medium",
    "count": 10
  }'
```

Example for a Writing topic:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Writing",
    "marks": 3,
    "question_type": "Short functional writing",
    "difficulty": "medium",
    "count": 5
  }'
```

Poll: `curl http://localhost:8000/api/generate/<job_id>`

---

### Step 5 — Export to Excel

```bash
curl "http://localhost:8000/api/export/questions?topic_id=<id>" \
  -o advanced_topic_<id>.xlsx
```

---

## Sample CSV Format

Column order: `skill, marks, question_type, difficulty, text, answer_key, option_a, option_b, option_c, option_d, bloom_level`

See `assets/sample_questions.csv` for a filled example.




