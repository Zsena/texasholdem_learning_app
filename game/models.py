from django.db import models

class Game(models.Model):
    player_cards = models.CharField(max_length=50)
    opponent_cards = models.CharField(max_length=50, blank=True, null=True)

    flop = models.CharField(max_length=50)
    turn = models.CharField(max_length=10)
    river = models.CharField(max_length=10)

    best_hand = models.CharField(max_length=50)
    hand_rank = models.IntegerField()

    outcome = models.CharField(max_length=50, blank=True, null=True)

    evaluation_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_cards} vs {self.opponent_cards} -> {self.outcome}"



