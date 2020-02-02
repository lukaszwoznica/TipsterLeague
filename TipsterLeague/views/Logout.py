from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/')
