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
                5: "you've guessed correctly 5 times so far",
                15: "you've guessed correctly 15 time so far",
                50: "are you okay?",
                100: "please hydrate"}
quiz_mode_on = {'userid': False}
fail_count = {'userid': 0}


@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    bot.send_message(message.chat.id, f'This sticker id: {message.sticker.file_id}')


@bot.message_handler(commands=['info'])
def info(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        bot.send_message(userid, "Sorry, you can't do that while you're playing! "
                                 "Finish the game first", reply_markup=None)
    else:
        if len(message.text) <= len('/info '):
            bot.send_message(userid, f"What language would you like to learn more about? Please type /info *and* the name of the language", reply_markup=None, parse_mode='Markdown')
        else:
            lang = message.text[len('/info '):]
            bot.send_message(userid, f"Information on {lang}: {lang}", reply_markup=None)


@bot.message_handler(commands=['end'])
def end(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        quiz_mode_on[userid] = False
        bot.send_message(userid, f"Okay! You've guessed "
                                 f"{currently_studying[userid][0][:currently_studying[userid][1]]}", reply_markup=None)
    else:
        bot.send_message(userid, "my guy you haven't even started yet", reply_markup=None)


@bot.message_handler(commands=['help'])
def help(message):
    userid = message.from_user.id
    bot.send_message(userid, "", reply_markup=None)


@bot.message_handler(commands=['hint'])
def help(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        bot.send_message(userid, f"This one is {currently_studying[userid][0][currently_studying[userid][1]]}", reply_markup=None)
    else:
        bot.send_message(userid, "my guy you aren't playing yet what do you want a hint at????", reply_markup=None)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global currently_studying
    userid = message.from_user.id

    if message.text == facl_list_message or message.text == most_list_message:
        if message.text == facl_list_message:
            currently_studying[userid] = [random.sample(langlists.facl, len(langlists.facl)), 0]
        elif message.text == most_list_message:
            currently_studying[userid] = [random.sample(langlists.most, len(langlists.most)), 0]
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('start')
        markup.add(btn1)
        bot.send_message(userid, f"Okay, let's start studying {currently_studying[userid][0]}! If you want to see more information on any of these languages before we start, type /info and the name of the language you want to learn more about, else just press _start_ :3", reply_markup=markup, parse_mode='Markdown')
    elif message.text == 'start':
        fail_count[userid] = 0
        markup = types.ReplyKeyboardMarkup()
        for lang in random.sample(currently_studying[userid][0], len(currently_studying[userid][0])):
            markup.add(types.KeyboardButton(lang))
        quiz_mode_on[userid] = True
        bot.send_message(userid, currently_studying[userid][0][0], reply_markup=markup)

    elif message.text in langlists.facl + langlists.most:  # если пользователь написал название языка
        langlist = currently_studying[userid][0]
        i = currently_studying[userid][1]
        if langlist[i] == message.text:  # если пользователь угадал язык правильно
            if userid not in personal_rating:
                personal_rating[userid] = 0
            personal_rating[userid] += 1
            currently_studying[userid][1] += 1
            i += 1
            if i == len(langlist):
                quiz_mode_on[userid] = False
                bot.send_message(userid, f"That's right! The game's over", reply_markup=None)
            else:
                bot.send_message(userid, f"That's right! Now, {langlist[i]}", reply_markup=None)

            if personal_rating[userid] in achievements:
                bot.send_message(userid, f"_new achievement unlocked: {achievements[personal_rating[userid]]}_", reply_markup=None, parse_mode='Markdown')
                bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAIBHmZGKRxnyYHcBkcXUXnW07XEUejaAAJuDgACzb5RUT1kKoe5P8b9NQQ")

        else:  # если не угадал язык
            if userid not in fail_count:
                fail_count[userid] = 0
            fail_count[userid] += 1
            bot.send_message(userid, "That's wrong :( Try again?", reply_markup=None)

    else:  # если пользователь совсем какой-то бред написал
        bot.send_message(userid, 'what?????', reply_markup=None)


def get_info(language_name):  # принимает название языка, возвращает текст с информацией о нем
    pass


bot.polling(none_stop=True, interval=0)
'''
python main.py
'''
