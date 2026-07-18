from django.shortcuts import render
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer
# Create your views here.

@api_view(["POST"])
def register(request):
    registration= RegisterSerializer(data=request.data)
    if registration.is_valid():
        registration.save()
        return Response(registration.data, status=status.HTTP_201_CREATED)
    return Response(registration.errors, status=status.HTTP_400_BAD_REQUEST)
