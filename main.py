import telebot
from telebot import types
import langlists
import random

bot = telebot.TeleBot('7133097481:AAGizdgJ2SPCFJb6KynnTn_k5ilPfbKbwLY')


facl_list = "фикл"
most_list = "самые изучаемые"


@bot.message_handler(commands=['start'])
def startbot(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(facl_list)
    btn2 = types.KeyboardButton(most_list)
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "please choose the languages you'd like to study:", reply_markup=markup)


currently_studying = {'userid': [['languages'], 0]}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global currently_studying
    if message.text == facl_list or message.text == most_list:
        if message.text == facl_list:
            currently_studying[message.from_user.id] = [random.sample(langlists.facl, len(langlists.facl)), 0]
        elif message.text == most_list:
            currently_studying[message.from_user.id] = [random.sample(langlists.most, len(langlists.most)), 0]
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('начать игру')
        markup.add(btn1)
        bot.send_message(message.from_user.id, f'давайте начнем {currently_studying[message.from_user.id][0]}',
                         reply_markup=markup)
    elif message.text == 'начать игру':
        markup = types.ReplyKeyboardMarkup()
        for lang in currently_studying[message.from_user.id][0]:
            markup.add(types.KeyboardButton(lang))
        bot.send_message(message.from_user.id, currently_studying[message.from_user.id][0][0], reply_markup=markup)
    elif message.text in langlists.facl + langlists.most:  # если пользователь написал название языка
        langlist = currently_studying[message.from_user.id][0]
        i = currently_studying[message.from_user.id][1]
        if langlist[i] == message.text:
            currently_studying[message.from_user.id][1] += 1
            i += 1
            if i == len(langlist):
                bot.send_message(message.from_user.id, f"that's right! the game's over", reply_markup=None)
            else:
                bot.send_message(message.from_user.id, f"that's right! now, {langlist[i]}", reply_markup=None)
        else:
            print(langlist, i)
            print(message.text)
            bot.send_message(message.from_user.id, 'wrong :(', reply_markup=None)
    else:  # если пользователь совсем какой-то бред написал
        bot.send_message(message.from_user.id, 'what?????', reply_markup=None)


bot.polling(none_stop=True, interval=0)
'''
python main.py
'''
