# 🤖 Insta Automation Pro (2026)

Production-grade Instagram automation engine built on `instagrapi` with enterprise-level session management, proxy rotation, anti-detection pacing, and modular task execution.

## ⚠️ Legal & Safety Notice
This tool interacts with Instagram's **private/unofficial API**. Automation violates Instagram's Terms of Service. Use responsibly, limit actions, rotate sessions, and maintain backups. The developers assume no liability for account suspensions.

---

## 🚀 Features
- ✅ Secure 2FA login with session persistence
- ✅ Post photos, carousels, reels, and stories
- ✅ Auto-like, comment, follow/unfollow with smart delays
- ✅ Scrape followers, following, hashtags, locations, competitors
- ✅ Multi-account support with proxy injection
- ✅ Anti-detection: request jitter, device fingerprint rotation, rate limiting
- ✅ `.env` + `config.json` configuration
- ✅ Docker-ready, modular, logging & retry logic built-in

> **Note on "Mouse/Typing" Anti-Detection**: Private API automation does not render a browser UI, making mouse/typing simulation irrelevant. This project instead implements **request-level humanization** (timing jitter, pacing, header rotation, session integrity) which is the actual vector Instagram uses for bot detection.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+ or Docker
- Instagram account (backup/recommended)
- Residential or high-quality 4G proxies (datacenter IPs get flagged quickly)

### 2. Local Installation
```bash
git clone https://github.com/your-org/insta-automation-pro.git
cd insta-automation-pro
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and config.json with your credentials & limits
python -m src.main
```

### 3. Docker
```bash
cp .env.example .env
docker compose up -d
docker compose logs -f insta-bot
```

---

## ⏱️ Rate Limits & Safety Guidelines (2026 Meta Baseline)

| Action                | Safe Limit/Hour | Max/Day | Notes                                  |
|-----------------------|-----------------|---------|----------------------------------------|
| Likes                 | 100-150         | 500     | Spread evenly, avoid bursts            |
| Follows               | 20-40           | 200     | High-risk action; warm up first        |
| Comments              | 30-50           | 150     | Use natural, varied text               |
| Posts (Feed)          | 3-5             | 10      | Space out 30-60min                     |
| Stories               | 10-20           | 100     | Add tags/location for engagement       |
| API Requests          | ~200/min        | N/A     | Internal pacing enforced automatically |

### 🔒 Anti-Ban Checklist
- [ ] Use residential proxies (`socks5://` or `http://user:pass@host:port`)
- [ ] Enable 2FA on accounts
- [ ] Never run multiple accounts on the same IP/device fingerprint simultaneously
- [ ] Start with 20-30% of max limits, scale slowly over 7-10 days
- [ ] Rotate session files weekly
- [ ] Avoid spammy captions or identical comment templates
- [ ] Monitor `logs/automation.log` for `ChallengeRequired` or `LoginRequired`

---

## 📁 Project Structure
See repository tree at the top. All logic is modular under `src/`.

- `client.py`: Core wrapper with 2FA, proxy, session management
- `poster.py`: Media handling with type validation
- `actions.py`: Engagement with rate tracking
- `scraper.py`: Data extraction with CSV export
- `scheduler.py`: Cron-like task runner
- `utils.py`: Logging, delays, retry logic, action tracker

---

## 🔄 Updates & Maintenance
Instagram updates its private API frequently. To update:
1. Pull latest `instagrapi` version
2. Run tests in staging account
3. Clear `sessions/` if login breaks
4. Update `user_agent_pool` in `config.json` with latest Instagram app signatures

---

## 📜 License
MIT. Use at your own risk. Respect creator platforms and avoid spam.
