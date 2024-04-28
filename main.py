import telebot

botTimeWeb = telebot.TeleBot('7133097481:AAGizdgJ2SPCFJb6KynnTn_k5ilPfbKbwLY')

from telebot import types

@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nХочешь расскажу немного о нашей компании?"
  markup = types.InlineKeyboardMarkup()
  button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
  markup.add(button_yes)
  botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
  

'''from pygrambank import Grambank
gb = Grambank('.')
gb.sheets_dir
for sheet in gb.iter_sheets():
   print(sheet)
   break'''