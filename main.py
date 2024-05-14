import telebot

bot = telebot.TeleBot('7133097481:AAGizdgJ2SPCFJb6KynnTn_k5ilPfbKbwLY')

from telebot import types
from langlists import most, facl
import random
facl_list = "фикл"
most_list = "самые изучаемые"
@bot.message_handler(commands=['start'])
def startBot(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(facl_list)
    btn2 = types.KeyboardButton(most_list)
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Выберите языки", reply_markup=markup)

lang_counter = 0
lang_list = list()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == facl_list or most_list:
        if message.text == facl_list:
            lang_list = most
        elif message.text == most_list:
            lang_list = facl
        lang_counter = 0
        markup = types.ReplyKeyboardMarkup()  # создание новых кнопок
        btn1 = types.KeyboardButton('начать игру')
        markup.add(btn1)
        bot.send_message(message.from_user.id, f'давайте начнем {facl_list}', reply_markup=markup)  # ответ бота


import csv
def choose_language(li):
    random.shuffle(li)
    lang = li[0].capitalize()
    # print(lang)
    with open('data/draft.csv') as raw_data:
        reader = list(csv.reader(raw_data, delimiter=','))
        lang_data = [(line[2], line[4]) for line in reader if line[1] == lang]
        return lang_data

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть

