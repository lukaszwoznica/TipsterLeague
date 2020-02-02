from django import template
from django.contrib.auth.models import Group

from TipsterLeague.models import MatchPrediction

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='is_predicted')
def is_predicted(match, user):
    return MatchPrediction.objects.filter(user=user, match=match).exists()
