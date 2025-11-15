# Digital-World-Mental-Health-Monitor
An automated, server‑less Python pipeline for early‑warning of population‑level psychological distress – aligned with UN SDG 3 (Good Health &amp; Well‑Being) Author: Farah Farchoukh | Program: IT Automation with Python - Google Scholarship

# Digital‑World Mental‑Health Monitor

An automated, serverless Python pipeline that ingests public Twitter & Reddit posts,
scores them for mental‑health risk, aggregates daily risk per city, and sends
real‑time alerts to NGOs.  The solution is fully reproducible, runs on the
Google Cloud free tier, and aligns with UN SDG 3 Target 3.4.

## Table of Contents
1. [Architecture diagram](docs/architecture.png)
2. [Setup – Prerequisites](#setup)
3. [Running locally (Docker)](#local)
4. [Deploying to GCP](#deployment)
5. [Testing](#testing)
6. [License](#license)

---

## Setup <a name="setup"></a>

1. **Create a GCP project** and enable the following APIs:
   - Cloud Functions
   - Cloud Scheduler
   - Cloud Pub/Sub
   - Cloud Storage
   - BigQuery
   - Artifact Registry
   - Secret Manager

2. **Create a Service Account** (`capstone-sa`) and grant it the roles listed in
   `infra/terraform/main.tf`.  Download the JSON key.

3. **Create Secret Manager entries** for:
   - `TWITTER_BEARER` – your Twitter Academic API bearer token
   - `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`

4. **Clone the repository** and initialise Terraform:

```bash
git clone https://github.com/<your‑user>/mental-health-monitor.git
cd mental-health-monitor
terraform init
terraform apply -var="project_id=YOUR_GCP_PROJECT_ID"

mental-health-monitor/
├─ .github/
│   └─ workflows/
│       └─ ci.yml                # CI – lint, tests, Docker build & push
├─ infra/
│   └─ terraform/
│       ├─ main.tf               # all GCP resources (bucket, BQ, Pub/Sub, Scheduler, SA)
│       └─ variables.tf
├─ src/
│   ├─ collector/
│   │   ├─ twitter_collector.py   # pulls tweets → Cloud Storage
│   │   └─ reddit_collector.py    # pulls Reddit posts → Cloud Storage
│   ├─ clean/
│   │   └─ clean.py               # dedup, language filter, load to BQ
│   ├─ scoring/
│   │   ├─ vader_score.py         # VADER sentiment → 0‑1 score
│   │   ├─ bert_score.py          # optional DistilBERT inference
│   │   ├─ combine_score.py       # composite 0.7·VADER + 0.3·BERT
│   │   └─ score_posts.py         # batch scoring → BQ `scored` table
│   ├─ alert/
│   │   ├─ compute_alert.py       # Z‑score >2 & avg>0.6 → Pub/Sub
│   │   └─ send_alert.py          # Slack/E‑mail webhook
│   └─ dashboard/
│       └─ app.py                 # optional Streamlit UI (if you don’t use Looker)
├─ tests/
│   ├─ test_collector.py
│   ├─ test_clean.py
│   └─ test_scoring.py
├─ docs/
│   ├─ architecture.png          # Figure 1 (architecture diagram)
│   ├─ model_roc.png             # Figure 2 (ROC/PR curve)
│   ├─ slack_alert.png           # Figure 3 (alert screenshot)
│   └─ dashboard.png             # Figure 4 (Looker/Streamlit view)
├─ Dockerfile
├─ requirements.txt
├─ README.md
└─ LICENSE                      # Apache 2.0 (recommended)
