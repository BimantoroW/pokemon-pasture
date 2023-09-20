from django.urls import path
from main.views import show_main, catch_pokemon, show_json, show_json_by_id, show_xml, show_xml_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='main'),
    path('catch-pokemon/', catch_pokemon, name='catch_pokemon'),
    path('xml/', show_xml, name='xml'),
    path('xml/<int:id>', show_xml_by_id, name='xml_by_id'),
    path('json/', show_json, name='json'),
    path('json/<int:id>', show_json_by_id, name='json_by_id'),
]