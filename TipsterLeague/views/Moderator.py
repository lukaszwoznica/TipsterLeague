from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView

from TipsterLeague.api import API
from TipsterLeague.forms import AddCompetitionForm
from TipsterLeague.models import Competition, Match, MatchPrediction

moderator_decorators = [permission_required('TipsterLeague.add_competition'),
                        permission_required('TipsterLeague.add_match')]


@method_decorator(moderator_decorators, name='dispatch')
class ModeratorDashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competitions'] = Competition.objects.all()
        return context


@method_decorator(moderator_decorators, name='dispatch')
class AddCompetition(FormView):
    template_name = 'add-competition.html'
    form_class = AddCompetitionForm
    success_url = '/moderator/dashboard'

    def form_valid(self, form):
        competition_code = form.cleaned_data['competition_code']
        url = "competitions/{0}/matches".format(competition_code)
        response = API.getRequest(url)
        competition_data = response['competition']
        matches_data = response['matches']

        if not Competition.objects.filter(id=competition_data['id']).exists():
            competition = Competition.objects.create(id=competition_data['id'],
                                                     name=competition_data['name'],
                                                     current_gameweek=matches_data[0]['season']['currentMatchday'],
                                                     last_update=competition_data['lastUpdated'])

            for match_data in matches_data:
                if not Match.objects.filter(id=match_data['id']).exists():
                    Match.objects.create(id=match_data['id'],
                                         home_team=match_data['homeTeam']['name'],
                                         away_team=match_data['awayTeam']['name'],
                                         home_goals=match_data['score']['fullTime']['homeTeam'],
                                         away_goals=match_data['score']['fullTime']['awayTeam'],
                                         status=match_data['status'][:2],
                                         gameweek=match_data['matchday'],
                                         date=match_data['utcDate'],
                                         competition=competition)

            messages.success(self.request, 'Competition has been successfully added.')
            return super().form_valid(form)

        messages.warning(self.request, 'An error occurred while adding a competition.')
        return self.form_invalid(form)


@method_decorator(moderator_decorators, name='dispatch')
class UpdateCompetition(View):

    def get(self, request, **kwargs):
        competition_id = kwargs['id']
        competition = Competition.objects.get(id=competition_id)
        url = "competitions/{0}".format(competition_id)
        competitions_response = API.getRequest(url)
        last_api_update = datetime.strptime(competitions_response['lastUpdated'], "%Y-%m-%dT%H:%M:%SZ")

        if competition.last_update.astimezone() < last_api_update.astimezone():
            outdated_gameweeks = []
            for i in range(competition.current_gameweek,
                           int(competitions_response['currentSeason']['currentMatchday']) + 1):
                outdated_gameweeks.append(i)

            for gameweek in outdated_gameweeks:
                url = "competitions/{0}/matches?matchday={1}".format(competition_id, gameweek)
                response = API.getRequest(url)
                for match_data in response['matches']:
                    match = Match.objects.get(id=match_data['id'])
                    match.home_goals = match_data['score']['fullTime']['homeTeam']
                    match.away_goals = match_data['score']['fullTime']['awayTeam']
                    match.date = match_data['utcDate']
                    match.status = match_data['status'][:2]
                    match.save()
                    self.settleMatchPredictions(match)

            competition.current_gameweek = competitions_response['currentSeason']['currentMatchday']
            competition.last_update = competitions_response['lastUpdated']
            competition.save()

            messages.success(self.request, "Competition {0} has been successfully updated.".format(competition.name))

        else:
            messages.info(self.request, "Competition {0} is up to date".format(competition.name))

        return redirect('/moderator/dashboard')

    def settleMatchPredictions(self, match):
        if match.status == Match.MatchStatus.FINISHED:
            predictions = MatchPrediction.objects.filter(match=match)
            for prediction in predictions:
                if (
                        (match.homeTeamIsWinner() and prediction.home_goals > prediction.away_goals) or
                        (match.awayTeamIsWinner() and prediction.home_goals < prediction.away_goals) or
                        (match.isDraw() and prediction.home_goals == prediction.away_goals)
                   ):
                    prediction.correct_match_result = True
                else:
                    prediction.correct_match_result = False

                if prediction.home_goals == match.home_goals and prediction.away_goals == match.away_goals:
                    prediction.correct_score = True
                else:
                    prediction.correct_score = False

                prediction.status = MatchPrediction.MatchPredictionStatus.SETTLED
                prediction.save()
