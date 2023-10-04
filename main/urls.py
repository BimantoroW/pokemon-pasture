from django.urls import path
from main.views import show_main, show_json, show_json_by_id, show_xml, show_xml_by_id, register, login_user, logout_user, create_pokemon, catch_pokemon, increment_pokemon, decrement_pokemon, remove_pokemon, edit_pokemon

app_name = 'main'

urlpatterns = [
    path('', show_main, name='main'),
    path('create-pokemon/', create_pokemon, name='create_pokemon'),
    path('catch-pokemon/', catch_pokemon, name='catch_pokemon'),
    path('xml/', show_xml, name='xml'),
    path('xml/<int:id>', show_xml_by_id, name='xml_by_id'),
    path('json/', show_json, name='json'),
    path('json/<int:id>', show_json_by_id, name='json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('increment/<int:id>', increment_pokemon, name='increment'),
    path('decrement/<int:id>', decrement_pokemon, name='decrement'),
    path('remove/<int:id>', remove_pokemon, name='remove'),
    path('edit-pokemon/<int:id>', edit_pokemon, name='edit_pokemon')
]