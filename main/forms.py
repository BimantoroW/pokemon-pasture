from django.forms import ModelForm
from django import forms
from main.models import Pokemon, CaughtPokemon

class CreatePokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ["name", "pokedex_number", "description"]

class CatchPokemonForm(ModelForm):
    class Meta:
        model = CaughtPokemon
        fields = ["pokemon"]
    pokemon = forms.ModelChoiceField(queryset=Pokemon.objects.order_by("pokedex_number"), required=True)