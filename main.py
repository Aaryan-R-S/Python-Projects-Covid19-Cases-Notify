import time
from plyer import notification
import requests
from bs4 import BeautifulSoup
from bs4 import Comment

def getData(url):
    response = requests.get(url)
    return response.content

def modifyData(response):
    mySoup = BeautifulSoup(response, 'html.parser')
    comments = mySoup.find_all(string=lambda text: isinstance(text, Comment))
    strCase = ""
    for c in comments:
        if 'tbody' in c:
            c = c.replace("</td>", "")
            c = c.replace("<td>", "")
            c = c.replace("<tr>", "")
            c = c.replace("</tr>", "")
            c = c.replace("</strong>", "")
            c = c.replace("<strong>", "")
            c = c.replace("<tbody>", "")
            c = c.replace('<td colspan="1"><span>', "")
            c = c.replace("#</span>", "")
            c = c.replace('<td align = "right" style = "text-align:right;">', "")
            c = c.replace("\t", "")
            c = c.replace("\n\n\n\n", " | ")
            c = c.replace("\n\n\n", " | ")
            c = c.replace("\n\n", " | ")
            c = c.replace("\n", " | ")
            c = c.replace("     ", "")
            strCase += c
    l = strCase.split(" | ")

    while "" in l:
        l.remove("")
    
    lnew = []
    while len(l) >= 5:
        lsmall = []
        l.remove(l[0])
        for i in range(4):
            lsmall.append(l[i])
        for i in range(4):
            l.remove(l[0])
        lnew.append(lsmall)
    lnew[len(lnew)-1].append(l[0])
    lnew[len(lnew)-1].remove(lnew[len(lnew)-1][0])
    l.remove(l[0])

    return lnew

def notifyCases(array2d, state):
    array2dEntry = None
    for i in array2d:
        if state in i:
            array2dEntry = i
    if array2dEntry[0]=='Total':
        array2dEntry[0] = 'India'

    notification.notify(
        title = "COVID-19 Cases in India",
        message = f"\t{array2dEntry[0]}\nTotal Cases : {array2dEntry[2]}\nActive Cases : {array2dEntry[1]}\nNew Cases : {array2dEntry[3]}",
        app_icon = "D:\My Files\Complete Python Course\Projects\covid cases notify\\virus.ico",
        timeout = 15
    )

if __name__ == "__main__":
    state = input("\nEnter name of 'State' of India or 'Total' for Indian COVID-19 Cases:\n ")
    notifyCases(modifyData(getData("https://www.mohfw.gov.in/")), state)
    print(" ")


