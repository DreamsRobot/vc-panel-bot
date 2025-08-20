import os
from dataclasses import dataclass

@dataclass
class Settings:
    api_id: int = int(os.environ.get("API_ID", 0))
    api_hash: str = os.environ.get("API_HASH", "")
    bot_token: str = os.environ.get("BOT_TOKEN", "")
    # Optional: restrict bot to specific chats (comma-separated IDs)
    allowed_chats: list[int] | None = None

    def __post_init__(self):
        allowed = os.environ.get("ALLOWED_CHATS", "").strip()
        if allowed:
            self.allowed_chats = [int(x) for x in allowed.split(",") if x.strip()]

settings = Settings()

# Fail-fast if missing required env vars
missing = []
if not settings.api_id:
    missing.append("API_ID")
if not settings.api_hash:
    missing.append("API_HASH")
if not settings.bot_token:
    missing.append("BOT_TOKEN")

if missing:
    raise RuntimeError("Missing required environment variables: " + ", ".join(missing))
