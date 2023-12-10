import datetime
import schedule
import time
import calendar

import requests
from bs4 import BeautifulSoup
import pandas as pd

def respond(url, page):
    response = requests.get(url + str(page), timeout=10)
    response.encoding="utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('div', class_ ='blog-entry-inner clr')

#公告-本周 榮譽-前兩周 競賽-前兩月
def crawler():
    url_ann = "https://www.mksh.phc.edu.tw/category/post-a/page/"
    url_honor = "https://www.mksh.phc.edu.tw/category/post-a/a01-post-honor-roll/page/"
    url_comp = "https://www.mksh.phc.edu.tw/category/post-outer-school/f02-%e5%ad%b8%e7%94%9f%e7%a0%94%e7%bf%92%e8%88%87%e7%ab%b6%e8%b3%bd/page/"
    
    year_now = datetime.datetime.now().date().year
    month_now = datetime.datetime.now().date().month
    weekday_now = datetime.datetime.now().date().weekday()
    day_now = datetime.datetime.now().date().day
    
    time_lim = True
    page = 1
    while time_lim:
        announcement = respond(url_ann, page)
        for ann in announcement:
            date = ann.li.text[15:]
            weekday = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
            if weekday <= weekday_now:
                print(weekday, page)
            if weekday == 0:
                time_lim = False
                break
        page += 1

    time_lim = True
    page = 1
    while time_lim:
        honor = respond(url_honor, page)
        for hn in honor:
            month = int(hn.li.text[20:22])
            day = int(hn.li.text[23:])
            if month == month_now:
                if day >= day_now - 14:
                    print(day, page)
                else:
                    time_lim = False
                    break
            else:
                if month_now == 1:
                    day_now = datetime.datetime.now().date().day + 31
                else:
                    first_day_of_week, days_in_month = calendar.monthrange(year_now, month_now-1)
                    day_now = datetime.datetime.now().date().day + days_in_month
                if day >= day_now - 14:
                    print(day, page)
                else:
                    time_lim = False
                    break
        page += 1

    time_lim = True
    page = 1
    while time_lim:
        competition = respond(url_comp, page)
        for comp in competition:
            month = int(comp.li.text[20:22])
            if month_now == 1:
                if (month == 11) or (month == 12) or (month == 1):
                    print(month, page)
                else:
                    time_lim = False
                    break

            elif month_now == 2:
                if (month == 12) or (month == 1) or (month == 2):
                    print(month, page)
                else:
                    time_lim = False
                    break

            else:
                if month >= month_now-2:
                    print(month, page)
                else:
                    time_lim = False
                    break

        page += 1

"""需求
月份/2星期 榮譽
星期 重要
年度 競賽
"""

#每隔8小時執行一次
schedule.every(8).hours.at(":00").do(crawler)

#先執行一次
schedule.run_all()

#等待定時任務
while True:
    schedule.run_pending()
    time.sleep(1)