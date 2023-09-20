from django.shortcuts import render
from .models import Item
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import PokemonForm
from django.urls import reverse
from django.core import serializers

def show_main(request):
    items = Item.objects.all()

    amount = items.values_list("amount")
    total = 0
    for item in amount:
        total += item[0]

    context = {
        'items': items,
        'total': total
    }
    return render(request, 'main.html', context)

def catch_pokemon(request):
    form = PokemonForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        query_set = Item.objects.filter(name=form.cleaned_data['name']).filter(owner=form.cleaned_data['owner']).filter(description=form.cleaned_data['description'])
        if query_set.exists():
            pokemon = query_set.get(name=form.cleaned_data['name'])
            pokemon.amount += 1
            pokemon.save()
        else:
            form.save()
        return HttpResponseRedirect(reverse('main:main'))
    
    context = { "form" : form }
    return render(request, 'catch_pokemon.html', context)

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
