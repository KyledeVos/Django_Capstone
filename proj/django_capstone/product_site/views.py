from django.shortcuts import render, HttpResponse

def site_home(request):
    return render(request, 'site_home.html')
