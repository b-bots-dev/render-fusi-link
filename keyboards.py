from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import common_globals as cg


def keyboards(keyboard, param=None):

    if keyboard == 'cancel':
        btn1 = InlineKeyboardButton('CANCEL', callback_data='cancel')
        btn2 = InlineKeyboardButton('BACK', callback_data='back')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'users':
        btn1 = InlineKeyboardButton('ADD', callback_data='add')
        btn2 = InlineKeyboardButton('REMOVE', callback_data='remove')
        btn3 = InlineKeyboardButton('SHOW', callback_data='show')
        btn4 = InlineKeyboardButton('CANCEL', callback_data='cancel')
        buttons = [
            [btn1],
            [btn2],
            [btn3],
            [btn4]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'add_again':
        btn1 = InlineKeyboardButton('ADD AGAIN', callback_data='add')
        btn2 = InlineKeyboardButton('BACK', callback_data='back')
        btn3 = InlineKeyboardButton('CANCEL', callback_data='cancel')

        buttons = [[btn1],
                   [btn2, btn3]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'rm':
        buttons = []
        for tg_id in cg.whitelist:
            btn = InlineKeyboardButton(f'{tg_id}', callback_data=f'rm.{tg_id}')
            buttons.append([btn])
        btn1 = InlineKeyboardButton('BACK', callback_data='back')
        btn2 = InlineKeyboardButton('CANCEL', callback_data=f'cancel')
        buttons.append([btn1, btn2])
        kb = InlineKeyboardMarkup(buttons)
        return kb
