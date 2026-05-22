---
name: foundation-question-gen
description: Use this skill to generate English assessment questions for the English Foundation course.
---

# English Foundation — Question Generation Guide

## About This Course

English Foundation is the first level of the English programme. It covers the basics of Parts of Speech, Verbs, Pronouns, Adjectives, Articles, Prepositions, Conjunctions, and Tenses. All topics use the Grammar & Vocabulary skill, except the two Real Time Session topics which use the Writing skill.

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

### Module 1 — Parts of Speech

Topic 1 — Noun Vs Main Verb
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 2 — Noun: Number and Collection
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Sentence Conversion

Topic 3 — Countable and Uncountable Nouns
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

---

### Module 2 — Verbs and Pronouns

Topic 4 — Verb Forms and Noun + Helping Verb Agreement
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 5 — Possessive Noun: Apostrophe and Of Form
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 6 — Pronouns: People and Things
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 7 — Possessive Pronouns
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

---

### Module 3 — Adjectives and Articles

Topic 8 — Real Time Session 1
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 9 — Adjectives: Identification, Application and Degree
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 10 — Articles: A / An and The
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

---

### Module 4 — Prepositions and Question Words

Topic 11 — Prepositions
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 12 — Question Words
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 13 — Adverbs
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

---

### Module 5 — Conjunctions and Tenses

Topic 14 — Real Time Session 2
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 15 — Contractions and Interjections
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 16 — Conjunctions
Skill: Grammar & Vocabulary | Marks: 3 | Types: Fill in the blanks, Sentence arrangement, Sentence Conversion

Topic 17 — Tenses Possession
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

---

### Module 6 — Present Simple

Topic 18 — Present Simple 1
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 19 — Present Simple 2
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 20 — Present Simple 3
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Jumbled Sentences

Topic 21 — Present Simple 4
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 22 — Present Simple: Scenario Application
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Sentence Conversion

---

### Module 7 — Past Simple

Topic 23 — Past Simple 1
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 24 — Past Simple 2
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 25 — Past Simple 3
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Jumbled Sentences

Topic 26 — Past Simple 4
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 27 — Past Simple: Scenario Application
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Sentence Conversion

---

## Difficulty Targets Per Topic

Each topic generates questions across three difficulty levels.

For Grammar & Vocabulary topics: Easy 10, Medium 15, Hard 5
For Writing topics (Real Time Sessions): Easy 5, Medium 10, Hard 5

---

## Sample Questions CSV Format

The file sample_questions_template.csv in this folder shows the correct format.

Each row has these columns in order:
skill, marks, question_type, difficulty, text, answer_key, option_a, option_b, option_c, option_d, bloom_level

Lines starting with # are comments and are skipped.
Bloom level: 1 = Remember, 2 = Understand, 3 = Apply, 4 = Analyse, 5 = Evaluate, 6 = Create

---

## Excel Output Columns

The generated Excel file has one question per row with these columns:

Course, Module, Topic, Skill, Marks, Question Type, Difficulty, Bloom Level, Question Text, Answer Key, Option A, Option B, Option C, Option D, Validation Status

Approved questions are highlighted green. Rejected questions are highlighted red.
