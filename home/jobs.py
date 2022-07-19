from calendar import month
import threading
import time
from schedule import Scheduler
import schedule
from .models import Product
from django.db.models import Q
from datetime import date, datetime
import os

def job():
    query = Product.objects.all()
    for product in query:
        a = datetime.now()
        d = datetime.strptime(product.date,'%m/%d/%Y %H:%M:%S')
        if a.day==d.day and a.month==d.month:
         sum = a.hour - d.hour
         if sum>=1:
            os.remove(product.fileurl)
            query2 = Product.objects.filter(Q(fileurl=product.fileurl))
            query2.delete()
        #  print(sum)


def job2():
    schedule.every(1).seconds.do(job)
    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
t = threading.Thread(target=job2,daemon=True)
t.start()
