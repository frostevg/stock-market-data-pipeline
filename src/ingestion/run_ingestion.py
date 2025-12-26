from fetch_daily import main as run_full_ingestion


def run_job() -> None:
    """
    Entry point for running the full ingestion once.
    Can be called manually, by cron, or any scheduler.
    """
    print("\n=== Starting scheduled ingestion job ===")
    run_full_ingestion()
    print("=== Ingestion job completed ===\n")


if __name__ == "__main__":
    run_job()

