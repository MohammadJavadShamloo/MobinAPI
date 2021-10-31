from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
]
