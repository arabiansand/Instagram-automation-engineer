import csv
from pathlib import Path
from typing import Dict, List
from instagrapi import Client
from src.utils import logger, human_delay

class DataScraper:
    def __init__(self, client: Client):
        self.client = client
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)

    def scrape_followers(self, username: str, limit: int = 500) -> List[Dict]:
        logger.info(f"Scraping followers of {username}")
        user_id = self.client.user_id_from_username(username)
        users = self.client.user_followers(user_id, amount=limit)
        self._save_csv(f"{username}_followers.csv", list(users.values()))
        return list(users.values())

    def scrape_following(self, username: str, limit: int = 500) -> List[Dict]:
        logger.info(f"Scraping following of {username}")
        user_id = self.client.user_id_from_username(username)
        users = self.client.user_following(user_id, amount=limit)
        self._save_csv(f"{username}_following.csv", list(users.values()))
        return list(users.values())

    def scrape_hashtag(self, hashtag: str, limit: int = 50) -> List[Dict]:
        logger.info(f"Scraping posts from #{hashtag}")
        medias = self.client.hashtag_medias_top(hashtag, amount=limit)
        self._save_csv(f"hashtag_{hashtag}.csv", [self._media_to_dict(m) for m in medias])
        return medias

    def scrape_location(self, location_id: str, limit: int = 50) -> List[Dict]:
        logger.info(f"Scraping posts from location {location_id}")
        medias = self.client.location_medias_top(location_id, amount=limit)
        return medias

    def _media_to_dict(self, media) -> Dict:
        return {
            "id": media.pk,
            "code": media.code,
            "likes": media.like_count,
            "comments": media.comment_count,
            "caption": getattr(media, "caption", {}).get("text", ""),
            "timestamp": media.taken_at
        }

    def _save_csv(self, filename: str, data: List[Dict]):
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            if not  return
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Saved {len(data)} records to {filepath}")
