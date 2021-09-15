from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import sudo_users_only


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


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>**☞ ✰ᗯᴇʟᴄᴏᴍᴇ {message.from_user.first_name}** \n
**☞ ✰I'ᴍ ᑭʟᴀʏ ᗰᴜsɪᴄ Oɴ Tᴇʟᴇɢʀᴀᴍ ᐯᴏɪᴄᴇ ᑕʜᴀᴛ..** \n
**☞ 📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- [ᗷʟᴀᴢᴇ](https://t.me/THE_BLAZE_NETWORK)** \n
**☞ ✰ᖴᴏʀ ᗰᴏʀᴇ ᕼᴇʟᴘ ᑌsᴇ ᗷᴜᴛᴛᴏɴs ᗷᴇʟᴏᴡ ᗩɴᴅ ᗩʙᴏᴜᴛ ᗩʟʟ ᖴᴇᴀᴛᴜʀᴇ Oғ Tʜɪs ᗷᴏᴛ, ᒍᴜsᴛ Tʏᴘᴇ /help** 
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        " ➕ ᗩᴅᴅ ᗰᴇ Tᴏ Yᴏᴜʀ ᘜʀᴏᴜᴘ ➕ ", url=f"https://t.me/BLAZEMUSIC_BOT?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "•☞ ᕼᴏᴡ Tᴏ ᑌsᴇ ᗰᴇ 🎧", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         " •☞ ᑕᴍᴅs 🕹 ", url=f"https://telegra.ph/%E1%97%B7%CA%9F%E1%B4%80%E1%B4%A2%E1%B4%87-%E1%97%B0%E1%B4%9Cs%C9%AA%E1%B4%84-%E1%97%B7%E1%B4%8F%E1%B4%9B-09-14-2"),
                
                    InlineKeyboardButton(
                        " •☞ Oᴡɴᴇʀ 🕵 ", url=f"https://t.me/BLAZE_MUSIC")
                ],[
                    InlineKeyboardButton(
                        " •☞ Տᴜᴘᴘᴏʀᴛ ᘜʀᴏᴜᴘ 📣 ", url=f"https://t.me/Blaze_Support"),
                
                    InlineKeyboardButton(
                        " •☞ Oғғɪᴄɪᴀʟ ᑕʜᴀɴɴᴇʟ 📢 ", url=f"https://t.me/THE_BLAZE_NETWORK")
                ],[
                    InlineKeyboardButton(
                        " •☞ Տᴘᴀᴍ ᘜʀᴏᴜᴘ 📡 ", url="https://t.me/BLAZE_SPAMMER")
                ],
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **ᴢᴀɪᴅ ɪꜱ ʀᴜɴɴɪɴɢ**\n<b>💠 **ᴜᴘᴛɪᴍᴇ:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " •☞ ᘜʀᴏᴜᴘ 👥 ", url=f"https://t.me/Blaze_Support")
                ],[
                    InlineKeyboardButton(
                        " •☞ ᑕʜᴀɴɴᴇʟ 📣  ", url=f"https://t.me/THE_BLAZE_NETWORK"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Hello** {message.from_user.mention()}</b>

**Please press the button below to read the explanation and see the list of available commands powered By Zaid!**

⚡ __Powered by {BOT_NAME} ᴢᴀɪᴅ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" •☞ ᕼᴏᴡ Tᴏ ᑌsᴇ ᗰᴇ❓ ", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✯🎼 Hello {message.from_user.mention} </b>

**In This Menu All Commands Of This Bot Are Available Here..**
⚡ __Powered by {BOT_NAME} Zaid__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "•☞ ᗷᴀꜱɪᴄ ᑕᴍᴅꜱ ☺ ", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "•☞ ᗩᴅᴠᴀɴᴄᴇᴅ ᑕᴍᴅꜱ 🤗 ", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "•☞ ᗩᴅᴍɪɴ ᑕᴍᴅꜱ 🖱️", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "•☞ Տᴜᴅᴏ ᑕᴍᴅꜱ 💡", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "•☞ Oᴡɴᴇʀ ᑕᴍᴅꜱ 📁 ", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " ᠻꪊꪀ ᥴꪑᦔ𝘴 🎗 ", callback_data="cbfun"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("........")
    delta_ping = time() - start
    await m_reply.edit_text(
        "╰•★★  ℘ơŋɠ ★★•╯"
        f"\n 𝘽𝙇𝘼𝙕𝙀 𝙈𝙐𝙎𝙄𝘾 𝘽𝙊𝙏 `{delta_ping * 1000:.3f} ꪑ𝘴`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 『ᗷʟᴀᴢᴇ Տᴛᴀᴛᴜs』:\n"
        f"•☞ **ᑌᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"•☞ **Տᴛᴀʀᴛ Tɪᴍᴇ:** `{START_TIME_ISO}`\n\n"
        f"•☞ **📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬** :- [𝐇𝐄𝐑𝐄](https://t.me/THE_BLAZE_NETWORK)"

    )
