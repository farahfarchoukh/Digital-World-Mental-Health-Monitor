#!/bin/bash
# Run the whole pipeline once – you can call this from cron

export TWITTER_BEARER="YOUR_TWITTER_BEARER"
export SLACK_WEBHOOK_URL="YOUR_SLACK_WEBHOOK"
export RAW_DIR="data/raw"
export CLEAN_DIR="data/cleaned"
export DB_PATH="data/db/monitor.db"
export AGG_CSV="data/aggregates/daily_agg.csv"

python src/orchestrator.py
