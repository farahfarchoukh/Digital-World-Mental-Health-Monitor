import os, datetime, sqlite3, pandas as pd

DB_PATH = os.getenv("DB_PATH", "data/db/monitor.db")
AGG_CSV = os.getenv("AGG_CSV", "data/aggregates/daily_agg.csv")

def aggregate(event=None, context=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM scored", conn)
    conn.close()

    # Ensure datetime column is a real datetime
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date
    agg = df.groupby("date").agg(
        avg_score=("score", "mean"),
        n_posts=("post_id", "count")
    ).reset_index()

    os.makedirs(os.path.dirname(AGG_CSV), exist_ok=True)
    agg.to_csv(AGG_CSV, index=False)
    print(f"✅ Daily aggregate written to {AGG_CSV}")
