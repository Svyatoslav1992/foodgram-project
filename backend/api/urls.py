from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from api.views import (DownloadCart, IngredientViewSet, RecipeViewSet,
#                        TagViewSet)

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet)


from users.views import UsersViewSet

User = get_user_model()

router = DefaultRouter()

app_name = 'api'

router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    # path('recipes/download_shopping_cart/', DownloadCart.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'))
]
