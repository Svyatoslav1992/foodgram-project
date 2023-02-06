import csv
from os import path
from random import randint

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe

from users.models import User


class Command(BaseCommand):
    """Загружает тестовые данные."""
    # Загрузка ингридиентов
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем загрузку тестовых данных'))

        # Загрузка ингредиентов
        filename = path.join('.', 'data', 'ingredients.csv')
        try:
            with open(filename, 'r', encoding='UTF-8') as file:
                data = csv.reader(file)
                for row in data:
                    name, measure = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measure
                    )
        except FileNotFoundError as error:
            raise CommandError(error)

        # Загрузка пользователей
        users = [
            User(
                username='Ivan',
                first_name='Иван',
                last_name='Труха',
                email='Ivan@gmail.com',
                password='1q2w3e4r',
            ),
            User(
                username='Slava',
                first_name='Слава',
                last_name='Киин',
                email='Svyatoslav@gmail.com',
                password='1q2w3e4r',
                ),
            User(
                username='Darya',
                first_name='Дарья',
                last_name='Ан',
                email='Darya@gmail.com',
                password='1q2w3e4r',
            )
        ]
        User.objects.bulk_create(users)

        # Загрузка тэгов
        tag = [
            Tag(id=1, name='Завтрак', color='#E26C2D', slug='breakfast'),
            Tag(id=2, name='Обед', color='#49B64E', slug='dinner'),
            Tag(id=3, name='Ужин', color='#8775D2', slug='supper'),
        ]
        Tag.objects.bulk_create(tag)

       
        data = [

            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},

        ]

        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)

        for recipe in Recipe.objects.all():
            recipe.tags.add(randint(1,3))

        recipe_ingredients = []
        recipe_ingredients.extend(
            IngredientRecipe(
                recipe=Recipe.objects.get(id=1),
                ingredient=Ingredient.objects.get(id=101),
                amount=100
            ),
            IngredientRecipe(
                recipe=Recipe.objects.get(id=1),
                ingredient=Ingredient.objects.get(id=102),
                amount=100
            ),
            IngredientRecipe(
                recipe=Recipe.objects.get(id=2),
                ingredient=Ingredient.objects.get(id=103),
                amount=100
            ),
            IngredientRecipe(
                recipe=Recipe.objects.get(id=3),
                ingredient=Ingredient.objects.get(id=104),
                amount=100
            ),




        )
        IngredientRecipe.objects.bulk_create(recipe_ingredients)

        print(Recipe.objects.get(id=1))

        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))
