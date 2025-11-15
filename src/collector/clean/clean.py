import os, json, hashlib, csv
from pathlib import Path
from langdetect import detect, DetectorFactory
import pandas as pd

DetectorFactory.seed = 0
RAW_DIR   = Path(os.getenv("RAW_DIR", "data/raw"))
CLEAN_DIR = Path(os.getenv("CLEAN_DIR", "data/cleaned"))
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def clean(event=None, context=None):
    rows = []
    for json_file in RAW_DIR.rglob("*.json"):
        payload = json.loads(json_file.read_text())
        try:
            if detect(payload["text"]) != "en":
                continue
        except Exception:
            continue
        cleaned = payload["text"].replace("\n", " ").strip()
        rows.append({
            "post_id": payload["post_id"],
            "source": payload["source"],
            "created_at": payload["created_at"],
            "clean_text": cleaned
        })
    if rows:
        df = pd.DataFrame(rows)
        out_path = CLEAN_DIR / f"cleaned_{datetime.datetime.utcnow():%Y%m%d}.csv"
        df.to_csv(out_path, index=False)
        print(f"✅ Cleaned data written to {out_path}")
    else:
        print("⚠️ No rows passed cleaning")
