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
**☞ 📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- [𝗧𝗛𝗘_𝗕𝗟𝗔𝗭𝗘_𝗡𝗘𝗧𝗪𝗢𝗥𝗞](https://t.me/THE_BLAZE_NETWORK)** \n
**☞ ✰ᖴᴏʀ ᗰᴏʀᴇ ᕼᴇʟᴘ ᑌsᴇ ᗷᴜᴛᴛᴏɴs ᗷᴇʟᴏᴡ ᗩɴᴅ ᗩʙᴏᴜᴛ ᗩʟʟ ᖴᴇᴀᴛᴜʀᴇ Oғ Tʜɪs ᗷᴏᴛ, ᒍᴜsᴛ Tʏᴘᴇ /help** 
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        " ➕ ᗩᴅᴅ ᗰᴇ Tᴏ Yᴏᴜʀ ᘜʀᴏᴜᴘ ➕ ", url=f"https://t.me/BLAZEMUSIC_BOT?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "☞ ᕼᴏᴡ Tᴏ ᑌsᴇ ᗰᴇ 🎧", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         " ☞ ᑕᴍᴅs 🕹 ", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        " ☞ Oᴡɴᴇʀ 🕵 ", url=f"https://t.me/BLAZE_MUSIC")
                ],[
                    InlineKeyboardButton(
                        " ☞ Տᴜᴘᴘᴏʀᴛ ᘜʀᴏᴜᴘ 📣 ", url=f"https://t.me/Blaze_Support"
                    ),
                    InlineKeyboardButton(
                        " ☞ Oғғɪᴄɪᴀʟ ᑕʜᴀɴɴᴇʟ 📢 ", url=f"https://t.me/THE_BLAZE_NETWORK")
                ],[
                    InlineKeyboardButton(
                        " ☞ Տᴘᴀᴍ ᘜʀᴏᴜᴘ 📡 ", url="https://t.me/BLAZE_SPAMMER")
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
                        " ☞ ᘜʀᴏᴜᴘ 👥 ", url=f"https://t.me/Blaze_Support"
                    ),
                    InlineKeyboardButton(
                        " ☞ ᑕʜᴀɴɴᴇʟ 📣  ", url=f"https://t.me/THE_BLAZE_NETWORK"
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
                        text=" ☞ ᕼᴏᴡ Tᴏ ᑌsᴇ ᗰᴇ❓ ", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 Hello {message.from_user.mention} welcome to the help menu !</b>

**in this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

⚡ __Powered by {BOT_NAME} Zaid__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᗷꪖ𝘴𝓲ᥴ ᥴꪑᦔ𝘴 ☺ ", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        " ꪖᦔꪜꪖꪀᥴꫀᦔ ᥴꪑᦔ𝘴 🤗 ", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " ꪖᦔᦔꪑ𝓲ꪀ𝘴 ᥴꪑᦔ𝘴 🖱️", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        " 𝘴ꪊᦔꪮ ᥴꪑᦔ𝘴 💡", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " ꪮ᭙ꪀꫀ𝘳 ᥴꪑᦔ𝘴📁 ", callback_data="cbowner"
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
        "🤖 ᴢᴀɪᴅ ꜱᴛᴀᴛᴜꜱ:\n"
        f"• **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"• **ꜱᴛᴀʀᴛ ᴛɪᴍᴇ:** `{START_TIME_ISO}`"
    )
