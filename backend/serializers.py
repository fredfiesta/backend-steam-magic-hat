from rest_framework import serializers
from .models import SteamGame, SteamUser, OwnedGame
import os
from .utils.steam_api import fetch_steam_user_profile

class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = ['steam_id', 'username', 'profile_img_url']

    def create(self, validated_data):
        steam_id = validated_data['steam_id']
        api_key = os.getenv('STEAM_API_KEY')
        profile = fetch_steam_user_profile(steam_id, api_key)
        
        # Create or update user
        user, created = SteamUser.objects.update_or_create(
            steam_id=steam_id,
            defaults={
                'username': profile.get('personaname'),
                'profile_img_url': profile.get('avatarfull')
            }
        )
        return user

class SteamGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamGame
        fields = ['app_id', 'name', 'app_img_url']

class OwnedGameSerializer(serializers.ModelSerializer):
    steam_id = serializers.SlugRelatedField(
        slug_field='steam_id',
        queryset=SteamUser.objects.all(),
        source='user'
    )
    app_id = serializers.SlugRelatedField(
        slug_field='app_id',
        queryset=SteamGame.objects.all(),
        source='game'
    )

    class Meta:
        model = OwnedGame
        fields = ['steam_id', 'app_id']