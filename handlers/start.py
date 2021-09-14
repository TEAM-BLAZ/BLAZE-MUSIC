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
        f"""<b>✨ **𝐁𝐡𝐞𝐥𝐜𝐨𝐦𝐞 {message.from_user.first_name}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) 𝗮𝗹𝗹𝗼𝘄 𝘆𝗼𝘂 𝘁𝗼 𝗽𝗹𝗮𝘆 𝗺𝘂𝘀𝗶𝗰 𝗼𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝘁𝗵𝗲 𝗻𝗲𝘄 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺'𝘀 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝐩𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 𝐳𝐚𝐢𝐝!**

💡 **𝗙𝗶𝗻𝗱 𝗼𝘂𝘁 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗕𝗼𝘁'𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗻𝗱 𝗵𝗼𝘄 𝘁𝗵𝗲𝘆 𝘄𝗼𝗿𝗸 𝗯𝘆 𝗰𝗹𝗶𝗰𝗸𝗶𝗻𝗴 𝗼𝗻 𝘁𝗵𝗲 » 📚 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !**

❓ **𝗙𝗼𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗮𝗯𝗼𝘂𝘁 𝗮𝗹𝗹 𝗳𝗲𝗮𝘁𝘂𝗿𝗲 𝗼𝗳 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁, 𝗷𝘂𝘀𝘁 𝘁𝘆𝗽𝗲 /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        " ➕ ꪖᦔᦔ ꪑꫀ 𝓽ꪮ ꪗꪮꪊ𝘳 ᧁ𝘳ꪮꪊρ ➕ ", url=f"https://t.me/BLAZEMUSIC_BOT?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "ꫝꪮ᭙ 𝓽ꪮ ꪊ𝘴ꫀ ꪑꫀ 🎧", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         " ᥴꪑᦔ𝘴 🕹 ", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        " ꪮ᭙ꪀꫀ𝘳 🕵 ", url=f"https://t.me/Timesisnotwaiting")
                ],[
                    InlineKeyboardButton(
                        " 𝘴ꪊρρꪮ𝘳𝓽 ᧁ𝘳ꪮꪊρ 📣 ", url=f"https://t.me/Blaze_Support"
                    ),
                    InlineKeyboardButton(
                        " ꪮᠻᠻ𝓲ᥴ𝓲ꪖꪶ ᥴꫝꪖꪀꪀꫀꪶ 📢 ", url=f"https://t.me/THE_BLAZE_NETWORK")
                ],[
                    InlineKeyboardButton(
                        " Sρꪖꪑ G𝘳ꪮꪊρ 📡 ", url="https://t.me/BLAZE_SPAMMER")
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
                        " ᧁ𝘳ꪮꪊρ 👥 ", url=f"https://t.me/Blaze_Support"
                    ),
                    InlineKeyboardButton(
                        " ᥴꫝꪖꪀꪀꫀꪶ 📣  ", url=f"https://t.me/THE_BLAZE_NETWORK"
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
                        text=" ꫝꪮ᭙ 𝓽ꪮ ꪊ𝘴ꫀ ꪑꫀ ❓ ", callback_data=f"cbguide"
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
