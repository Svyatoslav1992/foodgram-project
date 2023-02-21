import io
from io import BytesIO

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from api.serializers import AddToSerializer
from foodgram import settings
from recipes.models import Recipe


def add_to(self, model, user, pk):
    """Метод для добавления"""
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response({'error': 'Рецепт/Подписка уже добавлен(а)'},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, pk=pk)
    instance = model.objects.create(user=user, recipe=recipe)
    serializer = AddToSerializer(instance)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def delete_from(self, model, user, pk):
    """Метод для удаления"""
    if model.objects.filter(user=user, recipe__id=pk).exists():
        model.objects.filter(
            user=user, recipe__id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# def download_cart(cart):
#     """ Выгрузка списка покупок в pdf """

#     buffer = BytesIO()
#     can = canvas.Canvas(buffer)

#     SANS_REGULAR = settings.STATIC_ROOT + '/fonts/OpenSans-Regular.ttf'
#     SANS_REGULAR_NAME = 'OpenSans-Regular'
#     SANS_BOLD = settings.STATIC_ROOT + '/fonts/OpenSans-Bold.ttf'
#     SANS_BOLD_NAME = 'OpenSans-Bold'

#     FILE_NAME = 'shopping_list.pdf'

#     pdfmetrics.registerFont(TTFont(SANS_REGULAR_NAME, SANS_REGULAR))
#     pdfmetrics.registerFont(TTFont(SANS_BOLD_NAME, SANS_BOLD))
#     can.setTitle('Список покупок')

#     can.setFont(SANS_BOLD_NAME, 32)
#     can.drawString(100, 750, 'foodgram')
#     can.setFont(SANS_REGULAR_NAME, 13)
#     can.drawString(100, 725, 'Ваш продуктовый помощник')
#     can.line(100, 715, 500, 715)
#     can.setFont(SANS_BOLD_NAME, 13)
#     can.drawString(393, 700, 'cписок покупок')
#     can.setFont(SANS_REGULAR_NAME, 10)

#     padding_top = 680
#     page_number = 1
#     steps = len(cart)
#     last_step = steps - 1
#     for step, ingredient in enumerate(cart):
#         ingredient = list(ingredient.values())
#         if step == last_step and steps >= 3:
#             x = padding_top - 20
#             can.line(100, x, 500, x)
#             can.setFont(SANS_BOLD_NAME, 13)
#             can.drawString(362, x - 15, 'приятного аппетита')
#             can.setFont(SANS_REGULAR_NAME, 10)
#         if padding_top <= 80:
#             can.showPage()
#             can.line(100, 770, 500, 770)
#             can.setFont(SANS_BOLD_NAME, 13)
#             can.drawString(393, 755, 'cписок покупок')
#             can.setFont(SANS_REGULAR_NAME, 10)
#             page_number += 1
#             padding_top = 735
#             can.drawString(100, 780, f'стр. {page_number}')
#         product = ingredient[0]
#         unit = ingredient[1]
#         total = ingredient[2]
#         string = f'{step+1}. {product[0:48]} ({unit[0:10]}) — {total}'
#         can.drawString(100, padding_top, string)
#         padding_top -= 19

#     can.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=FILE_NAME)

def download_cart(list_ing):
    SANS_REGULAR = settings.STATIC_ROOT + '/fonts/OpenSans-Regular.ttf'
    SANS_REGULAR_NAME = 'OpenSans-Regular'
    SANS_BOLD = settings.STATIC_ROOT + '/fonts/OpenSans-Bold.ttf'
    SANS_BOLD_NAME = 'OpenSans-Bold'

    pdfmetrics.registerFont(TTFont(SANS_REGULAR_NAME, SANS_REGULAR))
    pdfmetrics.registerFont(TTFont(SANS_BOLD_NAME, SANS_BOLD))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont(SANS_BOLD_NAME, 32)
    c.drawString(30, 775, 'Foodgram')

    c.setFont(SANS_REGULAR_NAME, 20)
    c.drawString(30, 740, 'Ваш продуктовый помошник')
    c.line(30, 730, 580, 730)

    c.drawString(30, 710, 'Список покупок')
    val = 680
    for step, ing in enumerate(list_ing):
        ingredient = list(ing.values())
        product = ingredient[0]
        unit = ingredient[1]
        amount = ingredient[2]
        string = f'{step+1}. {product} {unit} - {amount}'
        c.drawString(30, val, string)
        val -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='shoppcart_list.pdf'
    )