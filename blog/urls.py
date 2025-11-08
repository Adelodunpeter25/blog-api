"""Blog URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet, UserViewSet
from blog.views.auth import google_auth, logout_view

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/google/', google_auth, name='google_auth'),
    path('auth/logout/', logout_view, name='logout'),
]