import os
import json
import ffmpeg
import aiohttp
import aiofiles
import asyncio
import requests
import converter
from os import path
from asyncio.queues import QueueEmpty
from pyrogram import Client, filters
from typing import Callable
from helpers.channelmusic import get_chat_id
from callsmusic import callsmusic
from callsmusic.queues import queues
from helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
from downloaders import youtube

from config import que, THUMB_IMG, DURATION_LIMIT, BOT_USERNAME, BOT_NAME, UPDATES_CHANNEL, GROUP_SUPPORT, ASSISTANT_NAME
from helpers.filters import command, other_filters
from helpers.decorators import authorized_users_only
from helpers.gets import get_file_name, get_url
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Voice
from converter.converter import convert
from cache.admins import admins as a
from PIL import Image, ImageFont, ImageDraw

aiohttpsession = aiohttp.ClientSession()
chat_id = None
DISABLED_GROUPS = []
useer ="NaN"


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("you not allowed to do this!", show_alert=True)
            return
    return decorator                                                                       
                                          
                                                                                    
def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
        ar="48k"
    ).overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 60)
    draw.text((40, 550), f"Playing here....", (0, 0, 0), font=font)
    draw.text((40, 630),
        f"{title}",
        (0, 0, 0),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("**🔄 KOI SONG NAHIN CHAL RAHA..🤭**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**NOW PLAYING** ON {}".format(message.chat.title)
    msg += "\n• "+ now_playing
    msg += "\n• REQUESTED BY "+by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Queued Song**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n• {name}"
            msg += f"\n• Requested by {usr}\n"
    await message.reply_text(msg)
                            
# ============================= Settings =========================================
def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "ᑭʟᴀʏɪɴɢ Iɴ ᑕʜᴀᴛ **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "ᐯᴏʟᴜᴍᴇ: {}%\n".format(vol)
            stats += "ᑫᴜᴇᴜᴇ ᑎᴜᴍʙᴇʀ: `{}`\n".format(len(que))
            stats += "Տᴏɴɢ ᑎᴀᴍᴇ: **{}**\n".format(queue[0][0])
            stats += "ᑌꜱᴇʀ ᗷʏ: {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats

def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "ᒪᴇᴀᴠᴇ"),
                InlineKeyboardButton("⏸", "ᑭᴜsᴇ"),
                InlineKeyboardButton("▶️", "ᖇᴇsᴜᴍᴇ"),
                InlineKeyboardButton("⏭", "Տᴋɪᴘ")
            ],
            [
                InlineKeyboardButton("📖 ᑭʟᴀʏʟɪꜱᴛ", "playlist"),
            ],
            [       
                InlineKeyboardButton("🗑 ᑕʟᴏꜱᴇ", "cls")
            ]        
        ]
    )
    return mar


@Client.on_message(command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("PAUSE"))
            
        else:
            await message.reply(stats, reply_markup=r_ply("PLAY"))
    else:
        await message.reply("**PLEASE TURN ON THE VOICE CHAT FIRST.**")


