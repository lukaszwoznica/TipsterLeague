from django.contrib import admin

from TipsterLeague.models import *


def makeMatchPredictionSettled(modeladmin, request, queryset):
    queryset.update(status='S')


makeMatchPredictionSettled.short_description = "Mark selected match predictions as Settled"


def makeMatchScheduled(modeladmin, request, queryset):
    queryset.update(status='SC')


makeMatchScheduled.short_description = "Mark selected matches as Scheduled"


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_update', 'current_gameweek', 'id')
    readonly_fields = ('id',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_teams', 'home_goals', 'away_goals', 'date', 'status', 'competition', 'gameweek', 'id')
    list_filter = ('status', 'competition', 'gameweek')
    readonly_fields = ('id',)
    search_fields = ['home_team', 'away_team']
    actions = [makeMatchScheduled]


@admin.register(MatchPrediction)
class MatchPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'match', 'home_goals', 'away_goals', 'status')
    list_filter = ('status', 'correct_match_result', 'correct_score')
    readonly_fields = ('id',)
    actions = [makeMatchPredictionSettled]



