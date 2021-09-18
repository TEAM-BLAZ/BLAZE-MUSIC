import traceback
import asyncio
from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery, ChatPermissions

from cache.admins import admins
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from handlers.play import cb_admin_check
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues
from config import LOG_CHANNEL, OWNER_ID, BOT_USERNAME, COMMAND_PREFIXES
from helpers.database import db, dcmdb, Database
from helpers.dbtools import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from helpers.helper_functions.admin_check import admin_check
from helpers.helper_functions.extract_user import extract_user
from helpers.helper_functions.string_handling import extract_time


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

# Back Button
BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="cbback")]])

@Client.on_message(filters.text & ~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()


@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("ᗷᴏᴛ **ᖇᴇʟᴏᴀᴅᴇ !🤩**\n\n😉**ᗩdmin ᒪist** has been **updated **")


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "**Oᴘᴇɴᴇᴅ ᗰᴜꜱɪᴄ ᑭʟᴀʏᴇʀ ᗰᴇɴᴜ!☢️☢️**\n\n**👉 ᑎɪᴄʜʜᴇ ᗪɪʏᴇ ᘜʏᴇ ᗷᴜᴛᴛᴏɴs Տᴇ ᗩᴀᴘ ᗰᴜsɪᴄ ᑕᴏɴᴛʀᴏʟ Kʀ Տᴋᴛᴇ ᕼᴀɪɴ..😉**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ ᑭᴀᴜꜱᴇ", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ ᖇᴇꜱᴜᴍᴇ", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ Տᴋɪᴘ", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ ᗴɴᴅ", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⛔ ᗩɴᴛɪ ᑕᴍᴅꜱ", callback_data="cbdelcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰ᘜʀᴘꜱ Tᴏᴏʟꜱ", callback_data="cbgtools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 ᑕʟᴏꜱᴇ", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("I'ᴍ ᑭʟᴀʏɪɴɢ Տᴏɴɢ...?😶!")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ ᑭᴀᴜꜱᴇᴅ 😌!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ᗩɴʏᴛʜɪɴɢ ᑭᴀᴜꜱᴇᴅ ?")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ ᖇᴇꜱᴜᴍᴇᴅ!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text(" Տᴀʙ ᗰᴏʜᴀ ᗰᴀʏᴀ ᕼᴀɪɴ..ᗰᴀɪɴ ᑎʜɪ ᑭʟᴀʏ Kʀᴜ ᘜᴀ 😉🤪")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ ᗴɴᴅ ᗷʏ ᗷʟᴀᴢᴇ")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("ᑎʜɪ ᑕʜᴀʟ ᖇʜᴀ 😫😭")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⫸ Տᴋɪᴘ : **{skip[0]}**\n⫸ ᑎᴏᴡ ᑭʟᴀʏɪɴɢ...😒 : **{qeue[0][0]}**")


