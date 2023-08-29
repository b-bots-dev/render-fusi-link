import os
import re
from pyrogram import Client, filters
from keep_alive import keep_alive
from link_gen import link_gen


bot = Client("fusi-render",
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'])


@bot.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply('Alive')


@bot.on_message(filters.text)
async def text_message(client, message):
    text = str(message.text)
    cid = message.chat.id
    urls = re.findall(r'(https?://\S+)', text)
    uids = set()

    if text.upper().startswith('ID'):
        uid = text[2:].strip()
        if uid.isdigit():
            uids.add(uid)

    if text.upper().endswith('ID'):
        uid = text[:-2].strip()
        if uid.isdigit():
            uids.add(uid)

    for url in urls:

        if 'zhibo.yazhaiyabo.com/share/live' in url:
            uid = url.split('/')[-1].split('.')[0]
            if uid.isdigit():
                uids.add(uid)

        if 'liveRoom.html?roomId=' in url:
            uid = url.split('=')[1].split('&')[0]
            if uid.isdigit():
                uids.add(uid)

    if len(uids) > 0:
        for uid in uids:
            resp_text = link_gen(uid)
            if resp_text is not None:
                await bot.send_message(cid, resp_text)
            else:
                await bot.send_message(cid, 'Unhandled exception')
        uids.clear()

#
keep_alive()
print('BOT STARTED')
bot.run()
