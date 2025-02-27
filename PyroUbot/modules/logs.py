import asyncio
import os
from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *
from PyroUbot.core.database.logger import *
from PyroUbot import *
import wget

__MODULE__ = "ʟᴏɢ"
__HELP__ = """
<blockquote>Bantuan Untuk Logs

perintah : <code>{0}logs</code> query > on or off
    mengaktifkan atau menonaktifkan logs</blockquote>
"""

async def create_botlog(client):
    name = "NyxianNetwork Logs"
    desc = "Jangan Keluar Dari Grup Log Ini\n\nPowered by: @KatsuHere"
    group = await client.create_supergroup(name, desc)
    nt = wget.download("https://res.cloudinary.com/ddhi78eee/image/upload/v1737552097/pfe4fxwb8rgoh0gcfltt.jpg")
    photo_video = {"video": nt} if nt.endswith(".mp4") else {"photo": nt}
    kntl = group.id
    await client.set_chat_photo(kntl, **photo_video)
    await client.send_message(
        kntl,
        f"**Group Log Berhasil Dibuat\n\nJangan Keluar Dari Sini!!!**",
    )


async def get_log(client):
    name = "NyxianNetwork Logs"
    async for dialog in client.get_dialogs():
        if dialog.chat.title == name:
            return dialog.chat
    return None


@ubot.on_message(
    filters.group
    & filters.mentioned
    & filters.incoming
    & ~filters.bot
    & ~filters.via_bot
)
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)
    if not cek:
        return
    user_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    user_link = f"<a href='tg://user?id={message.from_user.id}'>{user_name}</a>"
    message_link = message.link
    text = f"""
📨 <b>TAGS MESSAGE</b>
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{message.chat.title}</code>
• <b>Dari :</b> {user_link}
• <b>Pesan:</b> <code>{message.text}</code>

• <b>Tautan Grup:</b> <a href="{message.link}">Disini</a>
"""
    try:
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )


@ubot.on_message(
    filters.private
    & filters.incoming
    & ~filters.me
    & ~filters.bot
    & ~filters.service
)
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)

    if cek is None:
        return  # Tindakan yang sesuai jika hasil get_log_group adalah None

    if message.chat.id == 777000:
        return  # Menghindari pesan dari grup sistem Telegram

    async for x in client.search_messages(message.chat.id, limit=1):
        # Jangan meneruskan pesan bertimer, tapi langsung unduh dan kirim
        if not x.media or (x.media and hasattr(x, 'date') and x.date > message.date):
            await x.forward(log.id)
        else:
            # Jika media bertimer, langsung unduh dan kirim
            if x.photo:
                media = await client.download_media(x)
                await client.send_photo(log.id, media)
            elif x.video:
                media = await client.download_media(x)
                await client.send_video(log.id, media)
            elif x.document:
                media = await client.download_media(x)
                await client.send_document(log.id, media)
            # Hapus file setelah dikirim
            os.remove(media)


@ubot.on_message(
    filters.private
    & filters.incoming
    & (filters.photo | filters.video | filters.audio | filters.document)
    & ~filters.bot
    & ~filters.via_bot
)
async def handle_media_timer(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)

    if not cek:
        return  # Log group tidak aktif, tidak perlu melakukan apa-apa

    if message.chat.id == 777000:
        return  # Menghindari pesan dari grup sistem Telegram

    # Menangani file media
    media_type = None
    media_caption = message.caption or ""

    if message.photo:
        media_type = 'photo'
    elif message.video:
        media_type = 'video'
    elif message.audio:
        media_type = 'audio'
    elif message.document:
        media_type = 'document'

    if media_type:
        Tm = await message.reply("<emoji id=6010111371251815589>⏳</emoji> Processing...")
        try:
            # Mengunduh media
            media_file = await client.download_media(message)
            # Mengirim media ke grup log
            if media_type == 'photo':
                await client.send_photo(log.id, media_file, caption=media_caption)
            elif media_type == 'video':
                await client.send_video(log.id, media_file, caption=media_caption)
            elif media_type == 'audio':
                await client.send_audio(log.id, media_file, caption=media_caption)
            elif media_type == 'document':
                await client.send_document(log.id, media_file, caption=media_caption)

            # Menghapus file setelah mengirim
            os.remove(media_file)

            await Tm.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await handle_media_timer(client, message)  # Coba lagi setelah menunggu


@PY.UBOT("logger")
async def _(client, message):
    xx = await message.reply(f"**Processing...**")
    cek = get_arg(message)
    logs = await get_log_group(client.me.id)
    if cek.lower() == "on":
        if not logs:
            await set_log_group(client.me.id, logger=True)
            await create_botlog(client)
            log = await get_log(client)
            grup = await client.export_chat_invite_link(int(log.id))
            return await xx.edit(f"**Log Group Berhasil Diaktifkan :\n\n{grup}**")
        else:
            return await xx.edit(f"**Log Group anda Sudah aktif.**")
    if cek.lower() == "off":
        if logs:
            await del_log_group(client.me.id)
            log = await get_log(client)
            await client.delete_supergroup(int(log.id))
            return await xx.edit(f"**Log Group Berhasil Dinonaktifkan.**")
        else:
            return await xx.edit(f"**Log Group anda Sudah Dinonaktifkan.**")
    else:
        return await xx.edit(
            f"**Format yang anda berikan salah. silahkan gunakan <code>{message.text} on/off</code>**"
        )
