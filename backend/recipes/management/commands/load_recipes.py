# from django.core.management import BaseCommand

# from recipes.models import Recipe


# class Command(BaseCommand):
#     help = 'Создаем рецепты'

#     def handle(self, *args, **kwargs):
#         data = [
#             {'name': 'Суп', 'text': 'Из семи залуп', 'image': 'https://avatars.mds.yandex.net/i?id=7ab3f5b759042e7890c08012ba6ab4a5-4032833-images-thumbs&n=13', 'cooking_time': '7', 'tags': 'завтрак', 'author': '', 'ingredients': ''},
#         ]
#         Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)
#         self.stdout.write(self.style.SUCCESS('Все рецепты созданы!'))

