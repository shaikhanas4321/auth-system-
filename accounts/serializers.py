from rest_framework import serializers
from django.contrib.auth import authenticate 
from .models import User,emailOTP

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]
        extra_kwargs = {
          "password": {
        "write_only": True
    }
}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
  
class sendOTPserializer(serializers.Serializer):
    email = serializers.EmailField()

class verifyOTPserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    def validate(self , data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist ")
        try:
            otp_obj=user.email_otp
        except emailOTP.DoesNotExist:
            raise serializers.ValidationError("No OTP found. Please request a new one.")
        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired. Please request a new one.")

        if otp_obj.otp != data["otp"]:
            raise serializers.ValidationError("Invalid OTP.")

        data ["user"]=user
        return data
 
    
class loginserializers(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True, style={"input_type":"password"})
    def validate(self , data):
        email=data.get("email")
        password=data.get("password")
        try:
            user_obj =  User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("email or password invalid")
        if not user.is_active:
            raise serializers.ValidationError("user is not active")
        if not user.email_verified:
            raise serializers.ValidationError("email not verified")
        data["user"] = user
        return data
        

    
    

