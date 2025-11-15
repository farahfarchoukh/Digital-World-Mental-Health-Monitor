import os, json, pandas as pd, requests
from datetime import datetime, timedelta

AGG_CSV = os.getenv("AGG_CSV", "data/aggregates/daily_agg.csv")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
THRESH_Z = float(os.getenv("THRESH_Z", "2"))
THRESH_SCORE = float(os.getenv("THRESH_SCORE", "0.6"))

def send(event=None, context=None):
    df = pd.read_csv(AGG_CSV)
    df["date"] = pd.to_datetime(df["date"])

    # use the last 30 days to compute running mean/std
    recent = df.tail(30)
    mu = recent["avg_score"].mean()
    sigma = recent["avg_score"].std()
    today = df.iloc[-1]

    if sigma == 0:
        print("⚠️ No variance – cannot compute Z")
        return

    z = (today["avg_score"] - mu) / sigma
    if abs(z) > THRESH_Z and today["avg_score"] > THRESH_SCORE:
        payload = {
            "date": str(today["date"].date()),
            "avg_score": round(today["avg_score"], 3),
            "z": round(z, 2)
        }
        msg = (f"*⚠️ Mental‑Health Spike*\n"
               f"*Date:* {payload['date']}\n"
               f"*Avg Score:* {payload['avg_score']} (z = {payload['z']})")
        resp = requests.post(SLACK_WEBHOOK, json={"text": msg})
        if resp.status_code != 200:
            raise RuntimeError(f"Slack webhook failed: {resp.text}")
        print("✅ Alert sent to Slack")
    else:
        print("✅ No alert today")
