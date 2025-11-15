import os, datetime
import sqlite3
import pandas as pd
from .combine_score import composite_score

CLEAN_DIR = os.getenv("CLEAN_DIR", "data/cleaned")
DB_PATH   = os.getenv("DB_PATH", "data/db/monitor.db")

def _ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS scored (
                    post_id TEXT PRIMARY KEY,
                    source TEXT,
                    created_at TEXT,
                    score REAL,
                    scored_at TEXT)""")
    conn.commit()
    return conn

def score(event=None, context=None):
    conn = _ensure_db()
    cur = conn.cursor()

    # get the latest cleaned CSV (you can keep a simple naming convention)
    latest = sorted(Path(CLEAN_DIR).glob("cleaned_*.csv"))[-1]
    df = pd.read_csv(latest)

    for _, row in df.iterrows():
        # skip if already scored
        cur.execute("SELECT 1 FROM scored WHERE post_id=?", (row["post_id"],))
        if cur.fetchone():
            continue
        s = composite_score(row["clean_text"])
        cur.execute(
            "INSERT INTO scored (post_id, source, created_at, score, scored_at) "
            "VALUES (?,?,?,?,?)",
            (row["post_id"], row["source"], row["created_at"], s,
             datetime.datetime.utcnow().isoformat())
        )
    conn.commit()
    conn.close()
    print(f"✅ Scored {len(df)} rows")
