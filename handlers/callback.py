

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>☞.**✰ᗯᴇʟᴄᴏᴍᴇ {query.message.from_user.mention}** \n
**☞ ✰I'ᴍ ᑭʟᴀʏ ᗰᴜsɪᴄ Oɴ Tᴇʟᴇɢʀᴀᴍ ᐯᴏɪᴄᴇ ᑕʜᴀᴛ..** \n
**☞ 📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- [𝗧𝗛𝗘_𝗕𝗟𝗔𝗭𝗘_𝗡𝗘𝗧𝗪𝗢𝗥𝗞](https://t.me/THE_BLAZE_NETWORK)** \n
**☞ ✰ᖴᴏʀ ᗰᴏʀᴇ ᕼᴇʟᴘ ᑌsᴇ ᗷᴜᴛᴛᴏɴs ᗷᴇʟᴏᴡ ᗩɴᴅ ᗩʙᴏᴜᴛ ᗩʟʟ ᖴᴇᴀᴛᴜʀᴇ Oғ Tʜɪs ᗷᴏᴛ, ᒍᴜsᴛ Tʏᴘᴇ ** /help
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
                         " ☞ ᑕᴍᴅs 🕹 ", url=f"https://telegra.ph/%E1%97%B7%CA%9F%E1%B4%80%E1%B4%A2%E1%B4%87-%E1%97%B0%E1%B4%9Cs%C9%AA%E1%B4%84-%E1%97%B7%E1%B4%8F%E1%B4%9B-09-14-2"
                    ),
                    InlineKeyboardButton(
                        " ☞ Oᴡɴᴇʀ 🕵 ", url=f"https://t.me/BLAZE_OWNER")
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



@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>**✯🎼 Hello, Welcome To The Help Menu's... 🤗** </b>
**In This Menu All Commands Of This Bot Are Available Here..**
**POWERED BY•☞ ⏤͟͟͞➖⃟💫🇧ʟᴀᴢᴇ ✘🇲ᴜsɪᴄ ‌‌ﮩ٨ـﮩﮩ٨ـ**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "•☞ᗷᴀsɪᴄ ᑕᴍᴅꜱ", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "•☞ᗩᴅᴠᴀɴᴄᴇᴅ ᑕᴍᴅꜱ", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "•☞ᗩᴅᴍɪɴ ᑕᴍᴅꜱ", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "•☞Տᴜᴅᴏ ᑕᴍᴅs", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "•☞Oᴡɴᴇʀ ᑕᴍᴅꜱ", callback_data="cbowner"
                    )
                ],              
                [
                    InlineKeyboardButton(
                        " ☜• ᗷᴀᴄᴋ😉", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**『𝗕𝗔𝗦𝗜𝗖 𝗖𝗠𝗗𝗦』**

🎧 [ 𝐁𝐋𝐀𝐙𝐄 𝐌𝐔𝐒𝐈𝐂 𝐆𝐑𝐎𝐔𝐏 𝐂𝐌𝐃𝐒 ]

/play (song name) - play song from youtube
/ytp (song name) - play song directly from youtube 
/stream (reply to audio) - play song using audio file
/playlist - show the list song in queue
/song (song name) - download song from youtube
/search (video name) - search video from youtube detailed
/vsong (video name) - download video from youtube detailed
/lyric - (song name) lyrics scrapper
/vk (song name) - download song from inline mode

🎧 [ 𝐁𝐋𝐀𝐙𝐄 𝐌𝐔𝐒𝐈𝐂 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐂𝐌𝐃𝐒 ]

/cplay - stream music on channel voice chat
/cplayer - show the song in streaming
/cpause - pause the streaming music
/cresume - resume the streaming was paused
/cskip - skip streaming to the next song
/cend - end the streaming music
/admincache - refresh the admin cache
/ubjoinc - invite the assistant for join to your channel

⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>『𝗔𝗗𝗩𝗘𝗡𝗖𝗘𝗗 𝗖𝗠𝗗𝗦』</b>

/start (in group) - see the bot alive status
/reload - reload bot and refresh the admin list
/cache - refresh the admin cache
/ping - check the bot ping status
/uptime - check the bot uptime status

⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>『𝗔𝗗𝗠𝗜𝗡𝗦 𝗖𝗠𝗗𝗦』</b>

/player - show the music playing status
/pause - pause the music streaming
/resume - resume the music was paused
/skip - skip to the next song
/end - stop music streaming
/userbotjoin - invite assistant join to your group
/auth - authorized user for using music bot
/deauth - unauthorized for using music bot
/control - open the player settings panel
/delcmd (on | off) - enable / disable del cmd feature
/musicplayer (on / off) - disable / enable music player in your group
/b and /tb (ban / temporary ban) - banned permanently or temporarily banned user in group
/ub - to unbanned user you're banned from group
/m and /tm (mute / temporary mute) - mute permanently or temporarily muted user in group
/um - to unmute user you're muted in group

⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>『𝗦𝗨𝗗𝗢 𝗖𝗠𝗗𝗦』</b>

/userbotleaveall - order the assistant to leave from all group
/gcast - send a broadcast message trought the assistant
/stats - show the bot statistic

⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>『𝗢𝗪𝗡𝗘𝗥 𝗖𝗠𝗗𝗦』</b>

/stats - show the bot statistic
/broadcast - send a broadcast message from bot
/block (user id - duration - reason) - block user for using your bot
/unblock (user id - reason) - unblock user you blocked for using your bot
/blocklist - show you the list of user was blocked for using your bot


⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )




@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""     **𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧: ❓**

1⃣... First, Add Me To Your Group.
2⃣... Then Promote Me As Admin And Give All Permissions Except Anonymous Admin.
3⃣... Add @{ASSISTANT_NAME} To Your Group Or Type  /userbotjoin To Invite Her.
4⃣... Turn On The Voice Chat First Before Start To Play Music.** \n

**📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- 『ᗷʟᴀᴢᴇ ᑎᴇᴛᴡᴏʀᴋ』**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᑕᴍᴅꜱ ᒪɪꜱᴛ⚙️", callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ᑕʟᴏꜱᴇ🗑️", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
@cb_admin_check
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 here is the control menu of bot :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ ᴘᴀᴜꜱᴇ", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ ʀᴇꜱᴜᴍᴇ", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ ꜱᴋɪᴘ", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ ᴇɴᴅ", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⛔ ᴀɴᴛɪ ᴄᴍᴅ", callback_data="cbdelcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛄 ɢʀᴘ ᴛᴏᴏʟꜱ", callback_data="cbgtools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 ᴄʟᴏꜱᴇ", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbgtools"))
@cb_admin_check
@authorized_users_only
async def cbgtools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information :</b>

