# GA Question Generator

An AI-powered tool that generates English assessment questions from reading material, supporting four courses across Foundation, Advanced, Applied, and Language Analytics levels. The tool produces questions aligned to Bloom's Taxonomy levels and Course Outcomes, with a full review workflow and Google Sheets tracking.

---

## What This Tool Does

1. Select a **Course → Module → Topic** and **Question Type** from the top bar.
2. Set difficulty and question count per level — Bloom's K-levels are automatically distributed based on the Course Outcome.
3. Generate questions using Claude (via OpenRouter) grounded in the topic's reading material and sample reference questions.
4. **Review each question** — approve it or reject it with a feedback note.
5. **Download as Excel** — approved questions in the main sheet, rejected/reviewed questions in a separate Feedback sheet.
6. **Log to Google Sheets** — track all generated questions across sessions in a live dashboard with charts.

---

## Prerequisites

| Tool | Version | Download |
|---|---|---|
| Python | 3.10 or 3.11 | https://www.python.org/downloads/ |
| Node.js | 18 LTS or newer | https://nodejs.org/ |

> During Python installation, tick **"Add Python to PATH"**.

Verify in PowerShell:
```powershell
python --version   # Python 3.10.x or 3.11.x
node --version     # v18.x or newer
npm --version
```

---

## First-Time Setup

Open **PowerShell** and run the following steps in order.

### Step 1 — Navigate to the project folder
```powershell
cd D:\GA
```

### Step 2 — Create a Python virtual environment
```powershell
py -3.10 -m venv backend\venv
```

### Step 3 — Activate the virtual environment
```powershell
backend\venv\Scripts\Activate.ps1
```

You will see `(venv)` at the start of the prompt. If you get an error about scripts being disabled:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try Step 3 again.

### Step 4 — Install Python packages
```powershell
pip install -r backend\requirements.txt
```
This takes 2–5 minutes. Wait until it finishes.

### Step 5 — Install frontend packages
```powershell
cd D:\GA\frontend
npm install
cd D:\GA
```

### Step 6 — Set your OpenRouter API key

Open `D:\GA\.env` in Notepad and set:
```
OPENROUTER_API_KEY=sk-or-v1-...your-key-here...
```

Get a key at https://openrouter.ai — create an account, add credits, and copy the API key.

> The `.env` file is private. Never share it or commit it to version control.

---

## Running the App

The app requires **two terminals** open at the same time.

### Terminal 1 — Backend (FastAPI)

```powershell
cd D:\GA
backend\venv\Scripts\python.exe -m uvicorn backend.api_server:app --reload --port 8000
```

Leave this running. You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 — Frontend (React + Vite)

```powershell
cd D:\GA\frontend
npm run dev
```

Open your browser and go to:
```
http://localhost:5173
```

Press **Ctrl + C** in either terminal to stop it.

---

## Using the App

### Selection Bar (top of page)

| Field | Description |
|---|---|
| **Course** | Foundation / Advanced / Applied / Language Analytics |
| **Module / Unit** | Module within the selected course |
| **Topic** | Specific topic — a ⚠ icon means no reading material is loaded yet |
| **Question Type** | See the full list below |
| **CO badge** | Auto-derived from the module number, or loaded from an uploaded syllabus |

### Question Types

Fill in the Blanks · Cloze · Error Correction · Sentence Arrangement · Jumbled Sentences · Jumbled Words · Sentence Conversion · Sentence Correction / MCQ

### Generating Questions

Once a module and question type are selected, the **Generation Panel** appears with three difficulty sections: Easy, Medium, and Hard.

- Set the number of questions per difficulty level.
- Click **Generate** on any difficulty row to generate for that level.
- Use **Generate for Module** (when a module has multiple topics) to generate questions for every topic in one pass — all results appear in the same pool.

Bloom's K-levels (K1–K6) are distributed automatically per question based on the CO number:
- Lower COs (CO1, CO2) emphasise K1–K3 (Remember, Understand, Apply)
- Higher COs (CO4, CO5) emphasise K4–K6 (Analyse, Evaluate, Create)

### Pool — Review Workflow

All generated questions appear in a scrollable pool. Each question shows:
- Question text, solution, and explanation
- Bloom level (K1–K6), difficulty badge, and topic label (for module-level generations)

**Actions per question:**
- **Approve** — mark the question as accepted
- **Reject** — mark as rejected and optionally type a feedback note
- Filter the pool by All / Pending / Approved / Rejected using the tab bar at the top

Questions persist in the pool when you switch topics within the same module. The pool resets when you change module or course.

### Optimizer

