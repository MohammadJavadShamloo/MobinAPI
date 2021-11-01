from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('send-otp/', views.SendOtpView.as_view(), name='send_otp'),
    path('validate-otp/', views.ValidateOtpView.as_view(), name='validate_otp'),
    path('change-pass/', views.ChangePassView.as_view(), name='change_password'),
    path('list-tokens/', views.ListTokensView.as_view(), name='list_tokens'),
    path('kill-tokens/', views.KillTokenView.as_view(), name='kill_tokens'),
]