@Client.on_message(
    command("musicplayer") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "**i'm only know** `/musicplayer on` **and** `/musicplayer off`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("`processing...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("**MUSIC PLAYER ALREADY ACTIVATED.**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"✅ ** MUSIC PLAYER HAS BEENn ACTIONvated INin THEis CHAT.**\n\n💬 {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("`processing...`")
        
        if message.chat.id in DISABLED_GROUPS:
            await LEL.EDIT("**MUSIC PLAYER ALREADY DEACTIVATED.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"✅ **MUSIC PLAYER HAS BEEN DEACTIVATED IN THIS CHAT.**\n\n💬 {message.chat.id}"
        )
    else:
        await message.reply_text(
            "**i'm only know** `/musicplayer on` **and** `/musicplayer off`"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que    
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("**nothing is playing ❗**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**NOW PLAYING** IN {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• REQUIRED BY " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "** Playlist **"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• REQUIRED BY {usr}\n"
        await cb.message.edit(msg)      


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que   
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chet_id] == "paused"
                ):
            await cb.answer("assistant is not connected to voice chat!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            
            await cb.answer("music paused!")
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("play"))
                
    elif type_ == "play":       
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chet_id] == "playing"
            ):
                await cb.answer("assistant is not connected to voice chat!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("music resumed!")
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("pause"))

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit("nothing in streaming!")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "** STARTED** Mm {}".format(cb.message.chat.title)
        msg += "\n• "+ now_playing
        msg += "\n• REQUIRED BY "+by
        temp.pop(0)
        if temp:
             msg += "\n\n"
             msg += "**Playlist**"
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style="md")
                 msg += f"\n• {name}"
                 msg += f"\n• REQUIRED BY {usr}\n"
        await cb.message.edit(msg)      
                      
    elif type_ == "resume":     
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chet_id] == "playing"
            ):
                await cb.answer("voice chat is not connected or already playing", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("music resumed!")
     
    elif type_ == "puse":         
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chet_id] == "paused"
                ):
            await cb.answer("voice chat is not connected or already paused", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            
            await cb.answer("music paused!")

    elif type_ == "cls":          
        await cb.answer("closed menu")
        await cb.message.delete()       

    elif type_ == "menu":  
        stats = updated_stats(cb.message.chat, qeue)  
        await cb.answer("menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "ᒪeave"),
                    InlineKeyboardButton("⏸", "ᑭuse"),
                    InlineKeyboardButton("▶️", "ᖇesume"),
                    InlineKeyboardButton("⏭", "Տkip")
                
                ],
                [
                    InlineKeyboardButton("📖 ᑭʟᴀʏʟɪꜱᴛ", "playlist"),
                
                ],
                [       
                    InlineKeyboardButton("🗑 ᑕʟᴏꜱᴇ", "cls")
                ]        
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":        
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("assistant is not connected to voice chat!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("• no more playlist\n• leaving voice chat")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"⫸ Տᴋɪᴘ \n⫸ ᑎᴏᴡ ᑭʟᴀʏɪɴɢ : **{qeue[0][0]}**"
                )

    elif type_ == "leave":
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("⏹ **ᗰusic Տtopped!**")
        else:
            await cb.answer("assistant is not connected to voice chat!", show_alert=True)


@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 __**RUKO JRA SABER KRO.. CHLA RHA HU...__ **")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name =  "helper"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await _.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message.from_user.id:  
                          try:
                              invitelink = await _.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "<b>**ᗰᴀᴋᴇ ᗰᴇ ᗩᴅᴍɪɴ ᖴɪʀꜱᴛ.**</b>",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message.chat.id," **       Tᴇᴀᴍ♡ᗷʟᴀᴢᴇ    \n 🤖: I'ᴍ ᒍᴏɪɴᴇᴅ Tᴏ Yᴏᴜʀ Ꮆʀᴏᴜᴘ** ")
                              await lel.edit(
                                  "<b>ᗷʟᴀᴢᴇ ᕼᴇʟᴘ ᑌsᴇʀʙᴏᴛ ᒍᴏɪɴᴇᴅ ᑌʀ ᑕʜᴀᴛ..🤗🤭</b>",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"<b>⛑ FLOOD WAIT ERROR ⛑\n{user.first_name} IS NOT IN YOUR GROUP PLEASE ADD...🥺"
                                  "\n\n& BLAZE ASSISTANT @{ASSISTANT_NAME} TRY TO ADD MANUALLY</b>",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} USERBOT NOT IN THIS CHAT, ASK ADMIN TO SEND /play COMMAND FOR FIRST TIME OR ADD {user.first_name} MANUALLY</i>"
        )
        return     
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    await lel.edit("**__SEARCHING YOUR SONG__**")
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await lel.edit("**__PROCESSING YOUR SONG__**")
    ydl_opts = {"format": "bestaudio/best"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit("SONG NOT FOUND.TRY ANOTHER SONG OR MAYBE SPELL IT PROPERLY....")
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖱 ᗰᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("🗑 ᑕʟᴏsᴇ", callback_data="cls"),
                ],[
                    InlineKeyboardButton("📣 ᑕʜᴀɴɴᴇʟ", url=f"https://t.me/THE_BLAZE_NETWORK"),
                    InlineKeyboardButton("✨ Ꮆʀᴏᴜᴘ", url=f"https://t.me/blaze_spammer")
                ],
            ]
        )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)  
    file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
        photo="final.png", 
        caption=f"#⃣ YOUR REQUESTED SONG **queued** JOIN {position}! JOIN @THE_BLAZE_NETWORK",
        reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = message.chat.id
        que[chat_id] = []
        qeue = que.get(message.chat.id)
        s_name = title            
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]      
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        except: 
            message.reply("GROUP CALL IS NOT CONNECTED OR I CAN'T JOIN IT")
            return
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="▶️ **PLAYING** HERE THE SONG REQUESTED BY {} JOIN @THE_BLAZE_NETWORK".format(
        message.from_user.mention()
        ),
    )
    os.remove("final.png")
    return await lel.delete()


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_=cbd.split(None, 1)[1]
    try:
        x,query,useer_id = typed_.split("|")      
    except:
        await cb.message.edit("❌ song not found")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("ʙʜᴀɢɢ ᴊᴀᴀ ʏʜᴀ ꜱᴇ ʙꜱᴅᴋ !", show_alert=True)
        return
    #await cb.message.edit("🔁 **processing...**")
    x=int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=6).to_dict()
    resultss=results[x]["url_suffix"]
    title=results[x]["title"][:25]
    thumbnail=results[x]["thumbnails"][0]
    duration=results[x]["duration"]
    views=results[x]["views"]
    url = f"https://www.youtube.com{resultss}"
    try:    
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
             await cb.message.edit(f"❌ ꜱᴏɴɢ ɴᴏᴛ ʟᴏɴɢᴇʀ ᴛʜᴀɴ `{DURATION_LIMIT}` ᴍɪɴᴜᴛᴇꜱ.")
             return
    except:
        pass
    try:
        thumb_name = f"thumb-{title}veezmusic.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl=url
    dlurl=dlurl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖱 ᗰᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("🗑 ᑕʟᴏsᴇ", callback_data="cls"),
                ],[
                    InlineKeyboardButton("📣 ᑕʜᴀɴɴᴇʟ", url=f"https://t.me/THE_BLAZE_NETWORK"),
                    InlineKeyboardButton("✨ Ꮆʀᴏᴜᴘ", url=f"https://t.me/blaze_spammer")
                ],
            ]
    )
    requested_by = useer_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await converter.convert(youtube.download(url))  
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(
        chat_id,
        photo="final.png",
        caption=f"💡 **Tʀᴀᴄᴋ Iɴ ᑫᴜᴇᴜᴇ**\n\n🏷 **ᑎᴀᴍᴇ:** [{title[:45]}]({url})\n⏱ **ᗪᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 ** ᑌꜱᴇʀ ᗷʏ:** {r_by.mention}\n" \
               +f"\n🔢 **Tʀᴀᴄᴋ ᑭᴏꜱɪᴛɪᴏɴ:**  {position} ",
        reply_markup=keyboard,
        )
        os.remove("final.png")
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await b.send_photo(
        chat_id,
        photo="final.png",
        caption=f"🏷 **ᑎᴀᴍᴇ:** [{title[:45]}]({url})\n⏱ ** ᗪᴜʀᴀᴛɪᴏɴ:** `{duration}`\n😍 **Տᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n" \
               +f"🎧 **ᑌꜱᴇʀ ᗷʏ:** {r_by.mention}",
        reply_markup=keyboard,
        )
        os.remove("final.png")


@Client.on_message(filters.command("ytp") & filters.group & ~filters.edited)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔄 **processing...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>**Please Add {user.first_name} To Your Channel.**</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>❗*ᗰᴀᴋᴇ ᗰᴇ ᗩᴅᴍɪɴ ᖴɪʀꜱᴛ.* </b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "🤖: i'm joined to this group "
                    )
                    await lel.edit(
                        "<b>💡 ᗷʟᴀᴢᴇ ᕼᴇʟᴘ ᑌsᴇʀʙᴏᴛ ᒍᴏɪɴᴇᴅ ᑌʀ ᑕʜᴀᴛ..🤗🤭</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ\n{user.first_name} Iꜱ Nᴏᴛ Iɴ Youʀ Cʜᴀᴛꜱ."
                        f"\n\n Tʀʏ Tᴏ @{ASSISTANT_NAME} Aᴅᴅ </b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>{user.first_name} was banned in this group, ask admin to unban @{ASSISTANT_NAME}....</i>"
        )
        return
    await lel.edit("🔎 **FINDING SONG...**")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
     

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🎵 **Cᴏɴɴᴇᴄᴛɪɴɢ Tᴏ Bʟᴀᴢᴇ Sᴇʀᴠᴇʀ...**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:25]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit(
            "**❗ SONG NOT FOUND,** PLEASE GIVE A VALID SONG NAME."
        )
        print(str(e))
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
            [
                    InlineKeyboardButton("🖱 ᗰᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("🗑 ᑕʟᴏsᴇ", callback_data="cls"),
                ],[
                    InlineKeyboardButton("📣 ᑕʜᴀɴɴᴇʟ", url=f"https://t.me/THE_BLAZE_NETWORK"),
                    InlineKeyboardButton("✨ Ꮆʀᴏᴜᴘ", url=f"https://t.me/blaze_spammer")
            ],
        ]
    )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption = f"🏷 **ᑎᴀᴍᴇ:** [{title[:25]}]({url})\n⏱ ** ᗪᴜʀᴀᴛɪᴏɴ:** `{duration}`\n😍 **Տᴛᴀᴛᴜꜱ:** `Qᴜᴇᴜᴇᴅ Iɴ ᑭᴏꜱɪᴛɪᴏɴ {position}`\n" \
                    + f"🎧 **ᑌꜱᴇʀ ᗷʏ:** {message.from_user.mention}",
                   reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**❗ sorry, no active voice chat here, please turn on the voice chat first**")
            return
        await message.reply_photo(
            photo="final.png",
            caption = f"🏷 **ᑎᴀᴍᴇ:** [{title[:25]}]({url})\n⏱ **ᗪᴜʀᴀᴛɪᴏɴ:** `{duration}`\n💡 **Տᴛᴀᴛᴜꜱ:** `ᴘʟᴀʏɪɴɢ`\n" \
                    + f"🎧 **ᖇequest by:** {message.from_user.mention}",
                   reply_markup=keyboard,)
        os.remove("final.png")
        return await lel.delete()
