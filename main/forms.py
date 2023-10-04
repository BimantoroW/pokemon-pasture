from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from main.models import Pokemon, CaughtPokemon

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CreatePokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ["name", "pokedex_number", "description"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pokedex_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CatchPokemonForm(ModelForm):
    class Meta:
        model = CaughtPokemon
        fields = ["pokemon"]
        widgets = {
            'pokemon': forms.Select(attrs={'class': 'form-control'})
        }
    #pokemon = forms.ModelChoiceField(queryset=Pokemon.objects.order_by("pokedex_number"), required=True)