from django.shortcuts import render, HttpResponse

# Create your views here.
def home_page(index):
    return HttpResponse("Home Page")
