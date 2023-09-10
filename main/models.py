from django.db import models

class Item:
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
