import os
import re
from pyrogram import Client, filters, enums
import pyrostep
from pyrogram.errors import RPCError
from keep_alive import keep_alive
from keyboards import keyboards
from link_gen import link_gen
import common_globals as cg


bot = Client("fusi-render",
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'])
pyrostep.listen(bot)


bot_msg = {}


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    fuid = msg.from_user.id
    if fuid in cg.whitelist:
        await msg.reply('Alive')
    else:
        await msg.reply("This BOT is private")


@bot.on_message(filters.command('users'))
async def users_command(client, msg):
    cid = msg.chat.id
    mid = msg.id
    await bot.delete_messages(cid, mid)

    if cid == int(os.environ['MASTER']):
        bm = await msg.reply('Select', reply_markup=keyboards('users'))
        bot_msg[cid] = bm
    else:
        await msg.reply("Command only for admins")


@bot.on_message(filters.text)
async def text_message(client, msg):
    text = str(msg.text)
    fuid = msg.from_user.id
    cid = msg.chat.id

    if fuid in cg.whitelist:
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
    else:
        await msg.reply("You don't have permissions to use this bot")


@bot.on_callback_query()
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id
    try:
        bm = bot_msg[cid]
    except KeyError:
        bm = None

    if call.data == 'add':
        await bot.edit_message_text(cid, bm.id, 'Enter ID to add', reply_markup=keyboards('cancel'))
        await pyrostep.register_next_step(cid, add)

    if call.data == 'remove':
        await bot.edit_message_text(cid, bm.id, 'Tap ID to remove', reply_markup=keyboards('rm'))

    if call.data.startswith('rm'):
        tg_id = int(call.data.split('.')[1])
        if tg_id != int(os.environ['MASTER']):
            cg.whitelist.remove(tg_id)
            await bot.edit_message_text(cid, bm.id, 'Tap ID to remove', reply_markup=keyboards('rm'))
        else:
            await bot.answer_callback_query(call.id, f"MASTER ID can't be removed", show_alert=True)

    if call.data == 'show':
        text = 'Current users\n\n'
        for user in cg.whitelist:
            text = f'{text}{user}\n'
        await bot.edit_message_text(cid, bm.id, text, reply_markup=keyboards('cancel'))

    if call.data == 'back':
        await pyrostep.unregister_steps(cid)
        await bot.edit_message_text(cid, bm.id, 'Select', reply_markup=keyboards('users'))
    if call.data == 'cancel':
        await pyrostep.unregister_steps(cid)
        await bot.delete_messages(cid, mid)
        try:
            del bot_msg[cid]
        except KeyError:
            pass


async def add(client, msg):
    cid = msg.chat.id
    mid = msg.id
    await bot.delete_messages(cid, mid)

    try:
        bm = bot_msg[cid]
    except KeyError:
        bm = None

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, bm.id, 'ID must be number\n\n'
                                                    'Enter ID to add', reply_markup=keyboards('cancel'))
        except RPCError:
            pass
        await pyrostep.register_next_step(cid, add)
    else:
        try:
            tg_id = int(msg.text)
            # try:
            # await bot.send_chat_action(tg_id, enums.ChatAction.TYPING)
            cg.whitelist.add(tg_id)
            await bot.edit_message_text(cid, bm.id, 'ID added successful', reply_markup=keyboards('add_again'))

            # except RPCError:
            #     await bot.edit_message_text(cid, bm.id, "BOT can't write to this id"
            #                                             'Enter ID to add', reply_markup=keyboards('cancel'))
            #     await pyrostep.register_next_step(cid, add)

        except ValueError:
            try:
                await bot.edit_message_text(cid, bm.id, 'ID must be number\n\n'
                                                        'Enter ID to add', reply_markup=keyboards('cancel'))
            except RPCError:
                pass
            await pyrostep.register_next_step(cid, add)


try:
    bot.stop()
except ConnectionError:
    pass

keep_alive()
print('BOT STARTING')
bot.run()
