from django.core.management import BaseCommand

from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Создаем рецепты'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Суп', 'text': 'Из семи залуп', 'image': 'https://avatars.mds.yandex.net/i?id=7ab3f5b759042e7890c08012ba6ab4a5-4032833-images-thumbs&n=13', 'cooking_time': '7', 'tags': 'завтрак', 'author': 'Ivan', 'ingredients': ''},
        ]
        Recipe.objects.bulk_create(Recipe(**recipes) for recipes in data)
        self.stdout.write(self.style.SUCCESS('Все рецепты созданы!'))


# class Recipe(models.Model):
#     name = models.CharField(
#         verbose_name='Название',
#         max_length=50
#     )
#     text = models.TextField(
#         verbose_name='Описание'
#     )
#     image = models.ImageField(
#         verbose_name='Изображение',
#         upload_to='images/',
#         null=True,
#         default=None
#     )
#     cooking_time = models.PositiveSmallIntegerField(
#         verbose_name='Время приготовления в минутах',
#         validators=(
#             MinValueValidator(
#                 1,
#                 'Блюдо уже готово!'
#             ),
#         )
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         verbose_name='Теги'
#     )
#     author = models.ForeignKey(
#         User,
#         verbose_name='Автор',
#         on_delete=models.CASCADE,
#         related_name='recipes_author'
#     )
#     ingredients = models.ManyToManyField(
#         "Ingredient",
#         verbose_name='Ингредиенты'
#     )
#     pub_date = models.DateTimeField(
#         verbose_name='Дата публикации',
#         auto_now_add=True
#     )