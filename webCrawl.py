from bs4 import BeautifulSoup
import requests
import urllib
from tabulate import tabulate

OGurl = "https://store.playstation.com/en-us/category/cf1645a7-a2e6-4151-8638-050cff3b1728/"
pageAmount = 23

def sortedSentence(Sentence):
    words = Sentence.split(" ")
    words.sort()
    newSentence = " ".join(words)
    return newSentence


bigList = []
headers = ["Consoles","Game","Discount Percent","Discount Price","Original Price"]
total = 0
for i in range(pageAmount):
    url = OGurl + str(i + 1)
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'lxml')

    priceInfo = soup.find_all("div", {"class": "ems-sdk-product-tile"})

    print(i)
    for item in soup.find_all("section", {"class": "ems-sdk-product-tile__details"}):
        print(item)

    for item in priceInfo:
        #linkTail = item.find('a')['href']

        if item.find_all("span", {"class": "psw-p-x-3xs ems-sdk-product-tile-image__badge"}) != None:
            consoleInfo = item.find_all("span", {"class": "psw-p-x-3xs ems-sdk-product-tile-image__badge"})

        if item.find("span", {"data-qa": "ems-sdk-product-tile-name"}) != None:
            gameTitle = item.find("span", {"data-qa": "ems-sdk-product-tile-name"}).text
        else:
            gameTitle = None

        if item.find("span", {"class": "psw-body-2 discount-badge discount-badge--undefined"}) != None:
            discountFactor = item.find("span", {"class": "psw-body-2 discount-badge discount-badge--undefined"}).text
        else:
            discountFactor = None

        if item.find("span", {"class": "price"}) != None:
            discountPrice = item.find("span", {"class": "price"}).text
        else:
            discountPrice = None

        if item.find("strike", {"class": "price price--strikethrough psw-m-l-xs"}) != None:
            originalPrice = item.find("strike", {"class": "price price--strikethrough psw-m-l-xs"}).text
        else:
            originalPrice = None

        if gameTitle != None:
            if len(gameTitle) > 70:
                print(gameTitle)
                gameTitle = gameTitle[0:60]

        consoleList = ""
        for console in consoleInfo:
            consoleList += console.text + " "

        if consoleList == "":
            consoleList = "Sub/DLC"

        if consoleList != "Sub/DLC" and consoleList != "":
            consoleList = sortedSentence(consoleList)

        bigList.append([consoleList,gameTitle,discountFactor,discountPrice,originalPrice])

bigList.sort(key = lambda x:str.lower(x[1]))
print(len(bigList))

print(tabulate(bigList, headers, tablefmt="github"))