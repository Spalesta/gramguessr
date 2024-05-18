most = '''English
German
French
Spanish
Japanese
Korean
Italian
Hindi
Mandarin
Russian'''.split()

facl = '''French
Swedish
Hebrew
Italian
German
Korean
Hindi'''.split('\n')


def start_msg(langlist):
    return f'''Okay, let's start studying *{', '.join(langlist)}*!
    
• If you want to see more information on any of these languages before we start, type /info and the name of the language you want to learn more about;
• if you want to add any languages, we can do that: type /add and the name of the language;
• if you want to removes any languages from the list, we can also do that: type /remove and the name of the language;

or just press _start_ :3'''