After reviewing questions, the **⚡ Optimize** button (shown when there are reviewed questions) submits feedback to the backend and adds approved questions as few-shot examples for future generations.

### Download Excel

Click **Download Excel (N)** in the top bar (N = count of non-rejected questions).

The downloaded `.xlsx` file has two sheets:

**Sheet 1 — Generated Questions**
| Column | Description |
|---|---|
| Q No. | Question number |
| Module No. | Module number extracted from the module ID |
| Bloom Level | K1–K6 per question |
| Difficulty | Easy / Medium / Hard |
| Course Outcome | CO associated with this generation |
| Module Name | Full module display name |
| Topic | Topic name |
| Question | Full question text |
| Solution | Correct answer |
| Explanation | Grammatical / contextual explanation |

**Sheet 2 — Feedback** *(only if questions were rejected or reviewed with notes)*
| Column | Description |
|---|---|
| Q No. | Question number |
| Module Name | Module |
| Topic | Topic |
| Difficulty | Easy / Medium / Hard |
| Bloom Level | K1–K6 |
| Question | Full question text |
| Solution | Correct answer |
| Status | rejected / approved |
| Feedback Note | Reviewer's comment |

Rows are colour-coded: light red for rejected, light green for approved-with-feedback.

---

## Syllabus Upload

Upload a course syllabus (PDF, DOCX, or TXT) to enable CO descriptions, unit names, and recommended question types per topic.

1. Click **Upload Syllabus** in the top bar.
2. Select the course and upload the file.
3. The LLM extracts the structure — units, CO definitions, topic names, and recommended question types.
4. Once uploaded, the CO badge in the selection bar shows the full CO description, and the Syllabus button changes to **✓ Syllabus**.

Syllabus files are stored under `D:\GA\syllabi\<course_id>.json`.

---

## Google Sheets Dashboard

The dashboard logs all generated questions to a Google Sheets spreadsheet and shows live progress charts.

### First-time Google Sheets setup

1. Click **📊 Dashboard** in the top bar.
2. Click **Sign in with Google** — a browser window opens for OAuth authorisation.
3. Sign in with your Google account. The app is in "Testing" mode, so only authorised test users can sign in.
4. After authorisation, the dashboard shows charts and a link to the spreadsheet.

> The `credentials/client_secret.json` file must be present in `D:\GA\credentials\`. This file is already set up for the project — do not delete it.

### Logging questions

Click **Log Pool to Sheets** in the dashboard header. All non-rejected questions from the current pool are appended to the Google Sheets "Questions Log" sheet, and the dashboard stats refresh automatically.

### Dashboard charts

| Chart | Type | Description |
|---|---|---|
| Review Status | Donut chart | Approved / Pending / Rejected breakdown |
| By Difficulty | Bar chart | Easy / Medium / Hard counts |
| Bloom Distribution | Horizontal bar chart | K1–K6 counts with colour gradient |
| Questions Over Time | Line chart | Questions generated per day (shown when data spans 2+ dates) |
| By Question Type | Horizontal bar chart | Count per question type |
| Module Progress | Table | Topics covered and question count per module |
| By Course | Horizontal bar chart | Count per course (shown when multiple courses are present) |

The Google Sheets file has three sheets:
- **Questions Log** — every logged question with timestamp, CO, status, and feedback
- **Feedback Log** — questions with reviewer feedback
- **Dashboard** — aggregate stats refreshed on every log

---

## Sample Questions

Click **Sample Questions** in the top bar to view the reference examples loaded for each question type. These are used as few-shot examples during generation.

### Uploading new sample questions

In the Sample Questions panel, select a question type and upload a CSV file with these columns:

```
Question, Solution, Explanation, Bloom's Level, Difficulty, CO
```

Uploaded samples are appended to `D:\GA\evals\<type>\eval_tests.yaml`.

---

## Adding Reading Material

Reading material is what the AI uses to generate questions. Each topic has a `material/` subfolder.

### To add or update material for a topic

Navigate to:
```
D:\GA\courses\<course>\<module>\<topic>\material\
```
For example:
```
D:\GA\courses\foundation\module_1\topic_1\material\
```

Place a `.md` file containing the reading text in that folder. The topic will automatically show as available (no ⚠ icon) the next time the app loads the structure.

> The more content in the material file, the more varied and grounded the generated questions will be.

---

## Folder Structure

```
D:\GA\
│
├── .env                          ← API keys (never commit this)
├── generate_questions.py         ← Core prompt builder + Bloom distribution logic
├── README.md                     ← This file
│
├── backend\
│   ├── api_server.py             ← FastAPI app (all API endpoints)
│   ├── requirements.txt          ← Python dependencies
│   ├── venv\                     ← Python virtual environment
│   └── integrations\
│       └── sheets.py             ← Google Sheets client (OAuth + logging + stats)
│
├── frontend\
│   ├── src\
│   │   ├── App.jsx               ← Main layout, selection bar, pool state
│   │   ├── components\
│   │   │   ├── PoolBuilder.jsx   ← Generation panel + review workflow
│   │   │   ├── Dashboard.jsx     ← Google Sheets dashboard with recharts
│   │   │   ├── SamplesPanel.jsx  ← Sample questions viewer + uploader
│   │   │   └── SyllabusPanel.jsx ← Syllabus upload modal
│   │   └── api\
│   │       └── client.js         ← All fetch calls to the backend
│   ├── package.json
│   └── vite.config.js            ← Proxies /api → port 8000
│
├── courses\
│   ├── foundation\
│   │   └── module_1\
│   │       └── topic_1\
│   │           ├── material\     ← .md reading material files
│   │           └── metadata.json ← topic_name, module, course, skills
│   ├── advanced\
│   ├── applied\
│   └── language_analytics\
│
├── credentials\
│   ├── client_secret.json        ← Google OAuth credentials (DO NOT commit)
│   └── token.json                ← OAuth token (auto-created after sign-in)
│
├── syllabi\                      ← Uploaded and parsed syllabus JSON files
│
├── feedback\
│   ├── feedback.jsonl            ← Reviewer feedback from the current session
│   └── feedback_archived.jsonl   ← Feedback archived after optimisation
│
└── evals\
    ├── cloze\
    │   └── eval_tests.yaml       ← Few-shot examples for Cloze
    ├── fill_in_the_blanks\
    ├── error_correction\
    ├── sentence_arrangement\
    └── (one folder per question type)
