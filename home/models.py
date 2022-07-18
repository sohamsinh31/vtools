from django.db import models

# Create your models here.
class Product(models.Model):
    username = models.CharField(max_length=122)
    fileurl=models.CharField(max_length=122)
    filename = models.CharField(max_length=122)
    date = models.CharField(max_length=122)
