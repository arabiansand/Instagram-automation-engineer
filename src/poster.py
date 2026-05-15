import os
from pathlib import Path
from typing import List
from instagrapi import Client
from PIL import Image
from src.utils import logger, human_delay, safe_retry, tracker
from src.config import AppConfig

class Poster:
    def __init__(self, client: Client, config: AppConfig):
        self.client = client
        self.config = config
        self.media_dir = Path(os.getenv("MEDIA_DIR", "media"))

    @safe_retry
    def post_photo(self, image_path: str, caption: str = "") -> bool:
        if not tracker.increment("posts", 10): return False
        path = self.media_dir / image_path
        if not path.exists():
            logger.error(f"Image not found: {path}")
            return False
        try:
            self.client.photo_upload(path, caption)
            logger.info(f"Posted photo: {path.name}")
            human_delay(self.config.actions.like_delay_min_sec, self.config.actions.like_delay_max_sec)
            return True
        except Exception as e:
            logger.error(f"Photo post failed: {e}")
            return False

    @safe_retry
    def post_carousel(self, image_paths: List[str], caption: str = "") -> bool:
        paths = [self.media_dir / p for p in image_paths]
        if len(paths) < self.config.posting.carousel_min_items:
            logger.warning("Carousel requires min 2 items")
            return False
        try:
            self.client.album_upload(paths, caption)
            logger.info(f"Posted carousel ({len(paths)} items)")
            human_delay(10, 30)
            return True
        except Exception as e:
            logger.error(f"Carousel post failed: {e}")
            return False

    @safe_retry
    def post_reel(self, video_path: str, caption: str = "") -> bool:
        path = self.media_dir / video_path
        if not path.exists(): return False
        try:
            self.client.igtv_upload_video(path, title="Reel", description=caption)
            logger.info(f"Posted reel: {path.name}")
            human_delay(20, 45)
            return True
        except Exception as e:
            logger.error(f"Reel post failed: {e}")
            return False

    @safe_retry
    def post_story(self, image_path: str, hashtags: List[str] = []) -> bool:
        path = self.media_dir / image_path
        if not path.exists(): return False
        mentions = " ".join([f"#{h}" for h in hashtags or self.config.posting.story_hashtags])
        try:
            self.client.story_upload(path, caption=mentions)
            logger.info("Story posted")
            human_delay(5, 15)
            return True
        except Exception as e:
            logger.error(f"Story post failed: {e}")
            return False
