from datetime import datetime, timedelta

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView
from pytz import timezone

from TipsterLeague.forms import MatchPredictionForm
from TipsterLeague.models import Match, MatchPrediction


class MatchPredictionView(FormView):
    template_name = 'match-prediction.html'
    form_class = MatchPredictionForm

    def get(self, request, *args, **kwargs):
        self.request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        if not self.request.user.is_authenticated:
            messages.warning(self.request,
                             "You must <a href='/login' class='alert-link'>log in</a> to be able to predict matches.")
            return redirect(self.request.session['previous_page'])

        if MatchPrediction.objects.filter(user=self.request.user, match=self.getMatch()).exists():
            messages.warning(self.request, "You already predicted this match.")
            return redirect(self.request.session['previous_page'])

        if self.getMatch().date.astimezone() < (datetime.now() + timedelta(minutes=15)).astimezone():
            messages.warning(self.request, "You can predict the match score up to 15 minutes before it starts.")
            return redirect(self.request.session['previous_page'])

        return super().get(request, args, kwargs)

    def form_valid(self, form):
        self.success_url = self.request.session['previous_page']
        home_goals = form.cleaned_data['home_goals']
        away_goals = form.cleaned_data['away_goals']
        user = self.request.user
        match = self.getMatch()
        MatchPrediction.objects.create(user=user, match=match, home_goals=home_goals, away_goals=away_goals)
        messages.success(self.request, "Match prediction successfully saved.")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = self.getMatch()

        return context

    def getMatch(self):
        try:
            match = Match.objects.get(id=self.kwargs['match_id'])
        except ObjectDoesNotExist:
            raise Http404("Match with given id doesn't exist")

        return match
