from datetime import datetime
from django.db import models

# Create your models here.
class Post(models.Model):
    boardSrl = models.AutoField(primary_key=True)

    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(max_length=10000, null=True, blank=True)
    viewCnt = models.IntegerField(null=True, blank=True, default=0)
    recommendCnt = models.IntegerField(null=True, blank=True, default=0)
    password = models.CharField(max_length=16)


    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def store(self):
        self.save()
        return self

    def get_write_day(self):
        return self.createdAt.time() if self.createdAt.date() == datetime.today().date() else str((datetime.today().date() - self.createdAt.date()).days) + ' 일전'

    def get_write_time(self):
        return self.createdAt.strftime('%Y. %m. %d %H:%M')

