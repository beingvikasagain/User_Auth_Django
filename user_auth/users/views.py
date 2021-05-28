from django.shortcuts import render
from rest_framework import status, generic
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


#user registration
