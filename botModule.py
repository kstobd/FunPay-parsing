import telebot
import requests

bot = telebot.TeleBot('1745359273:AAG2SWO_CsIWNmKPSZHMWXZd2nVhyhQOK2k')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот по отслеживаню цен на сайте FunPay. Приятно познакомиться, {message.from_user.first_name}. Напшиши /help')
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, f'Достпуные команды: \n url, чтобы ввести новый адрес сканирования \n amount, чтобы создать ограничение на колличество товара \n price, чтобы создать ограничение на цену')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет! Напиши /help')
    elif message.text.lower() == 'url':
        bot.send_message(message.from_user.id, 'Отправте ссылку на товар из FunPay (вместе с http(s))')
        bot.register_next_step_handler(message, get_url)
    elif message.text.lower() == 'amount':
        bot.send_message(message.from_user.id, 'Отправьте два значения через пробел (1000 10000)')
        bot.register_next_step_handler(message, get_amount)
    elif message.text.lower() == 'price':
        bot.send_message(message.from_user.id, 'Отправьте максимальное значение цены на товар (если число вещественное, то записывайте его через точку (0.8))')
        bot.register_next_step_handler(message, get_price)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит. Введи /help')

def get_url(message):
    try:
        global url
        if "funpay.ru" in message.text:
            page = requests.get(message.text)
            if page.status_code == 200: 
                url = message.text
                bot.send_message(message.from_user.id, 'Ссылка успешно обновлена!')
            else:
                bot.send_message(message.from_user.id, "Сайт не отвечает, попробуйте позднее")
        else:
            bot.send_message(message.from_user.id, 'эта ссылка не из FunPay :( Отправь другую!')
            bot.register_next_step_handler(message, get_url)
    except BaseException:
        bot.send_message(message.from_user.id, "Ты что-то ввел не правильно. Введи еще раз")
        bot.register_next_step_handler(message, get_url)

def get_amount(message):
    try:
        global minAmount, maxAmount
        minAmount, maxAmount = [int(elem) for elem in message.text.split()]
        bot.send_message(message.from_user.id, 'Граничные значения успешно обновлены')
    except BaseException:
        bot.send_message(message.from_user.id, "Ты что-то ввел не правильно. Введи еще раз")
        bot.register_next_step_handler(message, get_amount)

def get_price(message):
    try:
        global Value
        Value = float(message.text)
        bot.send_message(message.from_user.id, 'Минимальная цена успешно обновлена')
    except BaseException:
        bot.send_message(message.from_user.id, "Ты что-то ввел не правильно. Введи еще раз")
        bot.register_next_step_handler(message, get_price)
    
bot.polling(none_stop=True)