from fbchat import Client
from fbchat.models import *
import urllib3
from bs4 import BeautifulSoup
import datetime

client = Client("email", "pass")
groupId = 0;

http = urllib3.PoolManager()

zpravaList = []
url = "http://www.ssps.cz"
content = http.request("GET", url)
soup = BeautifulSoup(content.data)
day = "Default"
suplovani = "Nastala chyba, napiš tomu blbečkovi co to dělal"

def startSupl():
    for link in soup.find_all('a'):

        if getday() in link.text.strip():
            return getSupl(link.get("href").replace("#", ""))

def getSupl(tabNum):
    div = soup.find(id=tabNum)

    for sibling in div.li.next_siblings:
        if "3.C" in sibling.text:
            print(sibling.text)
            zpravaList.append(sibling.text)

    return zpravaList


def getday():

    dayNum = datetime.datetime.today().weekday() + 1

    if (dayNum == 1):
        day = "Pondělí"
    elif (dayNum == 2):
        day = "Úterý"
    elif (dayNum == 3):
        day = "Středa"
    elif (dayNum == 4):
        day = "Čtvrtek"
    elif (dayNum == 5):
        day = "Pátek"
    elif (dayNum == 6):
        day = "Pondělí"
    elif (dayNum == 7):
        day = "Pondělí"

    return day

while True:
    messages = client.fetchThreadMessages(groupId, 1)

    for message in messages:
        if "/supl" in str(message):
            zpravaList.clear()
            startSupl()
            client.reactToMessage(message.uid, MessageReaction.HEART)

            client.send(Message("V " + getday()), groupId, ThreadType.GROUP)
            for zprava in zpravaList:
                client.send(Message(zprava), groupId, ThreadType.GROUP)

        if "/gott" in str(message):
            client.sendLocalVoiceClips("trezor.mp3", message="", thread_id=groupId, thread_type=ThreadType.GROUP)
