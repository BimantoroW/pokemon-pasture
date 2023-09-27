from django.db import models
from django.contrib.auth.models import User

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    pokedex_number = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"

class CaughtPokemon(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
