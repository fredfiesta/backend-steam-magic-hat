from django.db import models

# Create your models here.
class SteamUser(models.Model):
    steam_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=100)
    profile_img_url = models.URLField()

    def __str__(self):
        return f"{self.username} (ID: {self.steam_id})"

class SteamGame(models.Model):
    app_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    app_img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (ID: {self.app_id})"

class OwnedGame(models.Model):
    user = models.ForeignKey(SteamUser, on_delete=models.CASCADE, related_name='owned_games')
    game = models.ForeignKey(SteamGame, on_delete=models.CASCADE, related_name='owners')

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} owns {self.game.name}"