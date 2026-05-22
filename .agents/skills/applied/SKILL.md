---
name: applied-question-gen
description: "Use this skill to generate English assessment questions for the English
  Applied course. Trigger when the user mentions Applied course, wants questions
  for topics like Sentence Structure, Conjunctions, Discussion, Framing Questions,
  Passive Voice, Essay writing, or any Module 1–4 topic of the Applied programme.
  The skill uploads reading material and sample questions for a topic, calls the
  generation API, and downloads the result as an Excel file."
---

# English Applied — Question Generation Skill

This skill generates Grammar & Vocabulary and Writing assessment questions for the
**English Applied** course using topic reading material (Markdown) and reference
sample questions (CSV) as inputs. Output is an Excel (.xlsx) file.

---

## Course Map

**English Applied** — 4 Modules, 12 Topics

### Module 1 — Structure and Discussion

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 1 | Accuracy in Sentence Structure | Grammar & Vocabulary | 2 | Error correction, Sentence arrangement |
| 2 | The Language of Connection | Grammar & Vocabulary | 3 | Sentence arrangement, Sentence Conversion |
| 3 | Mastering the Art of Discussion | Writing | 5 | Essay writing, Story writing |
| 4 | Designing Clear Prompts | Writing | 3 | Short functional writing |

### Module 2 — Expression and Obligation

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 5 | Framing Effective Questions | Grammar & Vocabulary | 2 | Sentence Conversion, Fill in the blanks |
| 6 | Emphasizing Self-Expression | Writing | 5 | Essay writing, Story writing |
| 7 | Expressing Possibility and Obligation | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 8 | Rephrasing Speech Accurately | Grammar & Vocabulary | 3 | Sentence Conversion, Sentence arrangement |

### Module 3 — Communication and Fluency

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 9 | Shifting Focus in Communication | Writing | 5 | Essay writing, Story writing |
| 10 | Improving Natural Fluency | Grammar & Vocabulary | 3 | Error correction, Sentence arrangement |

### Module 4 — Advanced Writing

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 11 | Balancing Ideas Clearly | Writing | 7 | Process writing / sequencing |
| 12 | Managing Hesitation and Highlighting Key Points | Writing | 5 | Essay writing, Short functional writing |

---

## Workflow

### Step 1 — Find the topic ID

```bash
curl http://localhost:8000/api/content/topics
```

Applied course topics are seeded after Advanced course topics.

---

### Step 2 — Upload reading material

```bash
curl -X POST http://localhost:8000/api/content/material \
  -F "topic_id=<id>" \
  -F "file=@courses/applied/module_1/topic_1/material/<topic-name>.md"
```

---

### Step 3 — Upload sample questions CSV

```bash
curl -X POST http://localhost:8000/api/content/samples \
  -F "topic_id=<id>" \
  -F "file=@courses/applied/module_1/topic_1/reference_questions/sample_questions.csv"
```

---

### Step 4 — Generate questions

Grammar & Vocabulary example (2-mark):
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Grammar & Vocabulary",
    "marks": 2,
    "question_type": "Error correction",
    "difficulty": "medium",
    "count": 10
  }'
```

Writing example (5-mark):
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Writing",
    "marks": 5,
    "question_type": "Essay writing",
    "difficulty": "medium",
    "count": 5
  }'
```

Writing example (7-mark):
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Writing",
    "marks": 7,
    "question_type": "Process writing / sequencing",
    "difficulty": "medium",
    "count": 5
  }'
```

---

### Step 5 — Export to Excel

```bash
curl "http://localhost:8000/api/export/questions?topic_id=<id>" \
  -o applied_topic_<id>.xlsx
```

---

## Sample CSV Format

Column order: `skill, marks, question_type, difficulty, text, answer_key, option_a, option_b, option_c, option_d, bloom_level`

See `assets/sample_questions.csv` for a filled example.
