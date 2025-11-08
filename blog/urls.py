"""Blog URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]