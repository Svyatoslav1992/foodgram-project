# это база
import base64


import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
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

#############################################################


# class IngredientSerializer(serializers.ModelSerializer):
#     "Сериализатор для модели Ingredient"
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


# class TagSerializer(serializers.ModelSerializer):
#     "Сериализатор для модели Tag"
#     color = Hex2NameColor()

#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    "Сериализатор для вспомогательной модели IngredientRecipe"
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = 'id', 'name', 'measurement_unit', 'amount',



# class RecipeReadSerializer(serializers.ModelSerializer):
#     "Сериализатор для модели Recipe для чтения и записи данных"
#     is_favorited = serializers.SerializerMethodField(read_only=True)
#     is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
#     author = UsersSerializer(read_only=True)

#     ingredients = serializers.SerializerMethodField(read_only=True)
#     image = Base64ImageField(required=True, allow_null=True)
#     tags = TagSerializer(many=True)


#     def get_ingredients(self, obj):
#         queryset = IngredientRecipe.objects.filter(recipe=obj)
#         return IngredientRecipeSerializer(queryset, many=True).data

#     def get_is_favorited(self, obj):
#         request = self.context.get('request')
#         if request.user.is_anonymous:
#             return False
#         favorite = request.user.user_favourite.filter(recipe=obj)
#         return favorite.exists()

#     def get_is_in_shopping_cart(self, obj):
#         request = self.context.get('request')
#         if request.user.is_anonymous:
#             return False
#         shopping_cart = request.user.user_shopping_cart.filter(recipe=obj)
#         return shopping_cart.exists()

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time'
#         )


# class IngredientRecipeWriteSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=True)
#     amount = serializers.IntegerField(required=True)

#     def validate_amount(self, value):
#         if value <= 0:
#             raise serializers.ValidationError(
#                 'Количесто ингредиента не может быть меньше <=0'
#             )
#         return value

    # class Meta:
    #     model = IngredientRecipe
    #     fields = 'id', 'amount',

# class AddIngredientSerializer(serializers.ModelSerializer):
#     """Сериализатор для добавления ингредиентов."""

#     id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
#     amount = serializers.IntegerField()

#     class Meta:
#         model = IngredientRecipe
#         fields = 'id', 'amount',

# class RecipeWriteSerializer(serializers.ModelSerializer):
#     """Сериализатор с краткой информацией о рецепте."""

#     tags = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Tag.objects.all()
#     )
#     image = Base64ImageField(required=True, allow_null=True)
#     # ingredients = IngredientRecipeWriteSerializer(many=True)
#     ingredients = AddIngredientSerializer(many=True)

#     class Meta:
#         model = Recipe
#         fields = (
#             'ingredients',
#             'tags',
#             'image',
#             'name',
#             'text',
#             'cooking_time'
#         )

#     def create_ingredients(self, ingredients, recipe):
#         IngredientRecipe.objects.bulk_create([
#             IngredientRecipe(
#                 recipe=recipe,
#                 amount=ingredient.get('amount'),
#                 ingredient_id=ingredient.get('id')
#             ) for ingredient in ingredients
#         ])

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         recipe = Recipe.objects.create(**validated_data)
#         recipe.save()
#         recipe.tags.set(tags)
#         self.create_ingredients(ingredients, recipe)
#         return recipe

#     def update(self, recipe, validated_data):
#         if 'ingredients' in validated_data:
#             ingredients = validated_data.pop('ingredients')
#             recipe.ingredients.clear()
#             self.create_ingredients(ingredients, recipe)
#         if 'tags' in validated_data:
#             tags_data = validated_data.pop('tags')
#             recipe.tags.set(tags_data)
#         return super().update(
#             instance=recipe,
#             validated_data=validated_data
#         )

