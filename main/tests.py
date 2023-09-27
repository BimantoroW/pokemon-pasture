from django.test import TestCase, Client
from .models import Pokemon

class userInterfaceTest(TestCase):
    def test_main_url_exists(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')

class modelTest(TestCase):
    def setUp(self):
        Pokemon.objects.create(name="smurf cat",
                            owner="the spectre",
                            amount=3,
                            description="we live we love we lie")
        
    def test_model_attributes(self):
        item = Pokemon.objects.get(name="smurf cat")
        self.assertEqual(item.name, "smurf cat")
        self.assertEqual(item.owner, "the spectre")
        self.assertEqual(item.amount, 3)
        self.assertEqual(item.description, "we live we love we lie")
