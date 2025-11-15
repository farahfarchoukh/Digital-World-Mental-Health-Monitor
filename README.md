# Digital-World-Mental-Health-Monitor
An automated, server‑less Python pipeline for early‑warning of population‑level psychological distress – aligned with UN SDG 3 (Good Health &amp; Well‑Being) Author: Farah Farchoukh | Program: IT Automation with Python - Google Scholarship

# Digital‑World Mental‑Health Monitor
## A pure‑Python IT‑automation capstone (UN SDG 3 – Good Health & Well‑Being)

### What it does
- Pulls public **Twitter** and **Reddit** posts containing mental‑health keywords.
- Cleans, de‑duplicates, and stores them locally.
- Scores each post with a **hybrid VADER + DistilBERT** model.
- Produces a **daily risk aggregate** (average score, post count).
- Sends a **Slack/E‑mail alert** when a statistically‑significant spike is detected.

### Why it’s an IT‑automation project
- All steps are **scripted**, **repeatable**, and **scheduled** with a single `schedule.sh` (or Windows `run_all.bat`).  
- No manual copy‑pasting of API responses, no hand‑crafted Excel sheets, and **zero human error** in the data‑pipeline.  
- ROI is measured in **minutes saved per run** (≈ 3 min vs. ≈ 30 min manual work) and **error reduction** (automated deduplication, language filtering, and deterministic scoring).

### Prerequisites
| Item | Version |
|------|---------|
| Python | 3.11 |
| pip | latest (`python -m pip install --upgrade pip`) |
| OS | Linux/macOS/Windows (any) |
| Slack workspace | (optional – for alerts) |
| Twitter Academic API token | (free for students) |
| Reddit app credentials | (free) |

### Installation
```bash
git clone https://github.com/farahfarchoukh/Digital-World-Mental-Health-Monitor.git
cd Digital-World-Mental-Health-Monitor
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Digital-World-Mental-Health-Monitor/
│
├─ .github/
│   └─ workflows/
│       └─ ci.yml                 # Lint + pytest (unchanged)
│
├─ data/                           # local storage – CSV/JSON files
│   ├─ raw/                        # raw Twitter & Reddit JSON blobs (saved by collector)
│   ├─ cleaned/                    # cleaned CSV files
│   └─ db/                         # SQLite DB (optional) – holds scored rows & aggregates
│
├─ src/
│   ├─ collector/
│   │   ├─ twitter_collector.py   # writes JSON to data/raw/
│   │   └─ reddit_collector.py    # writes JSON to data/raw/
│   │
│   ├─ cleaning/
│   │   └─ clean.py               # de‑dup, language filter → CSV in data/cleaned/
│   │
│   ├─ scoring/
│   │   ├─ vader_score.py
│   │   ├─ bert_score.py          # optional – loads a local .pt model
│   │   ├─ combine_score.py
│   │   └─ score_posts.py         # reads cleaned CSV, writes to SQLite table `scored`
│   │
│   ├─ aggregation/
│   │   └─ aggregate.py           # creates daily aggregates in SQLite, writes CSV for reporting
│   │
│   ├─ alert/
│   │   └─ send_alert.py          # reads aggregates, fires Slack/E‑mail if thresholds breached
│   │
│   └─ orchestrator.py            # top‑level script that calls the above steps in order
│
├─ tests/
│   ├─ test_collector.py
│   ├─ test_clean.py
│   └─ test_scoring.py
│
├─ docs/
│   ├─ architecture.png           # updated diagram (local‑file‑system flow)
│   ├─ model_roc.png
│   ├─ slack_alert.png
│   └─ dashboard.png
│
├─ requirements.txt
├─ README.md
├─ LICENSE
└─ schedule.sh                    # simple cron wrapper (Linux/macOS) or run_all.bat (Windows)
