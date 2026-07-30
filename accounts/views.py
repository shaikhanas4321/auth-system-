from django.shortcuts import render
from .models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status , permissions
from accounts.serializers import *
from accounts.utils import email_verification
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# Create your views here.

@api_view(["POST"])
def register(request):
    registration= RegisterSerializer(data=request.data)
    if registration.is_valid():
        user = registration.save()
        email_verification(user)
        return Response(registration.data, status=status.HTTP_201_CREATED)
    return Response(registration.errors, status=status.HTTP_400_BAD_REQUEST)


User=get_user_model()
class sendOTP(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self , request):
        serializer = sendOTPserializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
          user =  User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.email_verified:
            return Response({"message": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)

        email_verification(user)
        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

class VerifyOTP(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = verifyOTPserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        user.email_verified = True
        user.email_otp.delete()
        user.save(update_fields=["email_verified"])

        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        
class loginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self , request):
        serializer = loginserializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"] 
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        })
        
class profileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self , request):
        return Response({
            "message": "You are authenticated!",
            "user_id": request.user.id,
            "email": request.user.email,
        })       

class logoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self , request):
        serializer= logoutserializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token=serializer.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )

class ResetPasswordView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        serializer=ResetPasswordSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["NewPassword"])
        user.save()
        return Response({
            "message":"password reset successfull"
        },status=status.HTTP_200_OK)



class ForgetPasswordView(APIView):
     permission_classes = [permissions.AllowAny]
     def post(self , request):
            serializer = sendOTPserializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            try:
              user =  User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND) 
            email_verification(user)
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter