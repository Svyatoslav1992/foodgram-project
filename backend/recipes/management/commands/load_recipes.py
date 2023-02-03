from django.core.management import BaseCommand

from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Создаем рецепты'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Суп', 'text': 'Тот самый суп', 'image': 'https://avatars.mds.yandex.net/i?id=7ab3f5b759042e7890c08012ba6ab4a5-4032833-images-thumbs&n=13', 'cooking_time': '7', 'tags': 'завтрак', 'author': Ivan, 'ingredients': '[{ "id": 1123, "amount": 10}]'},
        ]
        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)
        self.stdout.write(self.style.SUCCESS('Все рецепты созданы!'))

