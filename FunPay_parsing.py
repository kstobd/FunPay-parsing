import datetime
from win10toast import ToastNotifier
import time
import requests as r
from bs4 import BeautifulSoup

newData, oldData = '', ''
while True:

    toast = ToastNotifier()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print("Подходящие лоты на", now )
    
    allValue, allAmount = [], []
    flag = True
    url = "https://funpay.ru/chips/62/"
    page = r.get(url)
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
            if float(allValue[data].text[1:-3]) <= 0.8 and int(allAmount[data].text) > 500:
                print(allAmount[data].text, allValue[data].text[1:], sep = (abs(len(allAmount[data].text)-13))*" ")
                if flag:
                    oldData = newData
                    newData = allAmount[data].text, allValue[data].text[1:]
                    if oldData != newData:
                        toast.show_toast("kst_obd Notification","it's time to buy \n Amount: {0}, Price: {1}".format(allAmount[data].text,allValue[data].text[1:]),duration=10)
                    flag = False
        except ValueError:
            print('pagenation must by filled!')
            print(allAmount[data].text, allValue[data].text[1:])
    time.sleep(10)
    print("\n" * 100)
