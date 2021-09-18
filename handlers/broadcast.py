
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from callsmusic.callsmusic import client as veez
from config import SUDO_USERS

@Client.on_message(filters.command(["gcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("Տᴛᴀʀᴛɪɴɢ ᗷʀᴏᴀᴅᴄᴀꜱᴛ ...")
        if not message.reply_to_message:
            await wtf.edit("Pʟᴢ Rᴇᴘʟʏ Tᴏ A Mᴇꜱꜱᴀɢᴇ Fᴏʀ Bʀᴏᴀᴅᴄᴀꜱᴛ!")
            return
        lmao = message.reply_to_message.text
        async for dialog in veez.iter_dialogs():
            try:
                await veez.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`Bʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ...` \n\n**SᴇɴD Tᴏ:** `{sent}` Cʜᴀᴛꜱ \n**Fᴀɪʟᴇᴅ Iɴ:** {failed} Cʜᴀᴛꜱ")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"`Gᴄᴀꜱᴛ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ..` \n\n**SᴇɴD Tᴏ:** `{sent}` Cʜᴀᴛꜱ \n**Fᴀɪʟᴇᴅ Iɴ:** {failed} Cʜᴀᴛꜱ")
