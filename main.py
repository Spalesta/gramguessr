import telebot
from telebot import types
import langlists
import random

bot = telebot.TeleBot('7133097481:AAGizdgJ2SPCFJb6KynnTn_k5ilPfbKbwLY')
facl_list_message = "I want to study FaCL languages!"
most_list_message = "I want to study top-10 most learned languages!"


@bot.message_handler(commands=['start'])
def startbot(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(facl_list_message)
    btn2 = types.KeyboardButton(most_list_message)
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     "Please choose the list of languages you'd like to study:", reply_markup=markup)


currently_studying = {'userid': [['languages'], 0]}
personal_rating = {'userid': 0}
achievements = {1: "your first correct guess!",
                5: "you've guessed correctly 5 time so far",
                15: "you've guessed correctly 15 time so far",
                50: "are you okay?",
                100: "please hydrate"}


@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    bot.send_message(message.chat.id, f'This sticker id: {message.sticker.file_id}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global currently_studying
    if message.text == facl_list_message or message.text == most_list_message:
        if message.text == facl_list_message:
            currently_studying[message.from_user.id] = [random.sample(langlists.facl, len(langlists.facl)), 0]
        elif message.text == most_list_message:
            currently_studying[message.from_user.id] = [random.sample(langlists.most, len(langlists.most)), 0]
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('start')
        markup.add(btn1)
        bot.send_message(message.from_user.id, f"Okay, let's start studying "
                                               f"{currently_studying[message.from_user.id][0]}", reply_markup=markup)
    elif message.text == 'start':
        markup = types.ReplyKeyboardMarkup()
        for lang in currently_studying[message.from_user.id][0]:
            markup.add(types.KeyboardButton(lang))
        bot.send_message(message.from_user.id, currently_studying[message.from_user.id][0][0], reply_markup=markup)

    elif message.text in langlists.facl + langlists.most:  # если пользователь написал название языка
        langlist = currently_studying[message.from_user.id][0]
        i = currently_studying[message.from_user.id][1]
        if langlist[i] == message.text:  # если пользователь угадал язык правильно
            if message.from_user.id not in personal_rating:
                personal_rating[message.from_user.id] = 0
            personal_rating[message.from_user.id] += 1
            currently_studying[message.from_user.id][1] += 1
            i += 1
            if i == len(langlist):
                bot.send_message(message.from_user.id, f"That's right! The game's over", reply_markup=None)
            else:
                bot.send_message(message.from_user.id, f"That's right! Now, {langlist[i]}", reply_markup=None)

            if personal_rating[message.from_user.id] in achievements:
                bot.send_message(message.from_user.id, f"__new achievement unlocked: {achievements[personal_rating[message.from_user.id]]}__", reply_markup=None, parse_mode='Markdown')
                bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAIBHmZGKRxnyYHcBkcXUXnW07XEUejaAAJuDgACzb5RUT1kKoe5P8b9NQQ")

        else:
            bot.send_message(message.from_user.id, "That's wrong :( Try again?", reply_markup=None)

    else:  # если пользователь совсем какой-то бред написал
        bot.send_message(message.from_user.id, 'what?????', reply_markup=None)


def get_info(language_name):  # принимает название языка, возвращает текст с информацией о нем
    pass


bot.polling(none_stop=True, interval=0)
'''
python main.py
'''
