#import telebot
import botModule as botM
from botModule import config
from _thread import start_new_thread
import datetime
from win10toast import ToastNotifier
import time
import requests as r
from bs4 import BeautifulSoup

class config:
    def __init__(self, minAmount, maxAmount, Value, url):
        self.minAmount = 0
        self.maxAmount = 100000
        self.Value = 2
        self.url = "https://funpay.ru/chips/62/"

def mainParser(config.Value, config.minAmount, config.maxAmount, config.url, newData, oldData):
    while True:
        toast = ToastNotifier()
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print("Подходящие лоты на", now )


        allAmount, allValue = [], []
        flag = True

        proxy = {'http': '193.86.201.109:4153',
             'http': '109.105.205.230:4145',
             'http': '82.137.224.193:8291',
             'http': '77.232.150.107:4153',
             'http': '20.52.37.89:16379',
             }
        page = r.get(config.url, proxies=proxy)
        print(page)
        if page.status_code != 200:
            print("Сайт не отвечает")
        

        source = BeautifulSoup(page.text, "html.parser") 

        amount = source.findAll('div', class_ = 'tc-amount')
        for count in amount[1:]:
            allAmount.append(count)
        price = source.findAll('div', class_ = 'tc-price')
        for rub in price[1:]:
            allValue.append(rub)
        print("Количество", "Цена", sep = "   ")
        for data in range(len(allAmount)):
            try:
                enteredAmount = ""
                for i in allAmount[data].text:
                    if i.isdigit(): enteredAmount += i
                if float(allValue[data].text[1:-3]) <= config.Value and int(enteredAmount) >= config.minAmount and int(enteredAmount) <= config.maxAmount:
                    print(allAmount[data].text, allValue[data].text[1:], sep = (abs(len(allAmount[data].text)-13))*" ")
                    if flag:
                        oldData = newData
                        newData = allAmount[data].text, allValue[data].text[1:]
                        if oldData != newData:
                            #toast.show_toast("kst_obd Notification","it's time to buy \n Amount: {0}, Price: {1}".format(allAmount[data].text,allValue[data].text[1:]),duration=10)
                            botM.bot.send_message(346860800, "Обнаружен новый лот по вашим параметрам \nКоличество: {0}. Цена: {1}".format(allAmount[data].text, allValue[data].text[1:]))
                            botM.bot.send_message(347767949, "Обнаружен новый лот по вашим параметрам \nКоличество: {0}. Цена: {1}".format(allAmount[data].text, allValue[data].text[1:]))
                        flag = False
            except ValueError:
                print('pagenation must by filled!')
                print(allAmount[data].text, allValue[data].text[1:])
        time.sleep(10)
        print("\n" * 100)


#message = botM.get_text_messages
newData, oldData = '', ''   


start_new_thread (mainParser, (config.Value, config.minAmount, config.maxAmount, config.config.url, newData, oldData))


botM.bot.polling(none_stop=True)