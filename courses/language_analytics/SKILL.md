---
name: language-analytics-question-gen
description: Use this skill to generate English assessment questions for the English Language Analytics course.
---

# English Language Analytics — Question Generation Guide

## About This Course

English Language Analytics is the fourth level of the English programme. It is the only course that uses all three skills — Grammar & Vocabulary, Reading, and Writing. It covers Verbal Ability, Vocabulary, Reading Comprehension, Sentence Structure, Academic Writing, and Professional Communication.

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

### Module 1 — Verbal Ability and Vocabulary

Topic 1 — Verbal Ability: Question Solving Strategies Part 1
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 2 — Real Time Session 1: Highlighting Key Points
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 3 — Vocabulary: Synonyms, Antonyms and Root Words
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 4 — Idioms, Phrases and One Word Substitutions
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 5 — Fill in the Blanks (Single and Double) and Cloze Test
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Cloze

Topic 6 — Analogy, Contextual Words and Miscellaneous Vocabulary
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

---

### Module 2 — Reading Comprehension

Topic 7 — Verbal Ability: Question Solving Strategies Part 2
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Cloze

Topic 8 — Real Time Session 2: Significance of Choosing Correct Words
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 9 — Reading Comprehension
Skill: Reading | Marks: 5 | Types: Literal and inferential comprehension

Topic 10 — Sentence (Continue the Context) and Paragraph Completion
Skill: Grammar & Vocabulary | Marks: 3 | Types: Fill in the blanks, Sentence arrangement

Topic 11 — Spot the Error and Sentence Correction
Skill: Grammar & Vocabulary | Marks: 2 | Types: Error correction

Topic 12 — Jumbled Words
Skill: Grammar & Vocabulary | Marks: 3 | Types: Jumbled Sentences

---

### Module 3 — Sentence Structure

Topic 13 — Verbal Ability: Question Solving Strategies Part 3
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction

Topic 14 — Sentence Construction
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Sentence Conversion

Topic 15 — Jumbled Sentences and Paragraphs
Skill: Grammar & Vocabulary | Marks: 3 | Types: Jumbled Sentences, Sentence arrangement

Topic 16 — Clauses
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 17 — Voice and Speech
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Error correction

Topic 18 — Spell Check
Skill: Grammar & Vocabulary | Marks: 2 | Types: Error correction

---

### Module 4 — Academic and Professional Writing

Topic 19 — Real Time Session 3: Maintaining Clarity in Delivery
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 20 — Paragraph and Essay Writing
Skill: Writing | Marks: 5 | Types: Essay writing, Sequencing

Topic 21 — Report and Summary Writing
Skill: Writing | Marks: 8 | Types: Report / Work report

Topic 22 — Academic Writing Essentials
Skill: Writing | Marks: 7 | Types: Process writing / sequencing

Topic 23 — Email and Letter Writing
Skill: Writing | Marks: 8 | Types: Email writing

---

### Module 5 — Professional Communication

Topic 24 — Mock Interviews and Group Discussions
Skill: Writing | Marks: 5 | Types: Essay writing

Topic 25 — Oral Presentations and Elevator Pitches
Skill: Writing | Marks: 5 | Types: Essay writing, Short functional writing

Topic 26 — Role-Plays for Professional Communication
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 27 — Non-Verbal Cues and Body-Language Practice
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 28 — Workplace Conversation Drills
Skill: Writing | Marks: 3 | Types: Short functional writing

Topic 29 — Resume and Cover-Letter Writing Practice
Skill: Writing | Marks: 8 | Types: Report / Work report

---

## Difficulty Targets Per Topic

For Grammar & Vocabulary topics: Easy 10, Medium 15, Hard 5
For Reading topics: Easy 5, Medium 10, Hard 5
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
