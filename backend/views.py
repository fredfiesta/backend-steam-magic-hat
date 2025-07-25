# Django core
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction
# DRF core
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Collections
from collections import defaultdict
# Local imports
from .models import SteamUser, SteamGame, OwnedGame
from .serializers import SteamUserSerializer, SteamGameSerializer, OwnedGameSerializer
from django.http import HttpResponse

def landing_page(request):
    return HttpResponse("Welcome to Steam Magic Hat API")

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
        
        # Get all games owned ONLY by this user
        user_games = SteamGame.objects.filter(
            owners__user=user
        ).annotate(
            owner_count=Count('owners')
        ).filter(
            owner_count=1
        )
        
        # Delete user and their exclusive games
        with transaction.atomic():
            user.delete()
            user_games.delete()
            
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
    """Returns games shared between users, with optional min_shared_count filter"""
    # Get min_shared_count from query params (default=2)
    min_shared = int(request.query_params.get('min_shared_count', 2))
    
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

    # Filter games by shared count threshold
    filtered_game_ids = [
        gid for gid, users in game_index.items() 
        if len(users) >= min_shared  # Changed from >1 to >= min_shared
    ]
    
    # Get game details in bulk
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
        for game in SteamGame.objects.filter(app_id__in=filtered_game_ids)
    ]
    
    # Sort by shared_count descending
    sorted_games = sorted(shared_games, key=lambda x: -x['shared_count'])
    
    return Response({
        'results': sorted_games,
        'meta': {
            'min_shared_count': min_shared,
            'total_games': len(sorted_games)
        }
    })