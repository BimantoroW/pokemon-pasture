from django.contrib import admin
from .models import Pokemon, CaughtPokemon

# Register your models here.

admin.site.register(Pokemon)
admin.site.register(CaughtPokemon)
