import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from app.config import settings
from app.keyboards import CLOSE_KB

APP = Client(
    name="vc_invite_panel_bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.bot_token,
    workers=8,
    in_memory=True,
)

def in_allowed_chat(chat_id: int) -> bool:
    if settings.allowed_chats is None:
        return True
    return chat_id in settings.allowed_chats

@APP.on_message(filters.command(["start"]) & filters.private)
async def start_pm(_, m: Message):
    text = (
        "👋 Hey! I post an inline panel whenever someone invites members "
        "to a Voice/Video Chat in your group.\n\n"
        "• Add me to your group and make sure I can read messages.\n"
        "• I react to service messages of type *Video Chat Participants Invited*.\n"
        "• Use ALLOWED_CHATS env var to restrict groups (optional)."
    )
    await m.reply_text(text)

@APP.on_message(filters.video_chat_members_invited & filters.group, group=1)
async def on_vc_invites(_, m: Message):
    if not m.chat or not in_allowed_chat(m.chat.id):
        return

    inviter = m.from_user.mention if m.from_user else "Unknown"

    invited_users = []
    try:
        invited = getattr(m, "video_chat_members_invited", None)
        if invited and getattr(invited, "users", None):
            for u in invited.users:
                if u:
                    invited_users.append(u.mention)
    except Exception:
        pass

    invited_text = ", ".join(invited_users) if invited_users else "—"

    text = (
        "🎤 <b>Voice Chat Invite</b>\n\n"
        f"👤 <b>Inviter:</b> {inviter}\n"
        f"👥 <b>Invited:</b> {invited_text}"
    )

    await m.reply_text(text, reply_markup=CLOSE_KB, disable_web_page_preview=True)

@APP.on_callback_query(filters.regex(r"^close_panel$"), group=1)
async def close_panel(_, cq: CallbackQuery):
    try:
        if cq.message:
            await cq.message.delete()
        await cq.answer("Closed")
    except Exception:
        try:
            await cq.answer("Couldn't delete, but noted.", show_alert=True)
        except Exception:
            pass

@APP.on_message(filters.video_chat_started & filters.group, group=2)
async def on_vc_started(_, m: Message):
    if not in_allowed_chat(m.chat.id):
        return
    await m.reply_text("🔴 Voice/Video Chat started.")

@APP.on_message(filters.video_chat_ended & filters.group, group=2)
async def on_vc_ended(_, m: Message):
    if not in_allowed_chat(m.chat.id):
        return
    await m.reply_text("⏹️ Voice/Video Chat ended.")

async def main():
    async with APP:
        print("Bot is up and running.")
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
