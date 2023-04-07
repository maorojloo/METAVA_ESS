from django.db import models
from persiantools.jdatetime import JalaliDate
import datetime
import pytz


dateNow=str(JalaliDate.today().strftime("%Y%m%d"))

class Subscriber(models.Model):
    email = models.EmailField(max_length=254)
    subscribeDate = models.CharField(max_length=8,default=dateNow)