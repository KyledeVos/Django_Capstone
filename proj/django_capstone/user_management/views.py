"""Views Module for Django App 'user_management' controlling user creation, login
    and logout functionality

Methods:
--------
user_login(request, source, error = 'none'):
    Render Html page to retrieve username and password for attempted login

authenticate_user(request, source):
    Retrieve username and password from html form attempting to log user in

user_logout(request):
    log current user out and return user to app homepage

create_user(request, source, error):
    render html page to retrieve username and password required for user creation

add_user(request, source):
    Retrieve username and password from html form, validate inputs and attempt to create
    new user. Successful creation will also log new user in as the current user
"""
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError


def user_login(request, source, error = 'none'):
    """Render Html page to retrieve username and password for attempted login.
    
    Parameters:
    -----------
    request: HTTPRequest object
        required for rendering of html page
    source: str
        description of page source where call for user login was made allowing return
        of user to the same page after successful login
    error: string
        description of error to display to user for failed login
    """
    return render(request, 'user_login.html', {'error': error, 'source':source})


def authenticate_user(request, source):
    """Retrieve username and password from html form attempting to log user in.
    
    Parameters:
    -----------
    request: HTTPRequest object
        used to retrieve user inputs from html form and attempt to log user in
    source: str
        description of page source where call for user login was made allowing return
        of user to the same page after successful login
    """
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
    """log current user out and return user to app homepage"""
    # perform logout
    logout(request)
    # return user to app homepage after logout
    return HttpResponseRedirect(reverse('product_site:site_home'))


def create_user(request, source, error):
    """render html page to retrieve username and password required for user creation.
    
    Parameters:
    ----------
    request: HTTPRequest object
        used to retrieve user inputs from html form
    source: str
        description of page source where call for user creation was made allowing return
        of user to the same page after successful new user creation
    error: string
        description of error to display to user for failed sign up
    """
    context = {
        'source': source,
        'error': error
    }
    return render(request, 'create_user.html', context)

def add_user(request, source):
    """Retrieve username and password from html form, validate inputs and attempt to create
    new user. Successful creation will also log new user in as the current user.

    Parameters:
    ----------
    request: HTTPRequest object
        used to retrieve user inputs from html form
    source: str
        description of page source where call for user creation was made allowing return
        of user to the same page after successful new user creation
    """
    # attempt to retrieve username and password
    username = request.POST['username']
    password = request.POST['password']
    # retrieve user full name and email address
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email_address']

    # check fields above do not contain empty characters
    if (username.isspace() or password.isspace() 
        or first_name.isspace() or last_name.isspace() or email.isspace()):
        error_message = "Sign Up Failed - An option did not contain any characters"
        return HttpResponseRedirect(reverse('user_management:create_user', args=(source, error_message,)))

    # attempt to create new user with a unique username and associated fields
    try:
        user = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name = first_name,
                        last_name = last_name,
                        email = email)
    except IntegrityError:
        # error message for display to user for non-unique username
        error_message = "Username is not unique"
        return HttpResponseRedirect(reverse('user_management:create_user', args=(source, error_message,)))
    
    # at this point the new user was successfully created. Log user in
    login(request, user)

    # return user to original page of call where 'sign_up' was selected
    return HttpResponseRedirect(reverse(f'product_site:{source}'))
