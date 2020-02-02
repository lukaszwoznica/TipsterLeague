from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.decorators import login_required

from TipsterLeague.forms import PasswordChangeForm
from TipsterLeague.models import MatchPrediction


@method_decorator(login_required, name='dispatch')
class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tips'] = MatchPrediction.objects.filter(user=self.request.user).count()
        return context


class TipsList(ListView):
    template_name = 'tips-list.html'
    context_object_name = 'tips'
    paginate_by = 20

    def get_queryset(self):
        qs = MatchPrediction.objects.filter(user=self.request.user).order_by('-id')
        return qs


@method_decorator(login_required, name='dispatch')
class PasswordChange(FormView):
    template_name = 'change-password.html'
    form_class = PasswordChangeForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChange, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['new_password'])
        self.request.user.save()
        messages.success(self.request, 'Your password has been successfully changed. Log in with new password.')
        return super().form_valid(form)
