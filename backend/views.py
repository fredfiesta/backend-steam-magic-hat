from django.shortcuts import render
from .models import SteamUser, SteamGame, OwnedGame
from .serializers import SteamUserSerializer, SteamGameSerializer, OwnedGameSerializer
from rest_framework import viewsets, permissions
# Create your views here.

class SteamUserViewSet(viewsets.ModelViewSet):
    queryset = SteamUser.objects.all()
    serializer_class = SteamUserSerializer
    permission_classes = [permissions.AllowAny]

class SteamGameViewSet(viewsets.ModelViewSet):
    queryset = SteamGame.objects.all()
    serializer_class = SteamGameSerializer
    permission_classes = [permissions.AllowAny]

class OwnedGameViewSet(viewsets.ModelViewSet):
    queryset = OwnedGame.objects.all()
    serializer_class = OwnedGameSerializer
    permission_classes = [permissions.AllowAny]
