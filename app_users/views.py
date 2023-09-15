import logging
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import RegistrationForm, UpdateBalanceForm
from .models import CustomUser
from django.urls import reverse_lazy as _

logger = logging.getLogger(__name__)



class LoginUser(LoginView):
    template_name = 'app_users/login_users.html'
    success_url = 'profile'

    def get(self, request, *args, **kwargs):
        logger.debug("test message in login user")
        return super().get(request, *args, **kwargs)


class LogoutUser(LogoutView):
    template_name = 'app_users/logout_users.html'


class RegistrationView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'app_users/registration_view.html'


class DetailProfile(DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'app_users/profile_detail.html'


class OrderHistory(DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'app_users/order_history.html'


class UpdateProfile(UpdateView):
    model = CustomUser
    form_class = UpdateBalanceForm
    template_name = 'app_users/update_profile.html'

    def post(self, request, *args, **kwargs):
        form = UpdateBalanceForm(request.POST, instance=self.get_object())
        if form.is_valid():
            need_user = form.save(commit=False)
            need_user.balance_user += form.cleaned_data['int_for_plus_balance']
            need_user.save()
            logger.debug("test message in replenishment of the balance")
        return redirect('profile', pk=request.user.pk)
