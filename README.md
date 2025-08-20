# Telegram Voice Chat Invite Panel Bot

A Telegram bot (Pyrogram) that detects when someone **invites members to a Voice/Video Chat** in a group and posts an inline panel:

- **Inviter name**
- **List of invited users**
- **Close button**

## Setup
1. Get `API_ID` and `API_HASH` from https://my.telegram.org
2. Create a bot with @BotFather → get `BOT_TOKEN`
3. Run locally:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export API_ID=123
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token
python -m app.main
