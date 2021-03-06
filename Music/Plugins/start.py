import yt_dlp
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton("đĨ Gece Mutualan", url=f"https://t.me/tegediskusirasa"),
            InlineKeyboardButton("đ° Ceha Random", url=f"https://t.me/grzmusik"),
        ],
        [
            InlineKeyboardButton("đ Daftar Perintah", url=f"https://telegra.ph/Mas-Gz-06-06"),
        ],
    ]
    return (
        "đ **{BOT_NAME} salah satu bot telegram yang bisa muter musik di grup**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "â Masukin gua ke Gece lu â", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton("đĨ Gece Mutualan", url=f"https://t.me/tegediskusirasa"),
            InlineKeyboardButton("đ° Ceha Random", url=f"https://t.me/grzmusik"),
        ],
        [
            InlineKeyboardButton( 
                "đ¤´ Wih Oner Bot", url=f"https://t.me/teleidgz"),
            InlineKeyboardButton("đ Daftar Perintah", url="https://telegra.ph/Mas-Gz-06-06"),
        ],
        [
            InlineKeyboardButton("âĒī¸ Gece Dukungan âŠī¸", url=f"https://t.me/tegediskusirasa"),
        ],
    ]
)
     
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text( 
                    f"đĻ Oner Bot [{member.mention}] Baru aja Gabung Di Gece Ini"
                )
            if member.id in SUDOERS: 
                return await message.reply_text(
                    f"đ¤ Etmin Bot [{member.mention}] Baru aja Gabung Di Gece Ini"
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id) 
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
đ **Hallo Sedih Rasanya Bisa Gabung Di Gece Ini**

đĄ **Jangan Lupa Untuk Jadiin Gua Admin Di Gece Ini**
""", 
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
Makasih Udah Masukin Gua Di Gece {message.chat.title}.
Musik nya Hidup Bwang. 

Info Bantuan Silahkan Klik Tombol Dibawah âŦ
""", 
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**đĻ Halo, Nama gua {rpk}!

đŦ Gua [{BOT_NAME}](t.me/{BOT_USERNAME}) Bot Musik Telegram dengan Segudang Fitur Eh Dikit Doang Sih đŋ
âââââââââââââ
âĸ Versi 7.9 Mutakhir
âĸ Rasakan Kegalauan, Masukin Gua di Gece
âââââââââââââ
â Tekan Tombol Command Buat Tahu Fitur Menarik Gua [{BOT_NAME}](t.me/{BOT_USERNAME})**

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            disable_web_page_preview=True,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
đ **Informasi Trek Video**

âī¸**Judul:** {x["title"]}

âŗ **Durasi:** {round(x["duration"] / 60)} Mins
đ **Ditonton:** `{x["view_count"]}`
đ **Suka:** `{x["like_count"]}`
đ **Tidak suka:** `{x["dislike_count"]}`
â­ī¸ **Peringkat Rata-rata:** {x["average_rating"]}
đĨ **Nama channel:** {x["uploader"]}
đ **Link Channel:** [Kunjungi Dari Sini]({x["channel_url"]})
đ **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**đ¤ DAFTAR PENGGUNA SUDO**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("Gada Pengguna Sudo Bwang")
            else:
                await message.reply_text(text)
