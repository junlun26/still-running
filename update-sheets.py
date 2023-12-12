import datetime
import schedule
import time
import calendar
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pygsheets

def respond(url, page):
    response = requests.get(url + str(page), timeout=10)
    response.encoding="utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('div', class_ ='blog-entry-inner clr')

def update_sheets(dataframe, sheet):
    gc = pygsheets.authorize(service_account_file='./gsheet.json')
    sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1cxvkIggrRHYnZy0oUH-leCFHy3gWdJGEi7XC3i1Hv3c/edit#gid=0')
    wks = sht[sheet]
    wks.clear()
    wks.set_dataframe(dataframe, (0, 0))

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
        df = pd.DataFrame(columns=["informations","web site"])
        for ann in announcement:
            date = ann.li.text[15:]
            weekday = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
            if weekday <= weekday_now:
                df.loc[len(df)] = [ann.a.text[2:], ann.a['href']]
            if weekday == 0:
                time_lim = False
                update_sheets(df, 0)
                break
        page += 1

    time_lim = True
    page = 1
    while time_lim:
        honor = respond(url_honor, page)
        df = pd.DataFrame(columns=["informations","web site"])
        for hn in honor:
            month = int(hn.li.text[20:22])
            day = int(hn.li.text[23:])
            if month == month_now:
                if day >= day_now - 14:
                    df.loc[len(df)] = [hn.a.text[2:], hn.a['href']]
                else:
                    time_lim = False
                    update_sheets(df, 1)
                    break
            else:
                if month_now == 1:
                    day_now = datetime.datetime.now().date().day + 31
                else:
                    first_day_of_week, days_in_month = calendar.monthrange(year_now, month_now-1)
                    day_now = datetime.datetime.now().date().day + days_in_month
                if day >= day_now - 14:
                    df.loc[len(df)] = [hn.a.text[2:], hn.a['href']]
                else:
                    time_lim = False
                    update_sheets(df, 1)
                    break
        page += 1

    time_lim = True
    page = 1
    while time_lim:
        competition = respond(url_comp, page)
        df = pd.DataFrame(columns=["informations","web site"])
        for comp in competition:
            month = int(comp.li.text[20:22])
            if month_now == 1:
                if (month == 11) or (month == 12) or (month == 1):
                    df.loc[len(df)] = [comp.a.text[2:], comp.a['href']]
                else:
                    time_lim = False
                    update_sheets(df, 2)
                    break
            elif month_now == 2:
                if (month == 12) or (month == 1) or (month == 2):
                    df.loc[len(df)] = [comp.a.text[2:], comp.a['href']]
                else:
                    time_lim = False
                    update_sheets(df, 2)
                    break
            else:
                if month >= month_now-2:
                    df.loc[len(df)] = [comp.a.text[2:], comp.a['href']]
                else:
                    time_lim = False
                    update_sheets(df, 2)
                    break
        page += 1

    print("done")

schedule.every().minute.at(":00").do(crawler)

#schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)
