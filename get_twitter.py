__author__ = 'Chandra S Narain Kappera'


from pprint import pprint
import requests, json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import urllib3

#Format
#{"importance": 0-10, "sentiment": positive/negative/neutral, "score":0-1}
#

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_sentiment(year, month, day):
    month_string = str(month)
    if len(month_string) < 2:
        month_string = "0" + month_string
    day_string = str(day)
    if len(day_string) < 2:
        day_string = "0" + day_string
    date = str(year) + month_string + day_string

    r1 = requests.get("http://archive.org/wayback/available?url=reddit.com/r/bitcoin&timestamp=" + date, verify=False)

    if(r1.status_code == 200):
        data1 = json.loads(r1.text)
        
        hasClosest = hasattr(data1['archived_snapshots'],'closest')
        hasUrl = hasattr(data1['archived_snapshots']['closest'],'url')
        
        if(hasattr(data1['archived_snapshots'],'closest')):
            archive_url  = None
        else:
            archive_url = data1['archived_snapshots']['closest']['url']
    else:
        archive_url = None
        print("Error return code = "+str(r1.status_code))

    fullUrl = "https://api.idolondemand.com/1/api/sync/analyzesentiment/v1?apikey=fe6dea49-084f-4cd8-be86-0976baf9a714&url=" + archive_url
    r2 = requests.get(fullUrl, verify=False)

    if(r2.status_code == 200):
        data2 = json.loads(r2.text)
        return data2['aggregate']['score']
    else:
        print("Error return code = "+str(r2.status_code))


def make_dict():
    scores = {}
    date = datetime.date(2016, 11, 27)
    #date = datetime.date.today()
    target = open('sentiment6.txt', 'a')
    for i in range(1000):
        print(str(date.day) + "." + str(date.month) + "." + str(date.year))
        stamp = date.year*10000+date.month*100+date.day
        value = get_sentiment(date.year, date.month, date.day)
        scores[(date.year, date.month, date.day)] = value
        date -= datetime.timedelta(days=1)
        target.write(str(stamp)+','+str(value))
        target.write('\n')
        target.flush()
    target.close()
make_dict()
