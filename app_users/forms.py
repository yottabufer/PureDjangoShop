from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name']


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    balance_user = forms.IntegerField(help_text='User balance')
    total_expenses = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'balance_user',
                  'total_expenses', 'status', 'password1', 'password2')


class UpdateBalanceForm(forms.ModelForm):
    int_for_plus_balance = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('balance_user',)
