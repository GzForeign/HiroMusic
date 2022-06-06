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
            InlineKeyboardButton("👥 Gece Mutualan", url=f"https://t.me/tegediskusirasa"),
            InlineKeyboardButton("🎰 Ceha Random", url=f"https://t.me/grzmusik"),
        ],
        [
            InlineKeyboardButton("📖 Daftar Perintah", url=f"https://telegra.ph/Mas-Gz-06-06"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} salah satu bot telegram yang bisa muter musik di grup**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ Masukin gua ke Gece lu ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton("👥 Gece Mutualan", url=f"https://t.me/tegediskusirasa"),
            InlineKeyboardButton("🎰 Gece Random", url=f"https://t.me/grzmusik"),
        ],
        [
            InlineKeyboardButton( 
                "🤴 Wih Oner Bot", url=f"https://t.me/teleidgz"),
            InlineKeyboardButton("📖 Daftar Perintah", url="https://telegra.ph/Mas-Gz-06-06"),
        ],
        [
            InlineKeyboardButton("↪️ Gece Dukungan ↩️", url=f"https://t.me/tegediskusirasa"),
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
                    f"🦍 Oner Bot [{member.mention}] Baru aja Gabung Di Gece Ini"
                )
            if member.id in SUDOERS: 
                return await message.reply_text(
                    f"👤 Etmin Bot [{member.mention}] Baru aja Gabung Di Gece Ini"
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id) 
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 **Hallo Sedih Rasanya Bisa Gabung Di Gece Ini**

💡 **Jangan Lupa Untuk Jadiin Gua Admin Di Gece Ini**
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

Info Bantuan Silahkan Klik Tombol Dibawah ⬇
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
**🦍 Halo, Nama gua {rpk}!

💬 Gua [{BOT_NAME}](t.me/{BOT_USERNAME}) Bot Musik Telegram dengan Segudang Fitur Eh Dikit Doang Sih 🗿
➖➖➖➖➖➖➖➖➖➖➖➖➖
• Versi 7.9 Mutakhir
• Rasakan Kegalauan, Masukin Gua di Gece
➖➖➖➖➖➖➖➖➖➖➖➖➖
➛ Tekan Tombol Command Buat Tahu Fitur Menarik Gua [{BOT_NAME}](t.me/{BOT_USERNAME})**

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
🔍 **Informasi Trek Video**

❇️**Judul:** {x["title"]}

⏳ **Durasi:** {round(x["duration"] / 60)} Mins
👀 **Ditonton:** `{x["view_count"]}`
👍 **Suka:** `{x["like_count"]}`
👎 **Tidak suka:** `{x["dislike_count"]}`
⭐️ **Peringkat Rata-rata:** {x["average_rating"]}
🎥 **Nama channel:** {x["uploader"]}
📎 **Link Channel:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
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
            text = "**👤 DAFTAR PENGGUNA SUDO**\n\n"
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
