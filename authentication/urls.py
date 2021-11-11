from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title='MobinAPI',
        default_version='v1',
        description='A Sample API for Authentication',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='mshomloo@email.kntu.ac.ir'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('send-otp/', views.SendOtpView.as_view(), name='send_otp'),
    path('validate-otp/', views.ValidateOtpView.as_view(), name='validate_otp'),
    path('change-pass/', views.ChangePassView.as_view(), name='change_password'),
    path('forgot-pass/', views.ForgotPassView.as_view(), name='forgot_password'),
    path('list-tokens/', views.ListTokensView.as_view(), name='list_tokens'),
    path('kill-tokens/', views.KillTokenView.as_view(), name='kill_tokens'),
    path('get-time/', views.GetWorldTimeView.as_view(), name='get_time'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/arch-pic/', views.ShowArchPicView.as_view(), name='show-arch-pic'),
    path('admin/delete-arch-pic/<int:pk>', views.DeleteArchPicView.as_view(), name='delete-arch-pic'),
    path('admin/update-arch-pic/<int:pk>', views.UpdateArchPicView.as_view(), name='update-arch-pic'),
    path('admin/create-arch-pic/', views.CreateArchPicView.as_view(), name='create-arch-pic'),
]

