import csv
from os import path
from random import randint

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe
# from mimesis import Person
# from mimesis.locales import Locale
from users.models import User

person = Person(locale=Locale.RU)


class Command(BaseCommand):
    """Загружает тестовые данные."""

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
        # users = []
        # for _ in range(5):
        #     users.append(
        #         User(
        #             username=person.username(mask='l'),
        #             first_name=person.first_name(gender='male'),
        #             last_name=person.last_name(gender='male'),
        #             email=person.email(gender='male'),
        #             password=person.password(length=8)
        #         )
        #     )
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
        # recipes = []
        # for _ in range(10):
        #     random_author = User.objects.get(id=randint(1,3))
        #     recipes.append(
        #         Recipe(
        #             author=random_author,
        #             name=
        #         )
        #     )

        # Recipe.objects.bulk_create(recipes)

        # recipe_ingredients = []
        # for _ in range(1):
        #     random_recipe = Recipe.objects.get(id=1)
        #     random_ingredient = Ingredient.objects.get(id=randint(1, 2000))
        #     random_amount = randint(1,100)

        #     recipe_ingredients.append(
        #         IngredientRecipe(
        #             recipe=random_recipe,
        #             ingredient=random_ingredient,
        #             amount=random_amount
        #         )
        #     )
        # IngredientRecipe.objects.bulk_create(recipe_ingredients)



        # recipe_ingredients.append = (
        #     id=1,
        #     ingredient=1,
        #     amount=10
        # )
        # IngredientRecipe.objects.bulk_create(recipe_ingredients)
        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))