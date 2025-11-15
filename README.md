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

