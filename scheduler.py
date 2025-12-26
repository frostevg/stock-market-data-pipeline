import time
import subprocess

INTERVAL_SECONDS = 60*60*24   # 24 hours; change to 60 for testing


def run_once():
    """
    Run the ingestion job once by calling the orchestrator script.
    """
    print("\n[Scheduler] Running scheduled ETL job...")
    result = subprocess.run(
        ["python", "src/ingestion/run_ingestion.py"],
        capture_output=True,
        text=True,
    )

    print("[Scheduler] Job finished with exit code:", result.returncode)
    if result.stdout:
        print("[Scheduler] STDOUT:\n", result.stdout)
    if result.stderr:
        print("[Scheduler] STDERR:\n", result.stderr)


def main():
    print("[Scheduler] Starting loop. Interval =", INTERVAL_SECONDS, "seconds.")
    while True:
        run_once()
        print(f"[Scheduler] Sleeping for {INTERVAL_SECONDS} seconds...\n")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

