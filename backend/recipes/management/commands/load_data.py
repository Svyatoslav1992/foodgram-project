import csv
from os import path
from random import randint

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

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
                password='1234',
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

        # Загрузка рецептов без тэгов и ингридиентов
        # https://www.russianfood.com/recipes/recipe.php?rid=102711
        image_recipes = SimpleUploadedFile('IMG_20230209_153016.jpg', content = open('/app/recipes/management/commands/IMG_20230209_153016.jpg').read() ,content_type='image/jpeg')
        recipes_1 = {'name': 'Суп «Харчо»',
                     'text': 'Тот самый суп',
                     'image': image_recipes,
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=141964
        recipes_2 = {'name': 'Куриный суп с вермишелью',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=153355
        recipes_3 = {'name': 'Тосканский суп с фаршем',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=130026
        recipes_4 = {'name': 'Сырный суп по‑французски, с курицей',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=156000
        recipes_5 = {'name': 'Томатный суп с курицей, фасолью и овощами',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=160235
        recipes_6 = {'name': 'Куриный суп с яйцом',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=91742
        recipes_7 = {'name': 'Суп картофельный с клецками',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=120468
        recipes_8 = {'name': 'Любимый суп',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=150580
        recipes_9 = {'name': 'Суп "Затируха" с курицей',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }
        # https://www.russianfood.com/recipes/recipe.php?rid=169194
        recipes_10 = {'name': 'Куриный суп с чесночными галушками',
                     'text': 'Тот самый суп',
                     'image': '',
                     'cooking_time': '7', 
                     'author_id': '1',
        }

        data = [
            recipes_1, recipes_2, recipes_3, recipes_4, recipes_5,
            recipes_6, recipes_7, recipes_8, recipes_9, recipes_10,
        ]

        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)

        # Загрузка тэгов в рецептах
        for recipe in Recipe.objects.all():
            recipe.tags.add(randint(1, 3))

        # Загрузка ингридиентов в рецептах
        recipe_ingredients = []
      
        # Рецепт 1
        id_recipes = Recipe.objects.get(id=1)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 2
        id_recipes = Recipe.objects.get(id=2)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 3
        id_recipes = Recipe.objects.get(id=3)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 4
        id_recipes = Recipe.objects.get(id=4)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 5
        id_recipes = Recipe.objects.get(id=5)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 6
        id_recipes = Recipe.objects.get(id=6)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 7
        id_recipes = Recipe.objects.get(id=7)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 8
        id_recipes = Recipe.objects.get(id=8)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 9
        id_recipes = Recipe.objects.get(id=9)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        # Рецепт 10
        id_recipes = Recipe.objects.get(id=10)
        add_ingredients = (
             IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            ),
            IngredientRecipe(
                recipe=id_recipes,
                ingredient=Ingredient.objects.get(id=randint(1, 2188)),
                amount= 10
            )
        )
        recipe_ingredients.extend(add_ingredients)

        IngredientRecipe.objects.bulk_create(recipe_ingredients)
        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))
