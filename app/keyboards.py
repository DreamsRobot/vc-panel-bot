from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CLOSE_KB = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Close", callback_data="close_panel")]]
)