```

---

## Running Quality Checks (Evals)

Quality checks test whether generated questions meet the defined standard using **Promptfoo** and the **Nx** task runner.

```powershell
# Check a specific question type
npx nx run cloze:eval
npx nx run fill-in-the-blanks:eval
npx nx run error-correction:eval

# Run all checks at once
npx nx run-many --target=eval --all

# View results in the browser
npx nx run cloze:view
```

You can also run evals from the **Nx Console** extension in VS Code:
1. Install the **Nx Console** extension (`Ctrl+Shift+X` → search "Nx Console")
2. Click the Nx icon in the left sidebar
3. Find the question type and click **eval**

> Quality checks use the OpenRouter API and consume credits.

---

## Troubleshooting

### "API key not set in .env" warning (amber badge in top bar)
Open `D:\GA\.env` and make sure it contains:
```
OPENROUTER_API_KEY=sk-or-v1-...
```
Restart the backend after saving.

### "Credit balance too low" error
Top up at https://openrouter.ai/credits

### "Backend not running" message in the app
Start Terminal 1 (the uvicorn command) and wait for it to print `Uvicorn running on http://127.0.0.1:8000`.

### "No reading material for this topic" (⚠ icon on topic)
Add a `.md` file to `D:\GA\courses\<course>\<module>\<topic>\material\` and refresh the page.

### Google Sheets — "Error 403: access_denied"
The app is in Testing mode. Add your Google account email as an authorised test user in Google Cloud Console → APIs & Services → OAuth consent screen → Test users.

### Google Sheets — no data saved after logging
Make sure the Google Sheets API is enabled in your project: Google Cloud Console → APIs & Services → Library → search "Google Sheets API" → Enable. Then sign out and sign in again from the Dashboard.

### Frontend blank page or "cannot find module"
```powershell
cd D:\GA\frontend
npm install
npm run dev
```

### Python package errors during setup
Confirm you are using Python 3.10 or 3.11:
```powershell
python --version
```
If needed, re-create the virtual environment:
```powershell
py -3.10 -m venv backend\venv
backend\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

---

## Quick Reference

| Task | Command |
|---|---|
| Start backend | `backend\venv\Scripts\python.exe -m uvicorn backend.api_server:app --reload --port 8000` |
| Start frontend | `cd D:\GA\frontend && npm run dev` |
| Open app | `http://localhost:5173` |
| Activate venv | `backend\venv\Scripts\Activate.ps1` |
| Install Python packages | `pip install -r backend\requirements.txt` |
| Install frontend packages | `cd D:\GA\frontend && npm install` |
| Run quality check | `npx nx run cloze:eval` |
| Run all quality checks | `npx nx run-many --target=eval --all` |
