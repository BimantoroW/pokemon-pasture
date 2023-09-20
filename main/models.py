from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    amount = models.IntegerField(default=1)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} - {self.owner}"
