import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config
from src.utils import setup_logger, human_delay, logger
from src.client import InstaClient
from src.poster import Poster
from src.actions import AutomationActions
from src.scraper import DataScraper
from src.scheduler import TaskScheduler

def run_account_pipeline():
    config = load_config()
    setup_logger(config.env_override.get("LOG_LEVEL", "INFO"))

    if not config.accounts:
        logger.error("No accounts configured in config.json")
        return

    client = InstaClient(config)
    cl = client.get_client()

    poster = Poster(cl, config)
    actions = AutomationActions(cl, config)
    scraper = DataScraper(cl)

    # Example workflow
    logger.info("Starting automation cycle...")
    
    # Scraping competitors
    if "scraper" in config.scheduler.enabled_modules:
        scraper.scrape_followers("competitor_username", limit=200)

    # Engagement
    if "actions" in config.scheduler.enabled_modules:
        actions.like_user_feed("target_niche_account", max_likes=5)
        human_delay(5, 10)

    # Posting (uncomment to enable)
    # poster.post_photo("example.jpg", "Automated post #ai #2026")

    logger.info("Cycle complete. Cooling down...")
    human_delay(30, 90)

def main():
    config = load_config()
    scheduler = TaskScheduler(config.scheduler.run_every_minutes)
    scheduler.register("full_pipeline", run_account_pipeline)
    scheduler.run_loop()

if __name__ == "__main__":
    main()
