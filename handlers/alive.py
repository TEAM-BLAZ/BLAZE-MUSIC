
from os import path

from pyrogram import Client, filters
from pyrogram.types import Message

from time import time
from datetime import datetime
from config import BOT_IMG, BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command, other_filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(filters.command(["alive", f"alive@{BOT_USERNAME}"]))
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_photo(
        photo=f"{BOT_IMG}",
        caption=f"""**╰┈➤ ᕼᴇʟʟᴏ👋..**\n**╰┈➤ ᗰʏ Տᴇʟғ {BOT_NAME}**\n\n**╰┈➤ __ᗷʟᴀᴢᴇ Is ᗯᴏʀᴋɪɴɢ__...**\n**╰┈➤ ᐯᴇʀsᴏɪɴ : 06:03.718**\n**╰┈➤ ᑌᴘᴛɪᴍᴇ : {uptime}**\n**╰┈➤ ᗰY ᗩssɪsᴛᴀɴᴛ :** __@{ASSISTANT_NAME}__\n\n**╰┈➤ 📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :『ᗷʟᴀᴢᴇ ᑎᴇᴛᴡᴏʀᴋ』**\n\n**   Tʜᴀɴᴋɪɴɢ Yᴏᴜ ᖴᴏʀ ᑌsᴇɪɴɢ Tʜɪs ᗷᴏᴛ..🤗**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏷️Ꮆʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "⌛ᑕʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )
