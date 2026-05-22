---
name: applied-question-gen
description: Use this skill to generate English assessment questions for the English Applied course.
---

# English Applied — Question Generation Guide

## About This Course

English Applied is the third level of the English programme. It focuses on applying language skills in practical and professional contexts — sentence accuracy, discussion, expressive writing, questioning, rephrasing, and advanced writing tasks. Topics are split between Grammar & Vocabulary and Writing.

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

### Module 1 — Structure and Discussion

Topic 1 — Accuracy in Sentence Structure
Skill: Grammar & Vocabulary | Marks: 2 | Types: Error correction, Sentence arrangement

Topic 2 — The Language of Connection
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence arrangement, Sentence Conversion

Topic 3 — Mastering the Art of Discussion
Skill: Writing | Marks: 5 | Types: Essay writing, Story writing

Topic 4 — Designing Clear Prompts
Skill: Writing | Marks: 3 | Types: Short functional writing

---

### Module 2 — Expression and Obligation

Topic 5 — Framing Effective Questions
Skill: Grammar & Vocabulary | Marks: 2 | Types: Sentence Conversion, Fill in the blanks

Topic 6 — Emphasizing Self-Expression
Skill: Writing | Marks: 5 | Types: Essay writing, Story writing

Topic 7 — Expressing Possibility and Obligation
Skill: Grammar & Vocabulary | Marks: 2 | Types: Fill in the blanks, Error correction, Sentence Conversion

Topic 8 — Rephrasing Speech Accurately
Skill: Grammar & Vocabulary | Marks: 3 | Types: Sentence Conversion, Sentence arrangement

---

### Module 3 — Communication and Fluency

Topic 9 — Shifting Focus in Communication
Skill: Writing | Marks: 5 | Types: Essay writing, Story writing

Topic 10 — Improving Natural Fluency
Skill: Grammar & Vocabulary | Marks: 3 | Types: Error correction, Sentence arrangement

Topic 11 — Enhancing Communicative Style
Skill: Writing | Marks: 5 | Types: Essay writing, Short functional writing

---

### Module 4 — Advanced Writing

Topic 12 — Balancing Ideas Clearly
Skill: Writing | Marks: 7 | Types: Process writing / sequencing

Topic 13 — Managing Hesitation and Highlighting Key Points
Skill: Writing | Marks: 5 | Types: Essay writing, Short functional writing

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
