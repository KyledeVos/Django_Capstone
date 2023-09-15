from django.shortcuts import render, HttpResponse

def site_home(request):
    return HttpResponse("Home Site")
