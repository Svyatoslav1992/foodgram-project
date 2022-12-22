import io

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