"""Blog URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]