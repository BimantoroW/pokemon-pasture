import datetime
import json
from django.shortcuts import render
from .models import Pokemon, CaughtPokemon
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from main.forms import CreatePokemonForm, CatchPokemonForm, RegisterForm
from django.urls import reverse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login')
def show_main(request):
    items = CaughtPokemon.objects.filter(owner=request.user).order_by("pokemon__pokedex_number")

    amount = items.values_list("amount")
    total = 0
    for item in amount:
        total += item[0]

    context = {
        'name': request.user.username,
        'items': items,
        'total': total,
        'last_login': request.COOKIES['last_login'] if request != None else ""
    }

    return render(request, 'main.html', context)

@login_required(login_url='/login')
def create_pokemon(request):
    form = CreatePokemonForm(request.POST or None)
    
    error = False
    if form.is_valid() and request.method == "POST":
        query_set = Pokemon.objects.filter(name=form.cleaned_data['name'])
        if query_set.exists():
            error = True
        else:
            form.save()
            return HttpResponseRedirect(reverse('main:main'))
    
    context = {
        "form" : form,
        "has_error": error
    }

    return render(request, 'create_pokemon.html', context)

@login_required(login_url='/login')
def catch_pokemon(request):
    form = CatchPokemonForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        caught_pokemon = form.save(commit=False)
        caught_pokemon.owner = request.user
        query_set = CaughtPokemon.objects.filter(pokemon=caught_pokemon.pokemon, owner=caught_pokemon.owner)
        if query_set.exists():
            caught_pokemon = query_set.get(pokemon=caught_pokemon.pokemon)
            caught_pokemon.amount += 1
        caught_pokemon.save()
        return HttpResponseRedirect(reverse('main:main'))
    context = { 'form': form }
    return render(request, 'catch_pokemon.html', context)

def edit_pokemon(request, id):
    pokemon = Pokemon.objects.get(pk=id)
    form = CreatePokemonForm(request.POST or None, instance=pokemon)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:main'))
    context = {'form': form}
    return render(request, 'edit_pokemon.html', context)

def increment_pokemon(request, id):
    pokemon = CaughtPokemon.objects.get(pk=id)
    pokemon.amount += 1
    pokemon.save()
    return HttpResponseRedirect(reverse('main:main'))

def decrement_pokemon(request, id):
    pokemon = CaughtPokemon.objects.get(pk=id)
    pokemon.amount -= 1
    if pokemon.amount <= 0:
        pokemon.delete()
    else:
        pokemon.save()
    return HttpResponseRedirect(reverse('main:main'))

def remove_pokemon(request, id):
    pokemon = CaughtPokemon.objects.get(pk=id)
    pokemon.delete()
    return HttpResponseRedirect(reverse('main:main'))

def show_xml(request):
    data = Pokemon.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_json(request):
    data = Pokemon.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

@csrf_exempt
def show_caught_json(request):
    data = CaughtPokemon.objects.filter(owner=request.user)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_xml_by_id(request, id):
    data = Pokemon.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_json_by_id(request, id):
    data = Pokemon.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def get_all_pokemon_ajax(request):
    pokemon = Pokemon.objects.all()
    return HttpResponse(serializers.serialize('json', pokemon))

def get_caught_pokemon_ajax(request):
    caught_pokemon = CaughtPokemon.objects.filter(owner=request.user).order_by("pokemon__pokedex_number")
    return HttpResponse(serializers.serialize('json', caught_pokemon))

def get_pokemon_by_id(request, id):
    pokemon = Pokemon.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', pokemon))

@csrf_exempt
def create_pokemon_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pokedex_number = request.POST.get("pokedex_number")
        description = request.POST.get("description")

        if not Pokemon.objects.filter(name=name).exists():
            new_pokemon = Pokemon(name=name, pokedex_number=pokedex_number, description=description)
            new_pokemon.save()
        
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

@csrf_exempt
def catch_pokemon_ajax(request):
    if request.method == "POST":
        pk = request.POST.get("pokemon_pk")
        print("asdasd")
        pokemon = Pokemon.objects.get(pk=pk)
        caught_pokemon = CaughtPokemon(pokemon=pokemon)
        caught_pokemon.owner = request.user
        query_set = CaughtPokemon.objects.filter(pokemon=pokemon).filter(owner=request.user)
        if query_set.exists():
            caught_pokemon = query_set.get(pokemon=pokemon)
            caught_pokemon.amount += 1
        caught_pokemon.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def create_pokemon_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        Pokemon.objects.create(
            name = data["name"],
            pokedex_number = int(data["pokedex_number"]),
            description = data["description"]
        )

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def catch_pokemon_flutter(request):
    if request.method == 'POST':
        print('asdasd')
        data = json.loads(request.body)
        pokemon_set = Pokemon.objects.filter(name=data["name"])
        if pokemon_set.exists():
            caught_pokemon = CaughtPokemon(
                pokemon=pokemon_set.get(name=data["name"]),
                owner=request.user
            )
            caught_set = CaughtPokemon.objects.filter(pokemon=caught_pokemon.pokemon, owner=caught_pokemon.owner)
            if caught_set.exists():
                caught_pokemon = caught_set.get(pokemon=caught_pokemon.pokemon)
                caught_pokemon.amount += 1
            caught_pokemon.save()

            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "error"}, status=402)
    else:
        return JsonResponse({"status": "error"}, status=401)