#     def validate_ingredients(self, value):
#         list = []
#         for ing in value:
#             ing_id = dict(ing).get('id')
#             if ing_id in list:
#                 raise serializers.ValidationError(
#                     'Ингредиенты не должны повторяться!'
#                 )
#             list.append(ing_id)
#         if not list:
#             raise serializers.ValidationError(
#                 'В рецепте должны быть ингредиенты'
#             )
#         return value

#     def validate_cooking_time(self, value):
#         if value == 0:
#             raise serializers.ValidationError(
#                 'Время приготовления не может быть 0 и отрицательным!'
#             )
#         return value

#     def validate_tags(self, value):
#         list = []
#         for tag in value:
#             if tag in list:
#                 raise serializers.ValidationError(
#                     'Теги не должны повторяться!'
#                 )
#             list.append(tag)
#         return value

# class AddIngredientSerializer(serializers.ModelSerializer):
#     """Сериализатор для добавления ингредиентов."""

#     id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
#     amount = serializers.IntegerField()

#     class Meta:
#         model = IngredientRecipe
#         fields = 'id', 'amount',

# class RecipeWriteSerializer(serializers.ModelSerializer):
#     """Сериализатор для добавления и обновления рецепта."""

#     author = UsersSerializer(read_only=True)
#     image = Base64ImageField()
#     ingredients = AddIngredientSerializer(many=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True,
#     )

#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'name', 'author', 'text', 'image', 'ingredients', 'tags',
#             'cooking_time'
#         )

#     @staticmethod
#     def __check_len(name, lst):
#         value = {'tags': 'Теги', 'ingredients': 'Ингредиенты'}
#         if len(set(lst)) < len(lst):
#             raise serializers.ValidationError(
#                 {'name': f'{value[name]} должны быть уникальными.'}
#             )

#     def tags_validation(self, tags):
#         if not tags:
#             raise serializers.ValidationError(
#                 {'tags': 'Выберите хотя бы один тег.'}
#             )
#         self.__check_len('tags', tags)

#     def ingredient_validation(self, ingredients):
#         ingredients_id = [i['id'] for i in ingredients]
#         self.__check_len('ingredients', ingredients_id)
#         if any([int(i['amount']) <= 0 for i in ingredients]):
#             raise serializers.ValidationError(
#                 {'amount': 'Количество ингредиента должно быть больше 0.'}
#             )

#     @staticmethod
#     def cooking_time_validation(cooking_time):
#         if int(cooking_time) <= 0:
#             raise serializers.ValidationError(
#                 {'cooking_time': 'Время приготовления должно быть больше 0.'}
#             )

#     def validate(self, data):
#         self.tags_validation(data['tags'])
#         self.ingredient_validation(data['ingredients'])
#         self.cooking_time_validation(data['cooking_time'])
#         return data

#     @staticmethod
#     def create_ingredients(recipe, ingredients):
#         ingredients_list = [IngredientRecipe(
#             recipe=recipe,
#             ingredient=ing['id'],
#             amount=ing['amount']
#         ) for ing in ingredients]
#         IngredientRecipe.objects.bulk_create(ingredients_list)

#     def create(self, validated_data):
#         author = self.context.get('request').user
#         tags_data = validated_data.pop('tags')
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(author=author, **validated_data)
#         recipe.save()
#         recipe.tags.set(tags_data)
#         self.create_ingredients(recipe, ingredients_data)
#         return recipe

#     def update(self, recipe, validated_data):
#         recipe.tags.clear()
#         IngredientRecipe.objects.filter(recipe=recipe).delete()
#         recipe.tags.set(validated_data.pop('tags'))
#         self.create_ingredients(recipe, validated_data.pop('ingredients'))
#         return super().update(recipe, validated_data)

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return RecipeReadSerializer(instance, context=context).data


# class RecipeShortInfo(RecipeWriteSerializer):
#     """"Сериализатор рецептов  для отображения нужных полей"""
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'ingredients', 'cooking_time')


