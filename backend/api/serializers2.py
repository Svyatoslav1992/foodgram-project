#AleksandrUsolcev
from rest_framework import serializers

from recipes.models import IngredientRecipe, Ingredient, Recipe, Tag, ShoppingCart
from users.models import User, Follow

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField('get_subscribed_info')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_subscribed_info(self, obj):
        request = self.context.get('request')
        if request is None:
            return True
        if request.user.is_authenticated:
            subscribed = request.user.subscribed.filter(author=obj)
            return subscribed.exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientPatchCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)


class AmountIngredientSerializer(IngredientSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        exclude = ('ingredient', 'recipe')


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = TagSerializer(many=True)
    ingredients = AmountIngredientSerializer(many=True)
    author = UserListSerializer(required=True)
    is_favorited = serializers.SerializerMethodField('get_favorited_info')
    is_in_shopping_cart = serializers.SerializerMethodField('get_cart_info')

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_favorited_info(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            favorites = request.user.favorites.filter(recipe=obj)
            return favorites.exists()
        return False

    def get_cart_info(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            cart = request.user.cart.filter(recipe=obj)
            return cart.exists()
        return False


class RecipeShortSerializer(RecipeReadSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeWriteSerializer(RecipeReadSerializer):
    ingredients = IngredientPatchCreateSerializer(many=True)
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тег')
        array = []
        for ingredient in ingredients:
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Значение ингредиента должно быть больше 0')
            array.append(ingredient.get('id'))
        if len(array) != len(set(array)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться')
        if len(array) == 0:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        return data

    def add_ingredients(self, ingredients_list, recipe):
        amounts = [
            IngredientRecipe(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            ) for ingredient in ingredients_list
        ]
        IngredientRecipe.objects.bulk_create(amounts)

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        IngredientRecipe.objects.filter(recipe_id=instance.pk).delete()
        self.add_ingredients(ingredients, instance)
        super().update(instance, validated_data)
        return instance


class FollowListSerializer(UserListSerializer):
    recipes = serializers.SerializerMethodField('recipes_limit')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def recipes_limit(self, obj):
        request = self.context.get('request')
        queryset = obj.recipes.all()
        if request:
            recipes_limit = request.query_params.get('recipes_limit', None)
            if recipes_limit:
                queryset = queryset[:int(recipes_limit)]
        serializer = RecipeShortSerializer(queryset, many=True)
        return serializer.data

class AddToSerializer(serializers.Serializer):
    "Сериализатор для добавления в спискок покупок/избранное"

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
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

class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""
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