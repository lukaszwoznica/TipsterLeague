from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import TemplateView
from TipsterLeague.models import Competition, Match


class Index(TemplateView):
    template_name = 'index.html'
    competition_id = 2021

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'comp_id' in kwargs:
            self.competition_id = kwargs['comp_id']

        try:
            competition = Competition.objects.get(id=self.competition_id)
            context['comp_name'] = competition.name
            context['comp_id'] = self.competition_id
            context['last_gameweek'] = Match.objects.filter(competition=competition,
                                                            gameweek=competition.current_gameweek - 1)
        except ObjectDoesNotExist:
            pass

        return context


class CompetitionView(TemplateView):
    template_name = 'competition.html'
    competition = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'id' in kwargs:
            self.competition = self.getCompetition()
            if 'gameweek' in kwargs:
                gameweek = kwargs['gameweek']
            else:
                gameweek = self.competition.current_gameweek
            gameweek_matches = self.getMatchesFromGameweek(gameweek)
            context['gameweek_number'] = gameweek
            context['gameweek_matches'] = gameweek_matches
            context['competition'] = self.competition
        else:
            raise Http404("Competition with given id doesn't exist")

        return context

    def getCompetition(self):
        try:
            competition = Competition.objects.get(id=self.kwargs['id'])
        except ObjectDoesNotExist:
            raise Http404("Competition with given id doesn't exist")

        return competition

    def getMatchesFromGameweek(self, gameweek):
        try:
            gameweek_matches = Match.objects.filter(competition=self.competition, gameweek=gameweek).order_by('date')
        except ObjectDoesNotExist:
            raise Http404("Invalid gameweek number")

        return gameweek_matches


class LeagueTable(TemplateView):
    template_name = 'league-table.html'
    page = 1

    def dispatch(self, request, *args, **kwargs):
        if 'page' in kwargs:
            self.page = kwargs['page']
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league_table = User.objects.raw(
            "SELECT u.id, username, COUNT(p.user_id) as tips, SUM(p.correct_match_result=1) as c_results, "
            "SUM(p.correct_score=1) as c_scores, SUM(p.correct_match_result=1)*2 + SUM(p.correct_score=1)*3 as pts "
            "FROM auth_user as u "
            "INNER JOIN TipsterLeague_matchprediction as p "
            "ON (u.id=p.user_id) "
            "WHERE p.status = 'S'"
            "GROUP BY u.id "
            "ORDER BY pts DESC"
        )

        paginator = Paginator(league_table, 20)
        context['table_page'] = paginator.get_page(self.page)
        context['page'] = self.page
        return context
