```markdown
## Environment Variables
| Name | Required | Example |
|-------------|----------|-------------------|
| `API_ID` | Yes | `123456` |
| `API_HASH` | Yes | `0123456789abcdef0123456789abcdef` |
| `BOT_TOKEN` | Yes | `12345:AA...` |
| `ALLOWED_CHATS` | No | `-1001234567890,-1009876543210` |

## Local Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export API_ID=123
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token
# optional
export ALLOWED_CHATS=-1001234567890
python -m app.main
```

## Deploy to Google Cloud Run (Console)
1. **Create Artifact Repository (one-time)**
- In Google Cloud Console: *Artifact Registry* → *Create repository* → Format: Docker.

2. **Build & Push via Cloud Build**
```bash
gcloud builds submit --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/tg-voicechat-invite-panel-bot:latest"
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy tg-voicechat-invite-panel-bot \
--image "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/tg-voicechat-invite-panel-bot:latest" \
--platform managed \
--region ${REGION} \
--min-instances 0 \
--max-instances 1 \
--allow-unauthenticated \
--set-env-vars API_ID=123,API_HASH=your_api_hash,BOT_TOKEN=your_bot_token,ALLOWED_CHATS=-1001234567890
```

> Cloud Run will keep the container running; the bot makes an outbound connection to Telegram. No HTTP server is required.

## GitHub Repo Setup
```bash
# Initialize repo locally
mkdir tg-voicechat-invite-panel-bot && cd $_
# Place the files from this repository structure here
git init
git add .
git commit -m "Initial commit: voice chat invite panel bot"
# Create a new repository on GitHub named tg-voicechat-invite-panel-bot, then:
git remote add origin https://github.com/<your-username>/tg-voicechat-invite-panel-bot.git
git branch -M main
git push -u origin main
```

## Bot Permissions
- The bot must be **added to the group** where voice chat invites happen.
- It does **not** need admin rights to send the panel. If you want it to delete other messages, grant *Delete Messages*. It can delete **its own** panel without admin.

## Notes
- Telegram represents voice/video chat events as service messages. We listen for `filters.video_chat_members_invited` (Pyrogram) to get inviter and invited users.
- If you don't see any panels, ensure that such invites actually occur in the group and that the bot can see service messages (privacy mode off in @BotFather if needed).
