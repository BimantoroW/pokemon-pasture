from django.shortcuts import render
from .models import Item

def show_main(request):
    # items = Item.objects.order_by("name")
    items = [
        Item(name="Charmander",
             owner="Red",
             amount=1,
             description="Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail.")
    ]
    context = {
        'items': items,
        'item_count': len(items)
    }
    return render(request, 'main.html', context)
