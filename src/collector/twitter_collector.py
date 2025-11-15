import os, json, hashlib, datetime, requests
from pathlib import Path

BEARER_TOKEN = os.getenv("TWITTER_BEARER")
RAW_DIR      = Path(os.getenv("RAW_DIR", "data/raw/twitter"))

def collect(event=None, context=None):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.utcnow()
    prefix = RAW_DIR / f"{now:%Y/%m/%d}"
    prefix.mkdir(parents=True, exist_ok=True)

    # same query as before …
    resp = requests.get(_query_url(), headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    resp.raise_for_status()
    payload = resp.json()

    for tweet in payload.get("data", []):
        record = {
            "post_id": tweet["id"],
            "source": "twitter",
            "created_at": tweet["created_at"],
            "text": tweet["text"]
        }
        fn = prefix / f"{hashlib.sha256(tweet['id'].encode()).hexdigest()}.json"
        fn.write_text(json.dumps(record))
    print(f"✅ Collected {len(payload.get('data', []))} tweets")

