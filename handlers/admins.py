# Powered by @HYPER_AD13 | @ShiningOff
# Dear Pero ppls Plish Don't remove this line from here🌚

from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.filters import command, other_filters
from callsmusic import callsmusic, queues
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, KeyboardButton,
                            ReplyKeyboardMarkup, ReplyKeyboardRemove)


PAUSED = "https://te.legra.ph/file/b0651ece8c715c4e09f80.jpg"
RESUMED = "https://te.legra.ph/file/f3adfee360b9921538437.jpg"
SKIPPED = "https://te.legra.ph/file/c06e694cfaed0ee37aed4.jpg"
END = "https://te.legra.ph/file/e4ceba57c28876220b355.jpg"

BUTTON = [
    [
        InlineKeyboardButton(text="Support", url="https://t.me/ShineVcbot_support"),
        InlineKeyboardButton(text="🗑️Close", callback_data="close_"),
    ],
]

ACTV_CALLS = []

@Client.on_message(command(["pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    
    await message.reply_photo(
        photo=PAUSED,
        caption=f"ᴏᴋᴋ, sᴛʀᴇᴀᴍ ᴘᴀᴜsᴇᴅ ʙʏ {message.from_user.mention} 🥀\n\n✦ /resume :- ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ!",
        reply_markup=InlineKeyboardMarkup(BUTTON)
    )
    await message.delete()


@Client.on_message(command(["resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    
    await message.reply_photo(
        photo=RESUMED,
        caption=f"ᴏᴋᴋ, ʀᴇsᴜᴍᴇᴅ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ ʙʏ {message.from_user.mention} 💫.\n\n✦ /pause :- ᴘᴀᴜsᴇ ᴘʟᴀʏʙᴀᴄᴋ!!",
        reply_markup=InlineKeyboardMarkup(BUTTON)
    )
    await message.delete()


@Client.on_message(command(["end"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chut_id = message.chat.id
    if int(chut_id) not in ACTV_CALLS:
        await message.reply_text(
            "ᴡᴛғ, ᴘʟᴀʏ ᴛʜᴇ sᴏɴɢ ғɪʀsᴛ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ sᴋɪᴘ ᴛᴀᴛ🙄!",
            reply_markup=InlineKeyboardMarkup(BUTTON)
        )
        await message.delete()
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    
        await message.reply_photo(
            photo=END,
            caption=f"ᴏᴋᴋ, sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ ʙʏ {message.from_user.mention} \n ɴᴏᴡ ʟᴇᴀᴠɪɴɢ ᴠᴄ ʙʏᴇ ʙʏᴇ!👋🏻",
            reply_markup=InlineKeyboardMarkup(BUTTON)
        )
        await message.delete()

@Client.on_message(command(["skip"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        
        await message.reply_text(
            "ᴡᴛғ, ᴘʟᴀʏ ᴛʜᴇ sᴏɴɢ ғɪʀsᴛ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ sᴋɪᴘ ᴛᴀᴛ🙄!",
            reply_markup=InlineKeyboardMarkup(BUTTON)
        )
        await message.delete()
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
    
    await message.reply_photo(
        photo=SKIPPED,
        caption=f"ʜᴜʜ ᴏᴋᴋ, ᴍᴏᴠᴇᴅ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ sᴏɴɢ!\nsᴛʀᴇᴀᴍ sᴋɪᴘ ʙʏ {message.from_user.mention}🥀",
        reply_markup=InlineKeyboardMarkup(BUTTON)
    )
    await message.delete()
