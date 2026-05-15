import random
from typing import List
from instagrapi import Client
from instagrapi.exceptions import ClientError
from src.utils import logger, human_delay, tracker
from src.config import AppConfig

class AutomationActions:
    def __init__(self, client: Client, config: AppConfig):
        self.client = client
        self.config = config.actions

    def like_user_feed(self, username: str, max_likes: int = 10):
        if not tracker.increment("likes", self.config.max_likes_per_hour): return
        try:
            user_id = self.client.user_id_from_username(username)
            medias = self.client.user_medias(user_id, amount=15)
            liked = 0
            for media in medias:
                if liked >= max_likes: break
                self.client.media_like(media.pk)
                liked += 1
                logger.info(f"Liked {username}'s post")
                human_delay(self.config.like_delay_min_sec, self.config.like_delay_max_sec)
        except ClientError as e:
            logger.error(f"Like action failed: {e}")

    def comment_post(self, media_id: str, comment_text: str):
        if not tracker.increment("comments", self.config.max_comments_per_hour): return
        try:
            self.client.media_comment(media_id, comment_text)
            logger.info("Comment posted")
            human_delay(self.config.comment_delay_min_sec, self.config.comment_delay_max_sec)
        except ClientError as e:
            logger.error(f"Comment failed: {e}")

    def follow_user(self, username: str):
        if not tracker.increment("follows", self.config.max_follows_per_hour): return
        try:
            self.client.user_follow(username)
            logger.info(f"Followed {username}")
            human_delay(self.config.follow_delay_min_sec, self.config.follow_delay_max_sec)
        except ClientError as e:
            logger.error(f"Follow failed: {e}")

    def unfollow_inactive(self, username: str):
        try:
            self.client.user_unfollow(username)
            logger.info(f"Unfollowed {username}")
            human_delay(self.config.follow_delay_min_sec, self.config.follow_delay_max_sec)
        except ClientError as e:
            logger.error(f"Unfollow failed: {e}")