class AddToSerializer(serializers.Serializer):
    "Сериализатор для добавления в спискок покупок/избранное"
        
    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortInfo(
            instance.recipe,
            context={'request': request}
        ).data

#     def validate(self, data):
#         request = self.context.get('request')
#         user = request.user
#         recipe = data.get('recipe')
#         if ShoppingCart.objects.filter(recipe=recipe, user=user):
#             raise serializers.ValidationError(
#                 'Вы уже добавили этот рецепт в список покупок/избранное'
#             )


# class FollowListSerializer(serializers.ModelSerializer):
#     """Сериализатор для списка избранного"""
#     recipes = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count'
#         )

#     def get_recipes_count(self, obj):
#         return obj.recipes_author.count()

#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         recipes_limit = request.query_params.get('recipes_limit')
#         if not recipes_limit:
#             return RecipeShortInfo(
#                 Recipe.objects.filter(author=obj),
#                 many=True,
#                 context={'request': request}
#             ).data
#         return RecipeShortInfo(
#             Recipe.objects.filter(author=obj)[:int(recipes_limit)],
#             many=True,
#             context={'request': request}
#         ).data

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         user = request.user
#         if not request or user.is_anonymous:
#             return False
#         subcribe = user.follower.filter(author=obj)
#         return subcribe.exists()


# class FollowSerializer(serializers.ModelSerializer):
#     """Сериализатор для подписки"""
#     class Meta:
#         model = Follow
#         fields = ('author', 'user')

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         return FollowListSerializer(
#             instance.author,
#             context={'request': request}
#         ).data

#     def validate(self, data):
#         request = self.context.get('request')
#         user = request.user
#         author = data.get('author')
#         if Follow.objects.filter(user=user, author=author):
#             raise serializers.ValidationError('Вы уже подписаны')
#         if user == author:
#             raise serializers.ValidationError(
#                 'Вы не можете подписаться на себя'
#             )
#         return data




########################################################




class RecipeInfoSerializer(serializers.ModelSerializer):
    """Сериализатор с краткой информацией о рецепте."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор описывающий тег."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор описывающий ингредиент."""

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор описывающий количество ингредиента."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = 'id', 'name', 'measurement_unit', 'amount',


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = 'id', 'amount',


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""

    tags = TagSerializer(many=True)
    author = UsersSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    @staticmethod
    def get_ingredients(obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data
        # return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favourite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и обновления рецепта."""

    author = UsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text', 'image', 'ingredients', 'tags',
            'cooking_time'
        )

    @staticmethod
    def __check_len(name, lst):
        value = {'tags': 'Теги', 'ingredients': 'Ингредиенты'}
        if len(set(lst)) < len(lst):
            raise serializers.ValidationError(
                {'name': f'{value[name]} должны быть уникальными.'}
            )

    def tags_validation(self, tags):
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Выберите хотя бы один тег.'}
            )
        self.__check_len('tags', tags)

    def ingredient_validation(self, ingredients):
        ingredients_id = [i['id'] for i in ingredients]
        self.__check_len('ingredients', ingredients_id)
        if any([int(i['amount']) <= 0 for i in ingredients]):
            raise serializers.ValidationError(
                {'amount': 'Количество ингредиента должно быть больше 0.'}
            )

    @staticmethod
    def cooking_time_validation(cooking_time):
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {'cooking_time': 'Время приготовления должно быть больше 0.'}
            )

    def validate(self, data):
        self.tags_validation(data['tags'])
        self.ingredient_validation(data['ingredients'])
        self.cooking_time_validation(data['cooking_time'])
        return data

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredients_list = [IngredientRecipe(
            recipe=recipe,
            ingredient=ing['id'],
            amount=ing['amount']
        ) for ing in ingredients]
        IngredientRecipe.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        self.create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        recipe.tags.set(validated_data.pop('tags'))
        self.create_ingredients(recipe, validated_data.pop('ingredients'))
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data
