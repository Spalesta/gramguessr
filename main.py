import telebot

bot = telebot.TeleBot('7133097481:AAGizdgJ2SPCFJb6KynnTn_k5ilPfbKbwLY')

from telebot import types

@bot.message_handler(commands=['start'])
def startBot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("фикл")
    btn2 = types.KeyboardButton('самые изучаемые')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Выберите языки", reply_markup=markup)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть

'''from pygrambank import Grambank
gb = Grambank('.')
gb.sheets_dir
for sheet in gb.iter_sheets():
   print(sheet)
   break'''
