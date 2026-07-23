from django.urls import path
from accounts import views
from .views import sendOTP , VerifyOTP

urlpatterns=[
    path("register/",views.register,name="register"),
    path("verify-otp/",VerifyOTP.as_view(), name="verifyOTP"),
    path("send-otp/",sendOTP.as_view(),name="sendOTP")
]