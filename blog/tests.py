import unittest

from django.test import TestCase, Client
from blog.models import Animal


# 单元测试
from blog.views import Test5


class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        # print(lion.speak())
        self.assertEqual(lion.speak(), "The lion says roar")
        self.assertEqual(lion.speak(), "The lion says meow")
        self.assertIsNone(lion.name)
        self.assertTrue(len(lion.name)==4)


# pipenv run python manage.py test blog.tests.SimpleTest
class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/api1/2/zhangsan/')
        print("response --> ", str(response.content, 'UTF-8'))
        print("-----------------------------")
        templates = response.templates
        for template in templates:
            print("template file name --> " + template.name )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['name']), 8)
        self.assertEqual(response.resolver_match.func.__name__, Test5.as_view().__name__)