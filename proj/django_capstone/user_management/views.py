from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def user_login(request, error = 'none'):
    return render(request, 'user_login.html', {'error': error})


def create_user(request):
    return render(request, 'create_user.html')

def authenticate_user(request):


    # retrieve username and password from login attempt
    username= request.POST['username']
    password = request.POST['password']

    # check username and password do not contain empty characters
    if username.isspace() or password.isspace():
        error_message = "Login Failed - Username and\\or password did not contain any characters"

        return HttpResponseRedirect(reverse('user_management:user_login', args=(error_message,)))


    return HttpResponse(f"Name: {username}, Password: {password}")
