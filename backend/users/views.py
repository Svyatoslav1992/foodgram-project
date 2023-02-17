from api.pagination import CustomPagination
from api.serializers import FollowListSerializer, FollowSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Follow
from users.serializers import UsersSerializer

User = get_user_model()


class UsersViewSet(UserViewSet):
    """Вьюсет кастомной модели User."""

    pagination_class = CustomPagination
    serializer_class = UsersSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = FollowListSerializer(
                pages,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response(
            'Вы ни на кого не подписаны',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            context = {'request': request}
            data = {
                'user': user.id,
                'author': author.id
            }
            serializer = FollowSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        subscribe = get_object_or_404(
            Follow,
            user=user,
            author=author
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
