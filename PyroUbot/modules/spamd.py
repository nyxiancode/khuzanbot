from PyroUbot import *
import asyncio

__MODULE__ = "dspam"
__HELP__ = """
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sᴘᴀᴍ 』</b>

<b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}dspam</code> [ᴊᴜᴍʟᴀʜ_ᴘᴇsᴀɴ - ᴊᴜᴍʟᴀʜ_ᴅᴇʟᴀʏ_ᴅᴇᴛɪᴋ - ᴘᴇsᴀɴ_sᴘᴀᴍ]
<b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ʙᴇʀᴜʟᴀɴɢ ᴅᴇɴɢᴀɴ ᴊᴇᴅᴀ ᴡᴀᴋᴛᴜ ᴛᴇʀᴛᴇɴᴛᴜ.

<b>ᴄᴏɴᴛᴏʜ:</b>
<code>{0}dspam 10 2 ᴛᴇsᴛ sᴘᴀᴍ</code>
"""

async def dspam_cmd(client, message):
    reply = message.reply_to_message
    msg = await message.reply("sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs", quote=False)
    
    try:
        # Ambil jumlah pesan dan jeda waktu dari perintah
        count_message = int(message.command[1])
        count_delay = int(message.command[2])
        
        # Batasi jumlah pesan dan jeda waktu untuk mencegah penyalahgunaan
        if count_message > 20:
            return await msg.edit("❌ ᴍᴀᴋsɪᴍᴀʟ 20 ᴘᴇsᴀɴ ᴘᴇʀ ᴘᴇʀɪɴᴛᴀʜ.")
        if count_delay < 1:
            return await msg.edit("❌ ᴊᴇᴅᴀ ᴡᴀᴋᴛᴜ ᴍɪɴɪᴍᴀʟ 1 ᴅᴇᴛɪᴋ.")
        
        # Jika pesan adalah balasan
        if reply:
            for i in range(count_message):
                await reply.copy(message.chat.id)
                await asyncio.sleep(count_delay)
        else:
            # Jika pesan bukan balasan, pastikan ada teks spam
            if len(message.command) < 4:
                return await msg.edit("❌ ᴍᴏʜᴏɴ ʙᴇʀɪᴋᴀɴ ᴘᴇsᴀɴ sᴘᴀᴍ. ᴋᴇᴛɪᴋ <code>{0}help dspam</code> ᴜɴᴛᴜᴋ ʙᴀɴᴛᴜᴀɴ.")
            text_to_spam = message.text.split(None, 3)[3]
            for i in range(count_message):
                await message.reply(text_to_spam, quote=False)
                await asyncio.sleep(count_delay)
        
        # Hapus pesan "sedang diproses" dan pesan perintah
        await msg.delete()
        await message.delete()
    
    except IndexError:
        await msg.edit("❌ ᴍᴏʜᴏɴ ʙᴇʀɪᴋᴀɴ ᴘᴀʀᴀᴍᴇᴛᴇʀ ʏᴀɴɢ ʙᴇɴᴀʀ. ᴋᴇᴛɪᴋ <code>{0}help dspam</code> ᴜɴᴛᴜᴋ ʙᴀɴᴛᴜᴀɴ.")
    except ValueError:
        await msg.edit("❌ ᴍᴏʜᴏɴ ʙᴇʀɪᴋᴀɴ ᴀɴɢᴋᴀ ʏᴀɴɢ ʙᴇɴᴀʀ.")
    except Exception as error:
        await msg.edit(f"❌ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ: {str(error)}")

@PY.UBOT("dspam")
async def dspam_handler(client, message):
    await dspam_cmd(client, message)
