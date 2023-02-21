from django.contrib.auth import get_user_model
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favourite, Ingredient, Recipe, ShoppingCart, Tag, IngredientRecipe
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from users.permissions import AuthorOrReadOnly

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, TagSerializer, RecipeShortInfo)
from api.utils import add_to, delete_from, download_cart
# from api.utils import add_to, delete_from





from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action



User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Для модели Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    # filter_backends = (DjangoFilterBackend, )
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Для модели Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Для модели Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = [DjangoFilterBackend]
    # filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly, )

    def perform_create(self, serializer):
        """Передает в поле author данные о пользователе."""

        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        """Удаляет объект класса рецепт."""

        instance.delete()

    def get_serializer_class(self):
        """Переопределение выбора сериализатора."""

        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )

    def shopping_cart(self, request, pk):
        """Метод для добавления/удаления из список покупок."""

        if request.method == 'POST':
            return add_to(self, ShoppingCart, request.user, pk)
        else:
            return delete_from(self, ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Метод для добавления/удаления из избранного."""

        if request.method == 'POST':
            return add_to(self, Favourite, request.user, pk)
        else:
            return delete_from(self, Favourite, request.user, pk)


class DownloadCart(APIView):
    """Вью для скачивания списка покупок."""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # list_ing = request.user.recipe_shopping_cart.values(
        list_ing = request.user.user_shopping_cart.values(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit'
        ).order_by('recipe__ingredients__ingredient__name').annotate(
            summ_amount=Sum('recipe__ingredients__amount'))
        return download_cart(list_ing)

# @action(detail=True, methods=['get', 'delete'],
#             permission_classes=[permissions.IsAuthenticated])
# def shopping_cart(self, request, pk=None):
#     if request.method == 'GET':
#         return self.add_obj(ShoppingCart, request.user, pk)
#     elif request.method == 'DELETE':
#         return self.delete_obj(ShoppingCart, request.user, pk)
#     return None

# @action(detail=False, methods=['get'],
#         permission_classes=[permissions.IsAuthenticated])
# def download_cart(self, request):
#     final_list = {}
#     ingredients = IngredientRecipe.objects.filter(
#         recipe__cart__user=request.user).values_list(
#         'ingredient__name', 'ingredient__measurement_unit',
#         'amount')
#     for item in ingredients:
#         name = item[0]
#         if name not in final_list:
#             final_list[name] = {
#                 'measurement_unit': item[1],
#                 'amount': item[2]
#             }
#         else:
#             final_list[name]['amount'] += item[2]
#     pdfmetrics.registerFont(
#         TTFont('Slimamif', 'Slimamif.ttf', 'UTF-8'))
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = ('attachment; '
#                                         'filename="shopping_list.pdf"')
#     page = canvas.Canvas(response)
#     page.setFont('Slimamif', size=24)
#     page.drawString(200, 800, 'Список ингредиентов')
#     page.setFont('Slimamif', size=16)
#     height = 750
#     for i, (name, data) in enumerate(final_list.items(), 1):
#         page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
#                                         f'{data["measurement_unit"]}'))
#         height -= 25
#     page.showPage()
#     page.save()
#     return response

# def add_obj(self, model, user, pk):
#     if model.objects.filter(user=user, recipe__id=pk).exists():
#         return Response({
#             'errors': 'Рецепт уже добавлен в список'
#         }, status=status.HTTP_400_BAD_REQUEST)
#     recipe = get_object_or_404(Recipe, id=pk)
#     model.objects.create(user=user, recipe=recipe)
#     serializer = CropRecipeSerializer(recipe)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# def delete_obj(self, model, user, pk):
#     obj = model.objects.filter(user=user, recipe__id=pk)
#     if obj.exists():
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     return Response({
#         'errors': 'Рецепт уже удален'
#     }, status=status.HTTP_400_BAD_REQUEST)