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
# from api.utils import add_to, delete_from, download_cart
from api.utils import add_to, delete_from

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Для модели Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
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


# class DownloadCart(APIView):
#     """Вью для скачивания списка покупок."""
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         list_ing = request.user.user_shopping_cart.values(
#             'recipe__ingredients__ingredient__name',
#             'recipe__ingredients__ingredient__measurement_unit').order_by(
#             'recipe__ingredients__ingredient__name').annotate(
#             total=Sum('recipe__ingredients__amount'))
#         return download_cart(list_ing)
