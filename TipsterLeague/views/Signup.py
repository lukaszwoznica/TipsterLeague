from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView

from TipsterLeague.forms import SignupForm


class Signup(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = '/login'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.email = email
            user.save()
            messages.success(self.request, 'Your account has been created. You can login now.')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'User with given username already exists.')
            return self.form_invalid(form)