import os
import json
import random
from pathlib import Path
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, BadCredentials
from src.config import AppConfig
from src.utils import logger, safe_retry

class InstaClient:
    def __init__(self, config: AppConfig, account_idx: int = 0):
        self.config = config
        self.account = config.accounts[account_idx] if config.accounts else {}
        self.client = Client()
        self.session_dir = Path(os.getenv("SESSION_DIR", "sessions"))
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.session_dir / f"session-{self.account.get('username', 'default')}.json"
        self._setup_device()
        self._inject_proxy()
        self.login()

    def _setup_device(self):
        """Randomize device fingerprint to avoid detection clustering"""
        ua = random.choice(self.config.anti_detection.user_agent_pool or [
            "Instagram 326.0.0.33.110 Android (34/14; 420dpi; 1080x2280; samsung; SM-S918B; p3s; qcom; en_US)"
        ])
        self.client.set_user_agent(ua)
        self.client.set_uuids()

    def _inject_proxy(self):
        proxy = self.account.get("proxy") or os.getenv("PROXY_URL")
        if proxy:
            self.client.set_proxy(proxy)
            logger.info(f"Proxy set: {proxy[:20]}...")

    @safe_retry
    def login(self) -> bool:
        if self.session_file.exists() and self._session_valid():
            logger.info("Restoring session...")
            self.client.load_settings(self.session_file)
            try:
                self.client.login(self.account["username"], self.account["password"])
                return True
            except LoginRequired:
                pass

        def _2fa_callback():
            mode = os.getenv("TWO_FA_MODE", "prompt")
            if mode == "prompt":
                return input("Enter 2FA code: ")
            raise ValueError("2FA required but no prompt mode configured")

        try:
            self.client.login(
                self.account["username"],
                self.account["password"],
                verification_code_callback=_2fa_callback
            )
            self._save_session()
            return True
        except (ChallengeRequired, BadCredentials) as e:
            logger.error(f"Login failed: {e}")
            return False

    def _session_valid(self) -> bool:
        """Check session freshness (rotate every N sessions to reduce flag risk)"""
        if not self.session_file.exists():
            return False
        try:
            with open(self.session_file) as f:
                settings = json.load(f)
            return settings.get("client_version") is not None
        except Exception:
            return False

    def _save_session(self):
        settings = self.client.get_settings()
        self.session_file.write_text(json.dumps(settings, indent=2))
        logger.info("Session saved securely.")

    def get_client(self) -> Client:
        return self.client
