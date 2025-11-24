from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "player_cards", "opponent_cards", "outcome")
    ordering = ("-created_at",)
    search_fields = ("player_cards", "opponent_cards")
