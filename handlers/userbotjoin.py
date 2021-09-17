import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from helpers.filters import command
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS


@Client.on_message(command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>MAKE ME AS ADMIN First'...😒</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: ⏤͟͟͞➖⃟🥀𓆩Bʅαȥҽ🕊️⃝❤️Assɪsᴛᴀɴᴛ Jᴏɪɴᴇᴅ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ....😊")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>HELPER ALREADY IN YOUR char</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 FLOOD WAIT ERROR 🛑 \n USER {user.first_name} COULDN'T JOINED YOUR GROUP DUE TO HEAVY JOIN REQUESTS FOR USERBOT! MAKE SURE USER IS NOT BANNED IN GROUP...."
            "\n\nOr MANUALLY ADD ASSISTANT TO YOUR GROUP AND TRY AGAIN</b>",
        )
        return
    await message.reply_text(
        "<b>USERBOT JOINED YOUR GROUP</b>",
    )


@Client.on_message(command(["userbotleave", f"userbotleave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>USER COULDN'T LEAVE YOUR GROUP! MAY BE FLOODWATERS."
            "\n\nOr MANUALLY KICK ME FROM TO YOUR GROUP</b>",
        )
        return
    
@Client.on_message(command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("ASSISTANT LEAVING ALL GROUPS")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")


@Client.on_message(command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("IS THE CHAT EVEN LINKED ?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>PROMOTE ME GROUP ADMIN FIRST...🤗</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: I JOINED HERE....")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>ASSISTANT ALREADY IN YOUR CHANNEL</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 FLOOD WAIT ERROR 🛑 \n USER {user.first_name} COULDN'T JOIN YOUR CHANNEL DUE TO HEAVY JOIN REQUESTS FOR USERBOT! MAKE SURE USER IS NOT BANNED IN CHANNEL..."
            f"\n\n AND MANUALLY ADD @{ASSISTANT_NAME} TO YOUR GROUP AND TRY AGAIN</b>",
        )
        return
    await message.reply_text(
        "<b> USERBOT JOINED YOUR CHANNEL</b>",
    )
