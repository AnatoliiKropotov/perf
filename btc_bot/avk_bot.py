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
@bot.message_handler(commands=['start'])
def start(message):
    graz = open('/home/akk1/graz.webp', 'rb')
    bot.send_sticker(message.chat.id, graz)
    bot.send_message(message.chat.id, "Поздравляю, бот запущен!")
    bot.send_message(message.chat.id, "/help - посмотреть список команд ")
    func = 'start'
    feedback(message, func)


#вызов списка команд
@bot.message_handler(commands=['help'])
def help_func(message):
    bot.send_message(message.chat.id, '''
Cписок команд:
/crypto - узнать стоимость криптовалюты
/currency - узнать стоимость валюты
/my_id - узнать свой id
/you_awesome - сказать боту что он потрясающий
/about - об авторе
/help - посмотреть список команд ''')
    func = 'help_func'
    feedback(message, func)


#узнать свой id
@bot.message_handler(commands=['my_id'])
def id_func(message):
    bot.send_message(message.chat.id, f'твой id {message.from_user.id}')
    func = 'id_func'
    feedback(message, func)


#выбор криптовалютной пары
@bot.message_handler(commands=['crypto'])
def btc_func(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('биткоин/доллар', callback_data = 'BTCUSD')
    button2 = types.InlineKeyboardButton('биткоин/рубль', callback_data = 'BTCRUB')
    button3 = types.InlineKeyboardButton('эфир/доллар', callback_data = 'ETHUSD')
    button4 = types.InlineKeyboardButton('эфир/рубль', callback_data = 'ETHRUB')
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'выбери криптовалютную пару', reply_markup=markup)
    func = 'crypto'
    feedback(message, func)

#выбор валютной пары
@bot.message_handler(commands=['currency'])
def cur_func(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('доллар/рубль', callback_data = 'USD')
    button2 = types.InlineKeyboardButton('евро/рубль', callback_data = 'EUR')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'выбери валютную пару', reply_markup=markup)
    func = 'currency'
    feedback(message, func)

#узнать цену, после нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # запрос на биржу Bitfinex
    def pair_r_quest(pair, number):
            url = "https://api-pub.bitfinex.com/v2/"
            pathParams = "tickers"
            queryParams = f"symbols=fUSD,t{pair}"

            response = requests.request("GET", url + pathParams + "?" + queryParams)

            data = response.text
            try:
                js = json.loads(data)
            except:
                bot.send_message(call.message.chat.id, 'не получилось')

            rate_pair = int(js[1][1])
            if number == 1:
                return rate_pair
            else:
                message(rate_pair)


    # запрос на сайт www.cbr-xml-daily.ru
    def currency_r_quest(currency, number):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        x = requests.get(url)
        data = x.text
        try:
            js = json.loads(data)
        except:
            bot.send_message(call.message.chat.id, 'не получилось')

        current_value = str(js["Valute"][currency]['Value'])
        current_rate = float(current_value[0:4])
        if number == 1:
            return current_rate
        else:
            message(current_rate)



    #считаем стоимость в рублях
    def rub_func(pair, currency, number):
        rate = int(float(pair_r_quest(pair, number) * currency_r_quest(currency,number)))
        message(rate)



    # вывод сообщения с ценой
    def message(rate):
        bot.send_message(call.message.chat.id, f'1 {a} стоит {rate} {b}')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)



    # распределяем кнопки
    number = 0
    if call.data == 'BTCUSD' or call.data == 'ETHUSD':
        if call.data == 'BTCUSD':
            a = 'биткоин'
            b = 'долларов'
            pair = call.data
            pair_r_quest(pair, number)
        elif call.data == 'ETHUSD':
            a = 'эфир'
            b = 'долларов'
            pair = call.data
            pair_r_quest(pair, number)
        else:
            bot.send_message(call.message.chat.id, 'Что-то пошло не так')

    elif call.data == 'USD' or call.data == 'EUR' :
        if call.data == 'USD':
            a = 'доллар'
            b = 'рублей'
            currency = call.data
            currency_r_quest(currency, number)

        elif call.data == 'EUR':
            a = 'евро'
            b = 'рублей'
            currency = call.data
            currency_r_quest(currency, number)

        else:
            bot.send_message(call.message.chat.id, 'Что-то пошло не так')

    elif call.data == 'BTCRUB' or call.data == 'ETHRUB':
        number = 1
        if call.data == 'BTCRUB':
            a = 'биткоин'
            b = 'рублей'
            pair = "BTCUSD"
            currency = "USD"
            rub_func(pair, currency, number)
        elif call.data == 'ETHRUB':
            a = 'эфир'
            b = 'рублей'
            pair = "ETHUSD"
            currency = "USD"
            rub_func(pair, currency, number)
        else:
            bot.send_message(call.message.chat.id, 'Что-то пошло не так')


    else:
        bot.send_message(call.message.chat.id, 'не получилось')




#информация о создателе
@bot.message_handler(commands=['about'])
def about_func(message):
    bot.send_message(message.chat.id, f'''
Aнатолий Кропотов
@{message.from_user.username}
ak0391@yandex.ru''')
    func = 'about_func'
    feedback(message, func)


#ты потрясающий
@bot.message_handler(commands=['you_awesome'])
def awesome_func(message):
    keanu = open('/home/akk1/keanu.webp', 'rb')
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
