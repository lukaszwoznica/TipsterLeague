from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    current_gameweek = models.IntegerField()
    last_update = models.DateTimeField()
    emblem = models.CharField(max_length=255, null=True, blank=True)
    theme_color_hex = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return "{0}. {1}".format(str(self.id), self.name)


class Match(models.Model):
    class MatchStatus(models.TextChoices):
        SCHEDULED = 'SC', _('Scheduled')
        FINISHED = 'FI', _('Finished')

    id = models.IntegerField(primary_key=True)
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    home_goals = models.IntegerField(null=True)
    away_goals = models.IntegerField(null=True)
    status = models.CharField(max_length=2, choices=MatchStatus.choices, default=MatchStatus.SCHEDULED)
    gameweek = models.IntegerField()
    date = models.DateTimeField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}. {1}-{2}".format(str(self.id), self.home_team, self.away_team)

    def match_teams(self):
        return "{0} - {1}".format(self.home_team, self.away_team)

    def homeTeamIsWinner(self):
        return self.home_goals > self.away_goals

    def awayTeamIsWinner(self):
        return self.home_goals < self.away_goals

    def isDraw(self):
        return self.home_goals == self.away_goals


class MatchPrediction(models.Model):
    class MatchPredictionStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        SETTLED = 'S', _('Settled')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    status = models.CharField(max_length=1, choices=MatchPredictionStatus.choices, default=MatchPredictionStatus.PENDING)
    correct_match_result = models.BooleanField(null=True)
    correct_score = models.BooleanField(null=True)
