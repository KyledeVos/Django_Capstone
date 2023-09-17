from django.shortcuts import render, HttpResponse

# Create your views here.

def user_login(request):
    return render(request, 'user_login.html')
