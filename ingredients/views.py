from django.shortcuts import render
from .models import Category
from django.http import JsonResponse
from graphene_django.views import GraphQLView

# Create your views here.
def Home(request):
    json = {
        'name': "hello"
    }
    return JsonResponse(json)

    