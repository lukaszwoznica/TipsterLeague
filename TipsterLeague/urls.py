"""TipsterLeague URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="index"),
    path('<int:comp_id>', Index.as_view(), name="index"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('signup/', Signup.as_view(), name="signup"),
    path('moderator/dashboard/', ModeratorDashboard.as_view(), name="moderator-dashboard"),
    path('moderator/add-competition/', AddCompetition.as_view(), name="add-competition"),
    path('moderator/update-competition/<int:id>/', UpdateCompetition.as_view(), name="update-competition"),
    path('competition/<int:id>/', CompetitionView.as_view(), name="competition"),
    path('competition/<int:id>/gameweek/<int:gameweek>/', CompetitionView.as_view(), name="competition_gameweek"),
    path('match-prediction/<int:match_id>/', MatchPredictionView.as_view(), name="match-prediction"),
    path('league-table/', LeagueTable.as_view(), name="league-table"),
    path('league-table/page/<int:page>/', LeagueTable.as_view(), name="league-table-page"),
    path('profile/', Profile.as_view(), name="profile"),
    path('profile/tips-list/', TipsList.as_view(), name="tips-list"),
    path('profile/tips-list/page/<int:page>/', TipsList.as_view(), name="tips-list-page"),
    path('profile/change-password/', PasswordChange.as_view(), name="password-change"),
]
