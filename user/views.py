from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def index(request):
    return Response({"Rest" :"FrameWork is working"})
   