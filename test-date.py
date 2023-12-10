import datetime
import schedule
import time
import pygsheets
gc = pygsheets.authorize(service_account_file='./gsheet.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1cxvkIggrRHYnZy0oUH-leCFHy3gWdJGEi7XC3i1Hv3c/edit#gid=0')
wks_list = sht.sheet1
def job():
    date = str(datetime.datetime.now().date())
    wks_list.update_value('A1', date)
schedule.every().minute.at(":00").do(job)

#等待定時任務
while True:
    schedule.run_pending()
    time.sleep(1)
