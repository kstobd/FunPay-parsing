import telebot
import botModule as botM
from _thread import start_new_thread
import datetime
from win10toast import ToastNotifier
import time
import requests as r
from bs4 import BeautifulSoup


def mainParser(message, Value, minAmount, maxAmount, url, newData, oldData):
    toast = ToastNotifier()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print("Подходящие лоты на", now )
    
    allAmount, allValue = [], []
    flag = True
    page = r.get(url)
    if page.status_code != 200:
        print("Сайт не отвечает")
        
    #print(page.status_code)

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
            if float(allValue[data].text[1:-3]) <= Value and int(enteredAmount) >= minAmount and int(enteredAmount) <= maxAmount:
                print(allAmount[data].text, allValue[data].text[1:], sep = (abs(len(allAmount[data].text)-13))*" ")
                if flag:
                    oldData = newData
                    newData = allAmount[data].text, allValue[data].text[1:]
                    if oldData != newData:
                        #toast.show_toast("kst_obd Notification","it's time to buy \n Amount: {0}, Price: {1}".format(allAmount[data].text,allValue[data].text[1:]),duration=10)
                        botM.bot.send_message(message.from_user.id, "Обнаружен новый лот по вашим параметрам \nКолличество: {0}, Цена: {1}".format(allAmount[data].text,allValue[data]))
                    flag = False
        except ValueError:
            print('pagenation must by filled!')
            print(allAmount[data].text, allValue[data].text[1:])
    time.sleep(10)
    print("\n" * 100)

message = botM.get_text_messages
newData, oldData = '', ''
minAmount, maxAmount, Value = 0, 100000, 2
url = "https://funpay.ru/chips/62/"



start_new_thread (mainParser, (Value, minAmount, maxAmount, url, newData, oldData, message))


botM.bot.polling(none_stop=True)