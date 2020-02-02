import re

from django import forms
from django.contrib.auth.models import User

LETTERS_PATTERN = re.compile(".*[a-z]+.*", re.IGNORECASE)
NUMBERS_PATTERN = re.compile(".*\\d+.*", re.IGNORECASE)


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=50, required=True)
    password = forms.CharField(label='Password', max_length=255, required=True, widget=forms.PasswordInput())


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=255, required=True)
    password = forms.CharField(label='Password', max_length=255, required=True, widget=forms.PasswordInput())

    username.widget.attrs.update({'class': 'textInput form-control'})
    email.widget.attrs.update({'class': 'emailinput form-control'})
    password.widget.attrs.update({'class': 'textInput form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters.')
        if not LETTERS_PATTERN.match(password):
            raise forms.ValidationError('Password must contain at least one letter.')
        if not NUMBERS_PATTERN.match(password):
            raise forms.ValidationError('Password must contain at least one number.')
        return password


class AddCompetitionForm(forms.Form):
    COMPETITION_CHOICES = (
        ("PL", "Premier League"),
        ("PD", "Primera Division (La Liga)"),
        ("FL1", "Ligue 1"),
        ("BL1", "Bundesliga"),
        ("SA", "Serie A"),
        ("DED", "Eredivisie"),
        ("PPL ", "Primeira Liga (Liga NOS)")
    )
    competition_code = forms.ChoiceField(choices=COMPETITION_CHOICES, required=True, label="Select competition")


class MatchPredictionForm(forms.Form):
    home_goals = forms.IntegerField(min_value=0, max_value=99, required=True)
    away_goals = forms.IntegerField(min_value=0, max_value=99, required=True)
    home_goals.widget.attrs.update({'class': 'form-control score_input'})
    away_goals.widget.attrs.update({'class': 'form-control score_input'})


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label='Current password', max_length=255, required=True,
                                       widget=forms.PasswordInput())
    new_password = forms.CharField(label='New password', max_length=255, required=True,
                                   widget=forms.PasswordInput())
    new_password_repeat = forms.CharField(label='Repeat new password', max_length=255, required=True,
                                          widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Invalid password.')
        return password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        if len(new_password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters.')
        if not LETTERS_PATTERN.match(new_password):
            raise forms.ValidationError('Password must contain at least one letter.')
        if not NUMBERS_PATTERN.match(new_password):
            raise forms.ValidationError('Password must contain at least one number.')
        return new_password

    def clean_new_password_repeat(self):
        new_password_repeat = self.cleaned_data['new_password_repeat']
        new_password = self.data.get('new_password')
        if new_password_repeat != new_password:
            raise forms.ValidationError('The entered passwords do not match.')
        return new_password_repeat
