# Django core
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
# DRF core
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
# Collections
from collections import defaultdict
# Local imports
from .models import SteamUser, SteamGame, OwnedGame
from .serializers import SteamUserSerializer, SteamGameSerializer, OwnedGameSerializer

class SteamUserViewSet(viewsets.ModelViewSet):
    queryset = SteamUser.objects.all()
    serializer_class = SteamUserSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        user = get_object_or_404(SteamUser, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(SteamUser, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SteamGameViewSet(viewsets.ModelViewSet):
    queryset = SteamGame.objects.all()
    serializer_class = SteamGameSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        game = get_object_or_404(SteamGame, pk=pk)
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        game = get_object_or_404(SteamGame, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OwnedGameViewSet(viewsets.ModelViewSet):
    queryset = OwnedGame.objects.all()
    serializer_class = OwnedGameSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def common_games_analysis(request):
    """Returns all games shared between any users, sorted by popularity"""
    # Single query to get all user-game relationships
    user_games = (
        SteamUser.objects
        .prefetch_related('owned_games__game')
        .annotate(game_count=Count('owned_games'))
        .filter(game_count__gt=0)
    )
    
    # Build game ownership index {game_id: [user_ids]}
    game_index = defaultdict(list)
    for user in user_games:
        for owned in user.owned_games.all():
            game_index[owned.game.app_id].append({
                'user_id': user.steam_id,
                'username': user.username
            })

    # Get games shared by at least 2 users
    shared_games = [
        {
            'game': {
                'app_id': game.app_id,
                'name': game.name,
                'app_img_url': game.app_img_url
            },
            'shared_by': game_index[game.app_id],
            'shared_count': len(game_index[game.app_id])
        }
        for game in SteamGame.objects.filter(app_id__in=[
            gid for gid, users in game_index.items() if len(users) > 1
        ])
    ]
    
    return Response({
        'results': sorted(shared_games, key=lambda x: -x['shared_count'])
    })