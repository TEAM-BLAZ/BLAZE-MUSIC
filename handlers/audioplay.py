

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("stream") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("🔁 **ᑭʀᴏᴄᴇꜱꜱɪɴɢ....**")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Ꮆʀᴏᴜᴘ",
                        url=f"https://t.me/BLAZE_SUPPORT"),
                    InlineKeyboardButton(
                        text="ᑕʜᴀɴɴᴇʟ",
                        url=f"https://t.me/THE_BLAZE_NETWORK")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ VIDEOS LONGER THAN {DURATION_LIMIT} MINUTE(s) AREN'T ALLOWED TO PLAY...!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("Ꮆɪᴠᴇ Տᴏᴍᴇᴛʜɪɴɢꜱ ᒪɪᴋᴇ ᗩᴜᴅɪᴏ ᖴɪʟᴇꜱ ᗩɴᴅ YᴏᴜTᴜʙ ᒪɪɴᴋ...!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#⃣  Yᴏᴜʀ ᖇᴇQᴜᴇꜱᴛᴇᴅ Տᴏɴɢ Iɴ **Qᴜᴇᴜᴇ** ᗩᴛ ᑭᴏꜱɪᴛɪᴏɴ {position} !\n\n⚡ __ᑭᴏᴡᴇʀᴇᴅ ᗷʏ {bn} ᗷʟᴀᴢᴇ ᑎᴇᴛᴡᴏʀᴋ__")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"💡 **ᑎᴏᴡ ᑭʟᴀʏɪɴɢ** ᗩ Տᴏɴɢ ᖇᴇQᴜᴇᴛᴇᴅ ᗷʏ {costumer} !\n\n⚡ __ᑭᴏᴡᴇʀᴇᴅ ᗷʏ {bn} ᗷʟᴀᴢᴇ ᑎᴇᴛᴡᴏʀᴋ__"
        )
        return await lel.delete()
