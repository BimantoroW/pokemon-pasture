from django.shortcuts import render
from .models import Item

def show_main(request):
    items = Item.objects.order_by("name")
    context = {
        'items': items,
        'item_count': len(items)
    }
    return render(request, 'main.html', context)
