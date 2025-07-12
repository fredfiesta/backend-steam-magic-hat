from rest_framework import serializers
from .models import SteamGame, SteamUser, OwnedGame
import os
from .utils.steam_api import fetch_steam_user_profile, fetch_steam_owned_games

class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = ['steam_id', 'username', 'profile_img_url']
        extra_kwargs = {
            'username': {'read_only': True},
            'profile_img_url': {'read_only': True}
        }

    def validate_steam_id(self, value):
        """Validate steam_id exists in Steam API before creating"""
        api_key = os.getenv('STEAM_API_KEY')
        try:
            profile = fetch_steam_user_profile(value, api_key)
            if not profile:
                raise serializers.ValidationError("Steam ID not found in Steam API")
        except Exception as e:
            raise serializers.ValidationError(f"Steam API error: {str(e)}")
        return value
    
    def create(self, validated_data):
        steam_id = validated_data['steam_id']
        api_key = os.getenv('STEAM_API_KEY')
        
        # 1. Fetch user profile
        profile = fetch_steam_user_profile(steam_id, api_key)
        user = SteamUser.objects.create(
            steam_id=steam_id,
            username=profile.get('personaname'),
            profile_img_url=profile.get('avatarfull')
        )
        
        # 2. Fetch and create games
        self._create_owned_games(user, api_key)
        
        return user

    def _create_owned_games(self, user, api_key):
        games = fetch_steam_owned_games(user.steam_id, api_key)
        
        for game in games:
            # Get or create game
            steam_game, _ = SteamGame.objects.get_or_create(
                app_id=game['appid'],
                defaults={
                    'name': game.get('name', f"Unknown Game {game['appid']}"),
                    'app_img_url': f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                }
            )
            
            # Create ownership record
            OwnedGame.objects.get_or_create(
                user=user,
                game=steam_game
            )

class SteamGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamGame
        fields = ['app_id', 'name', 'app_img_url']

class OwnedGameSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='steam_id',
        queryset=SteamUser.objects.all()
    )
    game = serializers.SlugRelatedField(
        slug_field='app_id',
        queryset=SteamGame.objects.all()
    )

    class Meta:
        model = OwnedGame
        fields = ['user', 'game']

    def validate(self, data):
        """Ensure both user and game exist"""
        if not data.get('user') or not data.get('game'):
            raise serializers.ValidationError("Both user and game must be specified")
        return data
    