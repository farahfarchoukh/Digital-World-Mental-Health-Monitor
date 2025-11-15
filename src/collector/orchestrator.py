import subprocess, os

def run_step(module, func):
    """Execute a module’s function via python -m"""
    cmd = ["python", "-m", f"src.{module}.{func}"]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    # 1. collect
    run_step("collector.twitter_collector", "collect")
    run_step("collector.reddit_collector", "collect")
    # 2. clean
    run_step("clean.clean", "clean")
    # 3. score
    run_step("scoring.score_posts", "score")
    # 4. aggregate
    run_step("aggregation.aggregate", "aggregate")
    # 5. alert
    run_step("alert.send_alert", "send")