@Client.on_message(command("auth") & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply(" ᖇᴇᴘʟʏ Tᴏ ᗩ ᑌꜱᴇʀ Tᴏ ᗩᴜᴛʜ!..🕯️🕯️")
        return
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("🟢 ᑎᴏᴡ Տᴏᴏɴ ᗩᴜᴛʜᴏʀɪᴢᴇᴅ.\n\n ᑎɪᴋʟ ᗰᴏᴊ ᗰᴀʀ 🤭.")
    else:
        await message.reply("✅ᑎᴏᴡ ᗩᴜᴛʜᴏʀɪᴢᴇᴅ..🤗🤗")


@Client.on_message(command("deauth") & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("❗ ᖇᴇᴘʟʏ Tᴏ ᗩ ᗰᴇꜱꜱᴀɢᴇ Oꜰ Tʜᴇ ᑌꜱᴇʀ...😬")
        return
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("ᗪᴇᴀᴜᴛʜᴏʀɪᴢᴇᴅ Տᴜᴄᴄᴇꜱꜱ...🤮")
    else:
        await message.reply("ᗰᴏᴊ ᕼᴏɢɪ Tᴇʀɪ TO...🤣🤣🤣 #ᑎɪᴋᴀʟ 🤣")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("ᖇᴇᴀᴅ /help ᗰᴇꜱꜱᴀɢᴇ Tᴏ Kɴᴏᴡ ᕼᴏᴡ Tᴏ ᑌꜱᴇ Tʜɪꜱ ᑕᴍᴅꜱ😗")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("✅ ᗩʟʀᴇᴀᴅʏ ᗩᴄᴛɪᴠᴀᴛᴇᴅ")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text(
                "🟢 ᗩᴄᴛɪᴠᴀᴛᴇᴅ "
            )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 ᗪɪꜱᴀʙʟᴇ Տᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ")
    else:
        await message.reply_text(
            "ᖇᴇᴀᴅ /help ᗰᴇꜱꜱᴀɢᴇ Tᴏ Kɴᴏᴡ ᕼᴏᴡ Tᴏ ᑌꜱᴇ Tʜɪꜱ ᑕᴍᴅꜱ"
        )


# music player callbacks (control by buttons feature)

@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
            ):
        await query.edit_message_text("❗️ ᑎothing Is ᑭlaying", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text("▶️ ᗰusic Is ᑭaused", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
            ):
        await query.edit_message_text("❗️ ᑎothing Is ᑭaused", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text("⏸ ᗰusic Is ᖇesumed", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗️ ᑎothing Is ᑭʟaying", reply_markup=BACK_BUTTON)
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass
        
        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text("✅ THE MUSIC QUEUE HAS BEEN CLEARED AND SUCCESSFULLY LEFT VOICE CHAT", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗️ NOTHING IS PLAYING", reply_markup=BACK_BUTTON)
    else:
        queues.task_done(query.message.chat.id)
        
        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )
            
    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(f"⏭ SKIPPED MUSIC\n\n» SKIPPED : **{skip[0]}**\n» NOW PLAYING : **{qeue[0][0]}**", reply_markup=BACK_BUTTON)

# (C) Veez Music Project

# ban & unban function

@Client.on_message(filters.command("ban", COMMAND_PREFIXES))
@authorized_users_only
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.kick_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ successfully banned "
                f"{user_first_name}"
                " from this group...🤗🤣"
            )
        else:
            await message.reply_text(
                "✅ banned "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " from this group...🤥"
            )


@Client.on_message(filters.command("tban", COMMAND_PREFIXES))
@authorized_users_only
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "the specified time type is invalid. "
                "use m, h, or d, format time: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.kick_member(
            user_id=user_id,
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ temporarily banned "
                f"{user_first_name}"
                f" ,banned for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "✅ temporarily banned "
                f"<a href='tg://user?id={user_id}'>"
                "from this group !"
                "</a>"
                f" ,banned for {message.command[1]}!"
            )

@Client.on_message(filters.command(["uban", "umute"], COMMAND_PREFIXES))
@authorized_users_only
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ ok accepted, user "
                f"{user_first_name} can"
                " join to this group again!"
            )
        else:
            await message.reply_text(
                "✅ ok, now "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> is not"
                " restricted again...😏 "
            )

@Client.on_message(filters.command("mute", COMMAND_PREFIXES))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ okay,🏻 "
                f"{user_first_name}"
                " successfully muted !"
            )
        else:
            await message.reply_text(
                "🏻✅ okay, "
                f"<a href='tg://user?id={user_id}'>"
                "now is"
                "</a>"
                " muted !"
            )


@Client.on_message(filters.command("tmute", COMMAND_PREFIXES))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "The specified time type is invalid. "
                "use m, h, or d, format time: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Muted for a while! "
                f"{user_first_name}"
                f" muted for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Muted for a while! "
                f"<a href='tg://user?id={user_id}'>"
                "is"
                "</a>"
                " now "
                f" muted, for {message.command[1]}!"
            )
