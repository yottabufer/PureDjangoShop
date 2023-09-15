from django.urls import path
from .views import RegistrationView, DetailProfile, LoginUser, LogoutUser, UpdateProfile, OrderHistory

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('<int:pk>/', DetailProfile.as_view(), name='profile'),
    path('update/<int:pk>/', UpdateProfile.as_view(), name='update_profile'),
    path('order_history/<int:pk>/', OrderHistory.as_view(), name='order_history'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

]
