from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView
from ..forms import *


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Successfully logged in.')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Incorrect login or/and password.')
            return self.form_invalid(form)
