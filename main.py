import telebot
from telebot import types
import langlists
import random
import pandas as pd
from config import *

bot = telebot.TeleBot(BOT_TOKEN)
facl_list_message = "I want to study FaCL languages!"
most_list_message = "I want to study top-10 most learned languages!"
rating = {}
fail_count = {}

@bot.message_handler(commands=['start'])
def startbot(message):
    userid = message.from_user.username
    if userid not in rating.keys():
        rating[userid] = 0

    if message.from_user.id not in fail_count.keys():
        fail_count[message.from_user.id] = 0

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
        if len(message.text.strip()) == len('/info'):
            bot.send_message(userid, f"What language would you like to learn more about? Please type /info *and* the name of the language", reply_markup=None, parse_mode='Markdown')
        else:
            lang = message.text[len('/info '):]
            info = get_info(lang)
            bot.send_message(userid, f"Information on <b>{lang}</b>:\n\n{info}", reply_markup=None, parse_mode="HTML")


@bot.message_handler(commands=['end'])
def end(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        quiz_mode_on[userid] = False
        bot.send_message(userid, f"Okay! You've guessed "
                                 f"{currently_studying[userid][0][:currently_studying[userid][1]]}", reply_markup=None)
    else:
        bot.send_message(userid, "my guy you haven't even started yet", reply_markup=None)


@bot.message_handler(commands=['rating'])
def get_rate(message):
    userid = message.from_user.id
    sorted_rate = dict(reversed(sorted(rating.items(), key=lambda x:x[1])))
    end = "Current rating:\n"
    for index in range(len(sorted_rate.items())):
        end += f"{index + 1}) <b>{list(sorted_rate.items())[index][0]}</b> - <b>{list(sorted_rate.items())[index][1]}</b>"

    bot.send_message(userid, end, reply_markup=None, parse_mode="HTML")


'''@bot.message_handler(commands=['help'])
def help(message):
    userid = message.from_user.id
    bot.send_message(userid, "", reply_markup=None)'''


@bot.message_handler(commands=['hint'])
def help(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        bot.send_message(userid, f"This one is {currently_studying[userid][0][currently_studying[userid][1]]}", reply_markup=None)
    else:
        bot.send_message(userid, "my guy you aren't playing yet what do you want a hint at????", reply_markup=None)


@bot.message_handler(commands=['add'])
def add(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        bot.send_message(userid, "Sorry, you can't do that while you're playing! "
                                 "Finish the game first", reply_markup=None)
    else:
        if len(message.text) <= len('/add '):
            bot.send_message(userid,
                             f"What language would you like to add? Please type /add *and* the name of the language",
                             reply_markup=None, parse_mode='Markdown')
        else:
            lang = message.text[len('/add '):]
            bot.send_message(userid, f"Added {lang} to current to-study list!", reply_markup=None)
            currently_studying[userid][0].append(lang)


@bot.message_handler(commands=['remove'])
def remove(message):
    userid = message.from_user.id
    if userid in quiz_mode_on and quiz_mode_on[userid]:
        bot.send_message(userid, "Sorry, you can't do that while you're playing! "
                                 "Finish the game first", reply_markup=None)
    else:
        if len(message.text) <= len('/remove '):
            bot.send_message(userid,
                             f"What language would you like to remove? Please type /remove *and* the name of the language",
                             reply_markup=None, parse_mode='Markdown')
        else:
            lang = message.text[len('/remove '):]
            bot.send_message(userid, f"Removed {lang} from current to-study list!", reply_markup=None)
            currently_studying[userid][0] = [item for item in currently_studying[userid][0] if item != lang]


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
        bot.send_message(userid, langlists.start_msg(currently_studying[userid][0]), reply_markup=markup, parse_mode='Markdown')
    
    elif message.text == 'start':
        markup = types.ReplyKeyboardMarkup()
        for lang in random.sample(currently_studying[userid][0], len(currently_studying[userid][0])):
            markup.add(types.KeyboardButton(lang))
        quiz_mode_on[userid] = True

        lang_info = get_info(currently_studying[userid][0][0])

        bot.send_message(userid, lang_info, reply_markup=markup, parse_mode="HTML")

    elif message.text in langlists.facl + langlists.most:  # если пользователь написал название языка
        langlist = currently_studying[userid][0]
        i = currently_studying[userid][1]
        
        if langlist[i] == message.text.strip():  # если пользователь угадал язык правильно
            rating[message.from_user.username] += 1

            if userid not in personal_rating:
                personal_rating[userid] = 0
            personal_rating[userid] += 1
            currently_studying[userid][1] += 1
            i += 1
            if i == len(langlist):
                quiz_mode_on[userid] = False
                bot.send_message(userid, f"That's right! The game's over", reply_markup=None)
            else:
                lang = langlist[i]
                info = get_info(lang)
                bot.send_message(userid, f"That's right!\nYou have {('❤️' * (LIVES_AMOUNT - fail_count[userid])) + ('🖤' * fail_count[userid])} lives.\n\nNow,\n{info}", reply_markup=None, parse_mode="HTML")

            if personal_rating[userid] in achievements:
                bot.send_message(userid, f"_new achievement unlocked: {achievements[personal_rating[userid]]}_", reply_markup=None, parse_mode='Markdown')
                bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAIBHmZGKRxnyYHcBkcXUXnW07XEUejaAAJuDgACzb5RUT1kKoe5P8b9NQQ")

        else:  # если не угадал язык
            if userid not in fail_count.keys():
                fail_count[userid] = 1
            else:
                fail_count[userid] += 1

            if fail_count[userid] >= LIVES_AMOUNT:
                markup = types.ReplyKeyboardMarkup()
                markup.row("start")

                bot.send_message(userid, f"That's wrong :(\nYou ran out of all your lives.\nYou have {('❤️' * (LIVES_AMOUNT - fail_count[userid])) + ('🖤' * fail_count[userid])} lives.\nTo try again press button below or print /start.", reply_markup=markup)
                fail_count[userid] = 0

            else:

                if fail_count == HINT_APPLY_AMOUNT:
                    bot.send_message(userid, "Type /hint if you'd like a hint ;3", reply_markup=None)
                bot.send_message(userid, f"That's wrong :( Try again?\nYou've got <b>{fail_count[userid]}</b> fails.\nYou have only {('❤️' * (LIVES_AMOUNT - fail_count[userid])) + ('🖤' * fail_count[userid])} lives.", reply_markup=None, parse_mode='HTML')

    else:  # если пользователь совсем какой-то бред написал
        bot.send_message(userid, 'what?????', reply_markup=None)


def get_info(language_name):  # принимает название языка, возвращает текст с информацией о нем
    data = pd.read_csv('./data/draft.csv')
    data["Language_name"] = data["Language_name"].apply(lambda x: x.lower())
    data.fillna("-", inplace=True)

    query = data[(data["Language_name"] == language_name.lower()) | (data["Language_ID"] == language_name.lower())]
    if query.shape[0] >= GET_INFO_AMOUNT:
        query = query.sample(GET_INFO_AMOUNT)

    if query.shape[0] == 0:
        return f"There is no data for {language_name}"

    else:
        end_msg = ""
        for _, row in query.iterrows():
            end_msg += f'<b>{row["Parameter"]}:</b>\n{row["Description"]}\n---\n'
        return end_msg

bot.polling(none_stop=True, interval=0)
'''
python main.py
'''
