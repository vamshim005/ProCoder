from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    AccountEmailActivateView,
    LoginView,
    RegisterView,
    ProfileView,
    LeaderBoardView,
    verify_info
)

app_name = 'account'

urlpatterns = [
    path('email/confirm/<str:key>/', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-info/', verify_info, name='verify_info'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('leaderboard/', LeaderBoardView.as_view(), name='leaderboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Password change URLs
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password/change/done/'
    ), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
] 