import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientRecipe, Recipe, ShoppingCart,
                            Tag, Favourite)
from users.models import Follow
from users.serializers import UsersSerializer

User = get_user_model()


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Ingredient только для чтения данных"
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Tag только для чтения данных"
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    "Сериализатор для вспомогательной модели IngredientRecipe"
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""

    tags = TagSerializer(many=True)
    author = UsersSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    @staticmethod
    def get_ingredients(obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(recipe=obj, user=request.user).exists()

    # def get_is_in_shopping_cart(self, obj):
    #     request = self.context.get('request')
    #     if not request or request.user.is_anonymous:
    #         return False
    #     return ShoppingCart.objects.filter(
    #         recipe=obj,
    #         user=request.user
    #     ).exists()


    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        shopping_cart = request.user.user_shopping_cart.filter(recipe=obj)
        return shopping_cart.exists()


class IngredientRecipeWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Количесто ингредиента не может быть меньше <=0'
            )
        return value

class RecipeWriteSerializer(serializers.ModelSerializer):
    "Сериализатор для добавления создания и изменения рецептов"
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True, allow_null=True)
    ingredients = IngredientRecipeWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create_ingredients(self, ingredients_list, recipe):
        amounts = [
            IngredientRecipe(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            ) for ingredient in ingredients_list
        ]
        IngredientRecipe.objects.bulk_create(amounts)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance

    def validate_ingredients(self, value):
        list = []
        for ing in value:
            ing_id = dict(ing).get('id')
            if ing_id in list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            list.append(ing_id)
        if not list:
            raise serializers.ValidationError(
                'В рецепте должны быть ингредиенты'
            )
        return value

    def validate_cooking_time(self, value):
        if value == 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше нуля.'
            )
        return value

    def validate_tags(self, value):
        list = []
        for tag in value:
            if tag in list:
                raise serializers.ValidationError(
                    'Теги не должны повторяться!'
                )
            list.append(tag)
        return value


class RecipeShortInfo(RecipeReadSerializer):
    """"Сериализатор рецептов  для отображения нужных полей"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AddToSerializer(serializers.Serializer):
    "Сериализатор для добавления в спискок покупок/избранное"

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortInfo(
            instance.recipe,
            context={'request': request}
        ).data

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = data.get('recipe')
        if ShoppingCart.objects.filter(recipe=recipe, user=user):
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в список покупок/избранное'
            )


class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes_author.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeShortInfo(
                Recipe.objects.filter(author=obj),
                many=True,
                context={'request': request}
            ).data
        return RecipeShortInfo(
            Recipe.objects.filter(author=obj)[:int(recipes_limit)],
            many=True,
            context={'request': request}
        ).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if not request or user.is_anonymous:
            return False
        subcribe = user.follower.filter(author=obj)
        return subcribe.exists()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('author', 'user')

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.author,
            context={'request': request}
        ).data

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        author = data.get('author')
        if Follow.objects.filter(user=user, author=author):
            raise serializers.ValidationError('Вы уже подписаны')
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя'
            )
        return data