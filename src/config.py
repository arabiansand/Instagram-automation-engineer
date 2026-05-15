import json
import os
from pathlib import Path
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class AntiDetectionConfig(BaseModel):
    request_jitter_min_ms: int = 200
    request_jitter_max_ms: int = 1500
    rotate_device_every_sessions: int = 5
    user_agent_pool: List[str] = []

class ActionsConfig(BaseModel):
    like_delay_min_sec: float = 3.5
    like_delay_max_sec: float = 12.0
    comment_delay_min_sec: float = 8.0
    comment_delay_max_sec: float = 25.0
    follow_delay_min_sec: float = 15.0
    follow_delay_max_sec: float = 45.0
    max_likes_per_hour: int = 120
    max_follows_per_hour: int = 30
    max_comments_per_hour: int = 40
    auto_unfollow_inactive_days: int = 14

class PostingConfig(BaseModel):
    story_hashtags: List[str] = []
    carousel_min_items: int = 2
    carousel_max_items: int = 10
    reel_max_duration_sec: int = 90

class SchedulerConfig(BaseModel):
    run_every_minutes: int = 60
    enabled_modules: List[str] = ["actions", "scraper"]

class AppConfig(BaseModel):
    accounts: List[Dict[str, str]] = []
    actions: ActionsConfig = Field(default_factory=ActionsConfig)
    posting: PostingConfig = Field(default_factory=PostingConfig)
    anti_detection: AntiDetectionConfig = Field(default_factory=AntiDetectionConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)

def load_config() -> AppConfig:
    cfg_path = BASE_DIR / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    # Override with .env if present
    raw["env_override"] = {
        "proxy": os.getenv("PROXY_URL"),
        "username": os.getenv("IG_USERNAME"),
        "password": os.getenv("IG_PASSWORD")
    }
    return AppConfig(**raw)
