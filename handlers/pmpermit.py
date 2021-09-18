from pyrogram import Client
import asyncio
from config import SUDO_USERS, PMPERMIT, OWNER_NAME, BOT_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from pyrogram import filters
from pyrogram.types import Message
from callsmusic.callsmusic import client as USER

PMSET =True
pchats = []

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    if PMPERMIT == "ENABLE":
        if PMSET:
            chat_id = message.chat.id
            if chat_id in pchats:
                return
            await USER.send_message(
                message.chat.id,
            f"👋",
            f"•**☞ HELLO I'M MUSIC ASSISTANT OF** {BOT_NAME}...\n•**☞ POWERED BY**:- @THE_BLAZE_NETWORK\n\n•**⫸** DON'T SPAM MESSAGE.....\n•**⫸** DON'T SEND ME ANYTHING CONFIDENTIAL..\n\n•**☞ JOIN HERE ..  ☟☟☟☟**\n\n•**⫸ MUSIC..** @AS_M_USIC_LOVER\n•**⫸ BLAZE OFFICIAL..** @the_blaze_network\n•**⫸ BLAZE SUPPORT..** @BLAZE_SUPPORT\n•__**⫸ •☞ If You Want I Can Join Your Group. So Send The Link Of Your Group...**__\n\n•**☞ MY BOT..** @BLAZEMUSIC_BOT",
            )
            return

    

@Client.on_message(filters.command(["/pmpermit"]))
async def bye(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        global PMSET
        text = message.text.split(" ", 1)
        queryy = text[1]
        if queryy == "on":
            PMSET = True
            await message.reply_text("✅ pmpermit turned on")
            return
        if queryy == "off":
            PMSET = None
            await message.reply_text("❎ pmpermit turned off")
            return

@USER.on_message(filters.text & filters.private & filters.me)        
async def autopmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("approved to pm due to outgoing messages")
        return
    message.continue_propagation()    
    
@USER.on_message(filters.command("yes", [".", ""]) & filters.me & filters.private)
async def pmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("✅ APPROVED TO PM...")
        return
    message.continue_propagation()    
    

@USER.on_message(filters.command("no", [".", ""]) & filters.me & filters.private)
async def rmpmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if chat_id in pchats:
        pchats.remove(chat_id)
        await message.reply_text("❌ disapproved to pm.")
        return
    message.continue_propagation()
