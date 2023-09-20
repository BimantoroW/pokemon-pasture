from django.forms import ModelForm
from main.models import Item

class PokemonForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "owner", "description"]