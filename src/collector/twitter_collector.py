import os, json, hashlib, datetime, requests
from google.cloud import storage

BEARER_TOKEN = os.getenv("TWITTER_BEARER")
RAW_BUCKET   = os.getenv("RAW_BUCKET")
KEYWORDS = ["depressed","depression","anxiety","suicidal","hopeless","panic","stress","mental health","crying","can't cope"]

def _auth_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

def _query_url():
    q = " OR ".join(KEYWORDS) + " lang:en -is:retweet"
    return f"https://api.twitter.com/2/tweets/search/recent?query={q}&tweet.fields=created_at,author_id"

def collect(event, context=None):
    """Cloud Function entry point – fetches recent tweets and stores each as JSON."""
    now = datetime.datetime.utcnow()
    prefix = f"twitter/{now:%Y/%m/%d}"
    client = storage.Client()
    bucket = client.bucket(RAW_BUCKET)

    resp = requests.get(_query_url(), headers=_auth_headers())
    resp.raise_for_status()
    payload = resp.json()

    for tweet in payload.get("data", []):
        record = {
            "post_id": tweet["id"],
            "source": "twitter",
            "created_at": tweet["created_at"],
            "text": tweet["text"]
        }
        blob_name = f"{prefix}/{hashlib.sha256(tweet['id'].encode()).hexdigest()}.json"
        bucket.blob(blob_name).upload_from_string(
            json.dumps(record), content_type="application/json"
        )
    print(f"✅ Collected {len(payload.get('data', []))} tweets")
