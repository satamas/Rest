import datetime
from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)

    class Meta:
        unique_together = (('name', 'surname', 'patronymic'),)


class Complain(models.Model):
    customer = models.ForeignKey(Customer)
    message = models.TextField()
    complain_date = models.DateField(default=datetime.date.today)