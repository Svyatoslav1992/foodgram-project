from django_filters import (AllValuesMultipleFilter, CharFilter, NumberFilter,
                            rest_framework)
from recipes.models import Ingredient, Recipe


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для модели Recipe."""

    is_favorited = NumberFilter(
        method='get_is_favorited'
    )
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_in_shopping_cart = NumberFilter(
        method='get_is_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'tags', 'is_in_shopping_cart', ]

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(recipe_favourite__user_id=user.id)
        return queryset.all()

    def get_is_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(recipe_shopping_cart__user_id=user.id)
        return queryset.all()


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр для модели Ingredient."""

    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
