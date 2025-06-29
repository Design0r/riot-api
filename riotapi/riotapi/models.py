from __future__ import annotations

from django.db import models


class Account(models.Model):
    puuid = models.TextField(max_length=78, primary_key=True, null=False)
    game_name = models.TextField(max_length=100, null=False)
    tag_line = models.TextField(max_length=100, null=False)

    mach_history: models.Manager["MatchHistory"]

    def __str__(self) -> str:
        return f"{self.game_name}#{self.tag_line}"


class Match(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    data = models.JSONField(default=dict)  # type: ignore

    mach_history: models.Manager["MatchHistory"]

    def __str__(self) -> str:
        return f"{self.id}"


class MatchHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    match_idx = models.IntegerField(null=False)
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="match_history", null=False
    )
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="match_history", null=False
    )

    def __str__(self) -> str:
        return f"[{self.id}] {self.user} - {self.match_idx}"
