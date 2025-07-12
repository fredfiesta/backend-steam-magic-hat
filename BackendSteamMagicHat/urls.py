from django.urls import path, include
from backend import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'steam_users', views.SteamUserViewSet, basename='steamuser')
router.register(r'steam_games', views.SteamGameViewSet, basename='steamgame')
router.register(r'owned_games', views.OwnedGameViewSet, basename='ownedgame')

urlpatterns = [
    path('', include(router.urls)),
    path('steam_games/shared', views.common_games_analysis, name='shared-games'),
]