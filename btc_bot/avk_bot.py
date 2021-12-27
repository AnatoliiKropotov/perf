import telebot
import config
import json
import requests
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


#отправка сообщения о действиях пользователей
def feedback(message, func):
    if message.from_user.id != 491353015:
        t = f'Пользователь {message.from_user.first_name} aka {message.from_user.username} воспользовался функцией {func}'
        bot.send_message(chat_id = 491353015, text = t)


#запуск бота
@bot.message_handler(commands='start')
def start(message):
    graz = open('C:/Users/Анатолий/Desktop/py4e/graz.webp', 'rb')
    bot.send_sticker(message.chat.id, graz)
    bot.send_message(message.chat.id, "Поздравляю, бот запущен!")
    func = 'start'
    feedback(message, func)


#вызов списка команд
@bot.message_handler(commands='help')
def help_func(message):
    bot.send_message(message.chat.id, '''
Cписок команд:
/crypto - узнать стоимость криптовалюты
/my_id - узнать свой id
/you_awesome - сказать боту что он потрясающий
/about - об авторе
/help - посмотреть список команд ''')
    func = 'help_func'
    feedback(message, func)


#узнать свой id
@bot.message_handler(commands='my_id')
def id_func(message):
    bot.send_message(message.chat.id, f'твой id {message.from_user.id}')
    func = 'id_func'
    feedback(message, func)


#выбор криптовалютной пары
@bot.message_handler(commands='crypto')
def btc_func(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('биткоин/доллар', callback_data = 'BTC_USD')
    button2 = types.InlineKeyboardButton('биткоин/рубль', callback_data = 'BTC_RUB')
    button3 = types.InlineKeyboardButton('эфир/доллар', callback_data = 'ETH_USD')
    button4 = types.InlineKeyboardButton('эфир/рубль', callback_data = 'ETH_RUB')
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'выбери криптовалютную пару', reply_markup=markup)
    func = 'crypto'
    feedback(message, func)


#узнать цену криптовалюты
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    url = "https://api.exmo.com/v1.1/ticker"
    payload={}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text

    try:
        js = json.loads(data)
    except:
        bot.send_message(call.message.chat.id, 'не получилось')
    rate = int(float((js[call.data]['sell_price'])))

    if call.data == 'BTC_USD':
        a = 'биткоин'
        b = 'долларов'
    elif call.data == 'BTC_RUB':
        a = 'биткоин'
        b = 'рублей'
    elif call.data == 'ETH_USD':
        a = 'эфир'
        b = 'долларов'
    elif call.data == 'ETH_RUB':
        a = 'эфир'
        b = 'рублей'
    else:
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')
    bot.send_message(call.message.chat.id, f'1 {a} стоит {rate} {b}')
    bot.delete_message( chat_id=call.message.chat.id, message_id=call.message.message_id)


#информация о создателе
@bot.message_handler(commands='about')
def about_func(message):
    bot.send_message(message.chat.id, '''
AK_46
id 491353015
ak0391@yandex.ru''')
    func = 'about_func'
    feedback(message, func)

#ты потрясающий
@bot.message_handler(commands='you_awesome')
def awesome_func(message):
    keanu = open('C:/Users/Анатолий/Desktop/py4e/keanu.webp', 'rb')
    bot.send_sticker(message.chat.id, keanu)
    if message.from_user.username != None:
        bot.send_message(message.chat.id, f'нет, {message.from_user.username}, это ты потрясающий!')
    else:
        bot.send_message(message.chat.id, f'нет, {message.from_user.first_name}, это ты потрясающий!')
    func = 'awesome_func'
    feedback(message, func)


#чат-бот
@bot.message_handler(content_types=['text'])
def text_func(message):
    if message.text == 'Привет' or message.text == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, f'''Cорян, я всего лишь бездушная машина и
не понимаю о чём ты. Чтобы посмотреть список команд введи /help или просто /''')



bot.infinity_polling()
