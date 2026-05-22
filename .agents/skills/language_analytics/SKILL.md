---
name: language-analytics-question-gen
description: "Use this skill to generate English assessment questions for the English
  Language Analytics course. Trigger when the user mentions Language Analytics course,
  wants questions for topics like Verbal Ability, Vocabulary, Reading Comprehension,
  Sentence Construction, Voice and Speech, Essay Writing, Email Writing, or any
  Module 1–5 topic of the Language Analytics programme. This course covers all
  three skills: Grammar & Vocabulary, Reading, and Writing. Output is an Excel file."
---

# English Language Analytics — Question Generation Skill

This skill generates Grammar & Vocabulary, Reading, and Writing assessment questions
for the **English Language Analytics** course using topic reading material (Markdown)
and reference sample questions (CSV) as inputs. Output is an Excel (.xlsx) file.

This is the only course that uses all three skills.

---

## Course Map

**English Language Analytics** — 5 Modules, 29 Topics

### Module 1 — Verbal Ability and Vocabulary

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 1 | Verbal Ability: Question Solving Strategies Part 1 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 2 | Real Time Session 1: Highlighting Key Points | Writing | 3 | Short functional writing |
| 3 | Vocabulary: Synonyms, Antonyms and Root Words | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 4 | Idioms, Phrases and One Word Substitutions | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 5 | Fill in the Blanks (Single and Double) and Cloze Test | Grammar & Vocabulary | 2 | Fill in the blanks, Cloze |
| 6 | Analogy, Contextual Words and Miscellaneous Vocabulary | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |

### Module 2 — Reading Comprehension

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 7 | Verbal Ability: Question Solving Strategies Part 2 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| 8 | Real Time Session 2: Significance of Choosing Correct Words | Writing | 3 | Short functional writing |
| 9 | Reading Comprehension | **Reading** | **5** | Literal & inferential comprehension |
| 10 | Sentence (Continue the Context) and Paragraph Completion | Grammar & Vocabulary | 3 | Fill in the blanks, Sentence arrangement |
| 11 | Spot the Error and Sentence Correction | Grammar & Vocabulary | 2 | Error correction |
| 12 | Jumbled Words | Grammar & Vocabulary | 3 | Jumbled Sentences |

### Module 3 — Sentence Structure

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 13 | Verbal Ability: Question Solving Strategies Part 3 | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction |
| 14 | Sentence Construction | Grammar & Vocabulary | 3 | Sentence arrangement, Sentence Conversion |
| 15 | Jumbled Sentences and Paragraphs | Grammar & Vocabulary | 3 | Jumbled Sentences, Sentence arrangement |
| 16 | Clauses | Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Sentence Conversion |
| 17 | Voice and Speech | Grammar & Vocabulary | 3 | Sentence Conversion, Error correction |
| 18 | Spell Check | Grammar & Vocabulary | 2 | Error correction |

### Module 4 — Academic and Professional Writing

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 19 | Real Time Session 3: Maintaining Clarity in Delivery | Writing | 3 | Short functional writing |
| 20 | Paragraph and Essay Writing | Writing | 5 | Essay writing, Sequencing |
| 21 | Report and Summary Writing | Writing | 8 | Report / Work report |
| 22 | Academic Writing Essentials | Writing | 7 | Process writing / sequencing |
| 23 | Email and Letter Writing | Writing | 8 | Email writing |

### Module 5 — Professional Communication

| # | Topic | Skill | Marks | Question Types |
|---|---|---|---|---|
| 24 | Mock Interviews and Group Discussions | Writing | 5 | Essay writing |
| 25 | Oral Presentations and Elevator Pitches | Writing | 5 | Essay writing, Short functional writing |
| 26 | Role-Plays for Professional Communication | Writing | 3 | Short functional writing |
| 27 | Non-Verbal Cues and Body-Language Practice | Writing | 3 | Short functional writing |
| 28 | Workplace Conversation Drills | Writing | 3 | Short functional writing |
| 29 | Resume and Cover-Letter Writing Practice | Writing | 8 | Report / Work report |

---

## Skill Reference for This Course

| Skill | Marks | Valid Question Types |
|---|---|---|
| Grammar & Vocabulary | 2 | Fill in the blanks, Error correction, Cloze |
| Grammar & Vocabulary | 3 | Fill in the blanks, Sentence arrangement, Sentence Conversion, Jumbled Sentences |
| **Reading** | **5** | Literal & inferential comprehension |
| Writing | 3 | Short functional writing |
| Writing | 5 | Essay writing, Sequencing, Story writing |
| Writing | 7 | Process writing / sequencing |
| Writing | 8 | Email writing, Report / Work report |

---

## Workflow

### Step 1 — Find the topic ID

```bash
curl http://localhost:8000/api/content/topics
```

Language Analytics topics are seeded last (after Foundation, Advanced, Applied).

---

### Step 2 — Upload reading material

```bash
curl -X POST http://localhost:8000/api/content/material \
  -F "topic_id=<id>" \
  -F "file=@courses/language_analytics/module_1/topic_1/material/<topic-name>.md"
```

---

### Step 3 — Upload sample questions CSV

```bash
curl -X POST http://localhost:8000/api/content/samples \
  -F "topic_id=<id>" \
  -F "file=@courses/language_analytics/module_1/topic_1/reference_questions/sample_questions.csv"
```

---

### Step 4 — Generate questions

Grammar & Vocabulary (2-mark):
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

Reading (5-mark — only for Topic 9: Reading Comprehension):
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Reading",
    "marks": 5,
    "question_type": "Literal & inferential comprehension",
    "difficulty": "medium",
    "count": 5
  }'
```

Writing (8-mark Email):
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": <id>,
    "skill": "Writing",
    "marks": 8,
    "question_type": "Email writing",
    "difficulty": "medium",
    "count": 5
  }'
```

Poll: `curl http://localhost:8000/api/generate/<job_id>`

---

### Step 5 — Export to Excel

By topic:
```bash
curl "http://localhost:8000/api/export/questions?topic_id=<id>" -o la_topic_<id>.xlsx
```

Entire Language Analytics course (filter by skill):
```bash
curl "http://localhost:8000/api/export/questions?skill=Reading" -o reading_questions.xlsx
curl "http://localhost:8000/api/export/questions?skill=Writing" -o writing_questions.xlsx
```

---

## Sample CSV Format

Column order: `skill, marks, question_type, difficulty, text, answer_key, option_a, option_b, option_c, option_d, bloom_level`

See `assets/sample_questions.csv` for a filled example.