💡 **Feature:** this feature contains functions that can ban, mute, unban, unmute users in your group.

and you can also set a time for the ban and mute penalties for members in your group so that they can be released from the punishment with the specified time.

❔ **usage:**

1️⃣ ban & temporarily ban user from your group:
   » type `/b username/reply to message` ban permanently
   » type `/tb username/reply to message/duration` temporarily ban user
   » type `/ub username/reply to message` to unban user

2️⃣ mute & temporarily mute user in your group:
   » type `/m username/reply to message` mute permanently
   » type `/tm username/reply to message/duration` temporarily mute user
   » type `/um username/reply to message` to unmute user

📝 note: cmd /b, /tb and /ub is the function to banned/unbanned user from your group, whereas /m, /tm and /um are commands to mute/unmute user in your group.

⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information :</b>
        
**💡 Feature:** delete every commands sent by users to avoid spam in groups !

❔ usage:**

 1️⃣ to turn on feature:
     » type `/delcmd on`
    
 2️⃣ to turn off feature:
     » type `/delcmd off`
      
⚡ 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘  @THE_BLAZE_NETWORK""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbback"
                    )
                ]
            ]
        )
    )



@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""     **𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧: ❓**

1⃣... First, Add Me To Your Group.
2⃣... Then Promote Me As Admin And Give All Permissions Except Anonymous Admin.
3⃣... Add @{ASSISTANT_NAME} To Your Group Or Type  /userbotjoin To Invite Her.
4⃣... Turn On The Voice Chat First Before Start To Play Music.** \n

**📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- 『ᗷʟᴀᴢᴇ ᑎᴇᴛᴡᴏʀᴋ』**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☜• ᗷᴀᴄᴋ😉", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
