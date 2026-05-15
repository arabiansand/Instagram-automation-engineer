import logging
import random
import time
import uuid
from datetime import datetime
from typing import Callable, Any
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

logger = logging.getLogger("insta_automation")

def setup_logger(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/automation.log", encoding="utf-8")
        ]
    )

def human_delay(min_sec: float, max_sec: float) -> None:
    jitter = random.uniform(min_sec, max_sec)
    logger.debug(f"Humanizing delay: {jitter:.2f}s")
    time.sleep(jitter)

def safe_retry(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)
    return retry(
        wait=wait_random_exponential(min=2, max=15),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, KeyError))
    )(wrapper)

class ActionTracker:
    def __init__(self):
        self.counts: Dict[str, int] = {}
        self.resets: Dict[str, datetime] = {}

    def increment(self, action_type: str, limit: int) -> bool:
        now = datetime.now()
        if action_type not in self.counts or now >= self.resets.get(action_type, now):
            self.counts[action_type] = 0
            self.resets[action_type] = datetime.now().replace(hour=now.hour+1, minute=0, second=0)

        if self.counts[action_type] >= limit:
            logger.warning(f"Hourly limit reached for {action_type}. Cooling down.")
            return False
        self.counts[action_type] += 1
        return True

tracker = ActionTracker()
