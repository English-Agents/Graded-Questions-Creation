# Cloze Question Eval — Complete Setup Guide

## Files You Receive

You will receive a zip folder containing these 5 files. Keep all of them in the same folder.

| File | Purpose |
|---|---|
| `GUIDE.md` | This guide |
| `promptfooconfig.yaml` | Eval configuration |
| `prompt.txt` | AI validator instructions |
| `eval_tests.yaml` | 5 valid Cloze questions (should all pass) |
| `testing_tests.yaml` | 5 flawed Cloze questions (should all fail) |

---

## Step 1 — Install VS Code

1. Go to https://code.visualstudio.com
2. Click **Download for Windows**
3. Run the installer with default settings
4. Open VS Code after installation

---

## Step 2 — Install Node.js

1. Go to https://nodejs.org
2. Download the **LTS** version
3. Run the installer with default settings
4. **Restart your computer** after installation

Verify — open VS Code terminal (`Ctrl + `` ` ``) and run:
```
node --version
npm --version
```
Both should show a version number like `v20.x.x`.

---

## Step 3 — Open the Eval Folder in VS Code

1. Extract the zip folder you received
2. Open VS Code
3. Click **File → Open Folder**
4. Select the extracted folder
5. You should see all 5 files in the left sidebar

---

## Step 4 — Get a FREE API Key (Groq)

This eval uses **Groq** — it is completely free, no credit card required.

1. Go to https://console.groq.com
2. Click **Sign Up** (you can sign in with Google)
3. Click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Give it any name and click **Submit**
6. Copy the key — it starts with `gsk_...`

---

## Step 5 — Create Your .env File

1. In VS Code, open the eval folder
2. Click **File → New File**
3. Save it as `.env` (exactly this name, with the dot) inside the eval folder
4. Type this inside:

```
OPENAI_API_KEY=paste-your-groq-key-here
```

Replace `paste-your-groq-key-here` with the key you copied from Groq.

Example:
```
OPENAI_API_KEY=gsk_abc123xyz...
```

5. Save the file (`Ctrl + S`)

---

## Step 6 — Open Terminal in VS Code

1. In VS Code, go to **Terminal → New Terminal** (or `Ctrl + `` ` ``)
2. The terminal should already be inside your eval folder
3. If not, type:
```
cd path\to\your\eval\folder
```

---

## Step 7 — Run the Eval

```
npx promptfoo eval --env-file .env
```

- First run downloads promptfoo automatically (~30 seconds)
- Then runs all 10 test cases
- Results appear in the terminal

Expected output:
```
Running 10 test cases...
Results:
  10 passed (100%)
  0 failed (0%)
  0 errors (0%)
```

---

## Step 8 — View Results in Browser

```
npx promptfoo view --yes
```

Opens your browser at `http://localhost:15500`:
- **Green** = PASS
- **Red** = FAIL
- Click any cell to see the full AI response and reasoning

---

## What the Eval Tests

### Eval Dataset — 5 Valid Questions (`eval_tests.yaml`)

Correctly formed Cloze questions. AI should say **VALID** for all.

| # | Scenario | Difficulty |
|---|---|---|
| 1 | Consultant sales data analysis | Hard |
| 2 | Hospital patient-record system | Medium |
| 3 | City council traffic patterns | Hard |
| 4 | Auditor company accounts | Hard |
| 5 | University curriculum review | Medium |

Each question has:
- A passage with exactly 4 blanks (i–iv)
- Each blank offers one noun form and one verb form in brackets
- A correct answer key
- A grammatical explanation

---

### Testing Dataset — 5 Flawed Questions (`testing_tests.yaml`)

Intentionally broken questions. AI should say **INVALID** for all.

| # | Scenario | Flaw |
|---|---|---|
| 1 | Legal team contract review | Answer key reversed — verbs where nouns needed, nouns where verbs needed |
| 2 | Museum restoration project | Blanks (ii) and (iv) have no verb option — both choices are nouns |
| 3 | Research team observation | Blanks (ii) and (iv) are ambiguous — both options are correct verbs |
| 4 | Engineer bridge inspection | Word-order error in blank (iv) — object placed before verb |
| 5 | Company safety training | Blank (ii) uses non-finite verb (preparing) instead of finite verb (prepared) |

---

## Validation Criteria

The AI checks every question against 6 rules:

| # | Rule | What it checks |
|---|---|---|
| 1 | **Structure** | Exactly 4 numbered blanks (i–iv) with two bracket options each |
| 2 | **Option types** | Each blank must have one noun form AND one verb form |
| 3 | **Answer key accuracy** | Selected answer must be grammatically correct in context |
| 4 | **Uniqueness** | Only one unambiguous correct answer per blank |
| 5 | **Grammar** | Passage must be free of sentence-structure or word-order errors |
| 6 | **Key reversal** | Nouns fill noun positions, verbs fill verb positions |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Missing OPENAI_API_KEY` | Check `.env` file exists and has the correct key |
| `node: command not found` | Install Node.js from nodejs.org and restart computer |
| `Cannot find module` | Run `npm install -g promptfoo` then try again |
| Browser doesn't open | Go to `http://localhost:15500` manually |
| All 10 tests show errors | Check internet connection and Groq API key |
