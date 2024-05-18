## gramguessr: что это и с чем его едят 
gramguessr - это образовательно-развлекательно-языковой бот, который поможет вам проверить свои знания в грамматике различных языков. 
- как это работает: бот выдаёт вам 20 рандомных грамматических фич какого-либо языка, и вы должны угадать сам язык, который загадал бот.
- какие языки у нас есть: мы добавили два режима игры.
  первый - языки ФиКЛа (шведский, иврит, французский, итальянский, немецкий, а также фантомные в год нашего набора, но вполне реальные в нашем боте - корейский и хинди!),
  второй - топ-10 языков по популярности изучения (английский, немецкий, испанский, французский, японский, корейский, итальянский, хинди, китайский и русский)
- что есть еще: ачивки, система жизней и рейтинг. а также вы можете узнать о фичах какого-нибудь языка, отправив боту соответствующую команду.

## как устроен репозиторий 
main.py -- это наш основной бото-код. там описаны все команды и всё-всё-всё, что надо для работы самого бота. 
langlists.py -- это два списка используемых языков.

папка data полностью посвящена табличке, из которой бот берёт всю информацию. 
- codes.csv, language_names.csv, parameters.csv, values.csv -- это csv таблички, скачанные прямиком с WALS. именно их мы склеивали между собой, чтобы получить финальную, красивую, рабочую табличку, который смог бы проанализировать наш бот.
- final_language_names.csv -- это таблица, в которой несколько отформатированы коды языков для корректной последующей склейки.
- draft.csv -- это наша финальная табличка для нужных нам языков, из которой бот берёт всю информацию.
- data_code.py -- код, который создал прекрасный файл из предыдущего пункта.

## как запустить код:
нужно
1. открыть терминал (перейти в нужную папку в командной строке или открыть встроенный терминал в pycharm) и ввести команду `python main.py`
2. начать диалог с @Gram_guessr_bot в telegram

## источники:
1. данные о языках: https://wals.info/
2. "каркас" бота мы брали отсюда: https://habr.com/ru/articles/442800/
3. отсюда кусочек, который отвечает на стикеры: https://qna.habr.com/q/1030694

## список участников
Колотева М.:
- реализована система жизней
- реализована рейтинговая система
- реализация функции вывода информации о языке
- реализация вывода фичей во время квиза

Спрукуль А.:
- (тут вся твоя работа)

Приймак А.:
вся работа с данными:
- проведен анализ гитхаба WALS и найдены все нужные таблицы для склеивания
- написан код, который корректно сшивает таблицы, убирает ненужные столбцы и фильтрует нужные для проекта языки
  
- написан readme
- сделана презентация
