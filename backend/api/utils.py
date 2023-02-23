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

import io

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.aggregates import Count, Sum
from django.db.models.expressions import Exists, OuterRef, Value
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework import permissions, viewsets

User = get_user_model()
FILENAME = 'shoppingcart.pdf'


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


# def download_cart(list_ing):
#     SANS_REGULAR = settings.STATIC_ROOT + '/fonts/OpenSans-Regular.ttf'
#     SANS_REGULAR_NAME = 'OpenSans-Regular'
#     SANS_BOLD = settings.STATIC_ROOT + '/fonts/OpenSans-Bold.ttf'
#     SANS_BOLD_NAME = 'OpenSans-Bold'

#     pdfmetrics.registerFont(TTFont(SANS_REGULAR_NAME, SANS_REGULAR))
#     pdfmetrics.registerFont(TTFont(SANS_BOLD_NAME, SANS_BOLD))

#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer)

#     c.setFont(SANS_BOLD_NAME, 32)
#     c.drawString(30, 775, 'Foodgram')

#     c.setFont(SANS_REGULAR_NAME, 20)
#     c.drawString(30, 740, 'Ваш продуктовый помошник')
#     c.line(30, 730, 580, 730)

#     c.drawString(30, 710, 'Список покупок')
#     val = 680
#     for step, ing in enumerate(list_ing):
#         ingredient = list(ing.values())
#         product = ingredient[0]
#         unit = ingredient[1]
#         amount = ingredient[2]
#         string = f'{step+1}. {product} {unit} - {amount}'
#         c.drawString(30, val, string)
#         val -= 20

#     c.showPage()
#     c.save()
#     buffer.seek(0)
#     return FileResponse(
#         buffer,
#         as_attachment=True,
#         filename='shoppcart_list.pdf'
#     )


@action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,))
def download_shopping_cart(self, request):
    """Качаем список с ингредиентами."""

    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    x_position, y_position = 50, 800
    shopping_cart = (
        request.user.user_shopping_cart.recipe.
        values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__amount')).order_by())
    page.setFont('Vera', 14)
    if shopping_cart:
        indent = 20
        page.drawString(x_position, y_position, 'Cписок покупок:')
        for index, recipe in enumerate(shopping_cart, start=1):
            page.drawString(
                x_position, y_position - indent,
                f'{index}. {recipe["ingredients__name"]} - '
                f'{recipe["amount"]} '
                f'{recipe["ingredients__measurement_unit"]}.')
            y_position -= 15
            if y_position <= 50:
                page.showPage()
                y_position = 800
        page.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename=FILENAME)
    page.setFont('Vera', 24)
    page.drawString(
        x_position,
        y_position,
        'Cписок покупок пуст!')
    page.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=FILENAME)