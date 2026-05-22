---
name: advanced-question-gen
description: Use this skill to generate English assessment questions for the English Advanced course.
---

# English Advanced — Question Generation Guide

## About This Course

English Advanced is the second level of the English programme. It builds on Foundation by covering Future Simple, Continuous Tenses, Modal Verbs, Perfect Tenses, Punctuation, and Writing. Most topics use Grammar & Vocabulary. Four topics use Writing for Real Time Sessions and written practice.

---

## How It Works

Each topic has two inputs and one output.

Inputs:
- Reading material — a Markdown file placed in the topic's material folder
- Sample questions — a CSV file placed in the topic's reference_questions folder

Output:
- An Excel file with generated questions, one row per question, covering Course, Module, Topic, Skill, Marks, Question Type, Difficulty, Bloom Level, Question Text, Answer Key, and Options.

---

## Complete Question Type Reference

This section lists every question type the system can generate, grouped by skill and mark value. Each topic in the map below uses a subset of these types.

Grammar and Vocabulary — 2 marks
Fill in the blanks, Error correction, Sentence arrangement, Jumbled Sentences, Sentence Conversion, Cloze

Grammar and Vocabulary — 3 marks
Fill in the blanks, Error correction, Sentence arrangement, Jumbled Sentences, Sentence Conversion, Cloze

Reading — 2 marks
Reading comprehension (higher-order: analysis, application, opinion)

Reading — 5 marks
Literal and inferential comprehension

Reading — 7 marks
Reading comprehension (choice-based, full answers)

Writing — 3 marks
Short functional writing

Writing — 5 marks
Sequencing, Story writing, Essay writing

Writing — 7 marks
Process writing / sequencing

Writing — 8 marks
Email writing, Notice writing, Report / Work report

Writing — 10 marks
Story writing (long)

Writing — 14 marks
Paragraph writing (choice-based)

---

## Module and Topic Map

### Module 1 — Future Simple

Topic 1 — Future Simple 1
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 2 — Future Simple 2
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 3 — Future Simple: Scenario Application
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Sentence arrangement

Topic 4 — Tenses Ability
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Error correction

---

### Module 2 — Continuous Tenses and Modals

Topic 5 — Real Time Session 3
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 6 — Tenses Continuous
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 7 — Scenario Application: Simple and Continuous Tenses
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Sentence arrangement

Topic 8 — Modal Verbs
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

---

### Module 3 — Perfect Tenses

Topic 9 — Present Perfect Tense
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 10 — Present Perfect Continuous Tense
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 11 — Present Perfect and Perfect Continuous Application
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Sentence arrangement

Topic 12 — Past Perfect
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 13 — Past Perfect Continuous
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 14 — Past Perfect and Past Perfect Continuous Application
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Sentence arrangement

---

### Module 4 — Future Perfect and Writing

Topic 15 — Future Perfect
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 16 — Future Perfect Continuous
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 17 — Question Making with Question Words
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Sentence Conversion, Error correction

Topic 18 — Question Making with Question Verbs
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Sentence Conversion

Topic 19 — Real Time Session 4
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 20 — Punctuation
Skill: Grammar & Vocabulary | Marks: 2 | Types: Error correction, Fill in the blanks

Topic 21 — Articulation
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 22 — Written Practice
Skill: Writing | Marks: 5 | Types: Essay writing, Story writing

Topic 23 — Conditional Sentences and Hypotheticals
Skill: Grammar & Vocabulary | Marks: 3 | Types: Fill in the blanks, Sentence Conversion, Error correction

---

## Difficulty Targets Per Topic

For Grammar & Vocabulary topics: Easy 10, Medium 15, Hard 5
For Writing topics: Easy 5, Medium 10, Hard 5

---

## Sample Questions CSV Format

The file sample_questions_template.csv in this folder shows the correct format.

Each row has these columns in order:
skill, marks, question_type, difficulty, text, answer_key, option_a, option_b, option_c, option_d, bloom_level

Lines starting with # are comments and are skipped.
Bloom level: 1 = Remember, 2 = Understand, 3 = Apply, 4 = Analyse, 5 = Evaluate, 6 = Create

---

## Excel Output Columns

Course, Module, Topic, Skill, Marks, Question Type, Difficulty, Bloom Level, Question Text, Answer Key, Option A, Option B, Option C, Option D, Validation Status

Approved questions are highlighted green. Rejected questions are highlighted red.
