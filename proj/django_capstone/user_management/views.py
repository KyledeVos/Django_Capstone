from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def create_user(request):
    return render(request, 'create_user.html')


def user_login(request, source, error = 'none'):
    return render(request, 'user_login.html', {'error': error, 'source':source})


def authenticate_user(request, source):
    # retrieve username and password from login attempt
    username= request.POST['username']
    password = request.POST['password']

    # check username and password do not contain empty characters
    if username.isspace() or password.isspace():
        error_message = "Login Failed - Username and\\or password did not contain any characters"
        return HttpResponseRedirect(reverse('user_management:user_login', args=(error_message,)))

    # attempt to authenticate user
    user = authenticate(username=username, password = password)

    if user is None:
        # unsuccessful authentication
        error_message = "Invalid username and\\or password - Please Try again"
        # allow user to try login again
        return HttpResponseRedirect(reverse('user_management:user_login', args=(error_message,)))
    else:
        # log current user in to session
        login(request, user)
        # successful login - use source to return user to original page of login call
        return HttpResponseRedirect(reverse(f'product_site:{source}'))
    

def user_logout(request):
    # perform logout
    logout(request)
    # return user to app homepage after logout
    return HttpResponseRedirect(reverse('product_site:site_home')
    )

