from rest_framework import serializers
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
 
    

    
    

