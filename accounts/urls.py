from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns=[
    path("register/",views.register,name="register"),
    path("verify-otp/",VerifyOTP.as_view(), name="verifyOTP"),
    path("send-otp/",sendOTP.as_view(),name="sendOTP"),
    path("login/",loginView.as_view(),name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/",profileView.as_view(),name="profile"),
    path("logout/",logoutView.as_view(),name="logout"),
    path("forget-password/",ForgetPasswordView.as_view(),name="forget-password"),
    path("reset-password/",ResetPasswordView.as_view(),name="reset-password"),
    path("google-login/", GoogleLogin.as_view(), name="google-login") 
]