"""Blog URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet, UserViewSet, ReactionViewSet, ReadingListViewSet
from blog.views.auth import google_auth, login_view, register_view, logout_view

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)
router.register(r'reactions', ReactionViewSet, basename='reaction')
router.register(r'reading-list', ReadingListViewSet, basename='readinglist')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/google/', google_auth, name='google_auth'),
    path('auth/logout/', logout_view, name='logout'),
]