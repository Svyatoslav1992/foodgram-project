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

        # Загрузка рецептов
        #recipes = [
        #    Recipe(
                # ingredients=[],
                # tags=[1, 2],
        #        image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        #        name='Суп',
         #       text='Супчик дня!',
         #       cooking_time='100',
         #   )
        #]
        #Recipe.objects.bulk_create(recipes)

        # tags = []
        # tags.append = (
        #     Tag(
        #         recipe=Recipe.objects.get(id=1),
        #         tag=Tag.objects.get(id=1)
        #     )
        # )
        # Tag.objects.bulk_create(tags)

        #recipe_ingredients = []
        #recipe_ingredients.append = (
         #   IngredientRecipe(
         #       recipe=Recipe.objects.get(id=1),
       #         ingredient=Ingredient.objects.get(id=200),
        #        amount=100
        #    )
        #)
       # IngredientRecipe.objects.bulk_create(recipe_ingredients)
        Ivan=User.objects.get(id=1)
        data = [

            {'name': 'Суп', 'text': 'Тот самый суп', 'image': 'https://avatars.mds.yandex.net/i?id=7ab3f5b759042e7890c08012ba6ab4a5-4032833-images-thumbs&n=13', 'cooking_time': '7', 'author_id': '1'},

        ]

        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)

        for recipe in Recipe.objects.all()
            recipe.tags.add(1)
    
        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))
