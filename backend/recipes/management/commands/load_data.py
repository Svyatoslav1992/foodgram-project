import csv
from os import path
from random import randint

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe
from django.core.files.uploadedfile import SimpleUploadedFile
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

        image1 = open('MG_20230209_153016.jpg')

        data = [

            {'name': 'Суп1', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп2', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп3', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '1'},
            {'name': 'Суп4', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп5', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп6', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '2'},
            {'name': 'Суп7', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп8', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп9', 'text': 'Тот самый суп', 'image': '', 'cooking_time': '7', 'author_id': '3'},
            {'name': 'Суп10', 'text': 'Тот самый суп', 'image': image1, 'cooking_time': '7', 'author_id': '3'},

        ]

        image1.close()

        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)

        for recipe in Recipe.objects.all():
            recipe.tags.add(randint(1, 3))

        recipe_ingredients = []
        # for _ in range(30):
        random_recipe = Recipe.objects.get(id=10)
        random_ingredient = Ingredient.objects.get(id=randint(1, 2188))
        random_amount = randint(1, 100)
        print(random_recipe, random_ingredient, random_amount)
        #     recipe_ingredients.append(
        #         IngredientRecipe(
        #             recipe=random_recipe,
        #             ingredient=random_ingredient,
        #             amount=random_amount
        #         ),
        #     )
        recipe_ingredients.append(
            IngredientRecipe(
                recipe=random_recipe,
                ingredient=random_ingredient,
                amount=random_amount
            ),
        )

        IngredientRecipe.objects.bulk_create(recipe_ingredients)
        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))
