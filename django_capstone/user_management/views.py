"""Views Module for Django App 'user_management' controlling user creation, login
    and logout functionality.

Methods:
--------
:meth:`user_login(request, source, error = 'none')`
    Render Html page to retrieve username and password for attempted login

:meth:`authenticate_user(request, source)`
    Retrieve username and password from html form attempting to log user in

:meth:`user_logout(request)`
    log current user out and return user to app homepage

:meth:`create_user(request, source, error)`
    render html page to retrieve username and password required for user creation

:meth:`add_user(request, source)`
    Retrieve username and password from html form, validate inputs and attempt to create
    new user. Successful creation will also log new user in as the current user
"""
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

def user_login(request, source, error = 'none'):
    """Render Html page to retrieve username and password for attempted login.

    :param request: required for rendering of html page
    :type request: HTTPRequest object
    :param source: description of page source where call for user login was made allowing return
        of user to the same page after successful login
    :type source: str
    :param error: description of error to display to user for failed login
    :type error: str

    :return: user to login page
    :rtype: HTTPResponse
    """
    return render(request, 'user_login.html', {'error': error, 'source':source})


def authenticate_user(request, source):
    """Retrieve username and password from html form attempting to log user in.

    :param request: used to retrieve user inputs from html form and attempt to log user in
    :type request: HTTPRequest object
    :param source: description of page source where call for user login was made allowing return
        of user to the same page after successful login
    :type source: str

    :return: Successful Login - `source` page. Unsuccessful Login - login page
    :rtype: HTTPRespons
    """
    # retrieve username and password from login attempt
    username= request.POST['username']
    password = request.POST['password']

    # check username and password do not contain empty characters
    if username.isspace() or password.isspace():
        error_message = "Login Failed - Username and\\or password did not contain any characters"
        return HttpResponseRedirect(reverse('user_management:user_login', args=(source, error_message)))

    # attempt to authenticate user
    user = authenticate(username=username, password = password)

    if user is None:
        # unsuccessful authentication
        error_message = "Invalid username and\\or password - Please Try again"
        # allow user to try login again
        return HttpResponseRedirect(reverse('user_management:user_login', args=(source, error_message)))
    else:
        # log current user in to session
        login(request, user)
        # successful login - use source to return user to original page of login call
        return HttpResponseRedirect(reverse(f'product_site:{source}'))


def user_logout(request):
    """log current user out and return user to app homepage

    :param request: needed to perform user logout
    :type request: HTTPRequest object

    :return: user to product site home page
    :rtype: HTTPResponse
    """
    # perform logout
    logout(request)
    # return user to app homepage after logout
    return HttpResponseRedirect(reverse('product_site:site_home'))


def create_user(request, source, error):
    """render html page to retrieve username and password required for user creation.

    :param request: used to retrieve user inputs from html form
    :type request: HTTPRequest object
    :param source: description of page source where call for user creation was made allowing return
        of user to the same page after successful new user creation
    :type source: str
    :param error: description of error to display to user for failed sign up
    :type error: str

    :return: user to create user page
    :rtype: HTTPResponse
    """
    context = {
        'source': source,
        'error': error
    }
    return render(request, 'create_user.html', context)

def add_user(request, source):
    """Retrieve username and password from html form, validate inputs and attempt to create
    new user. Successful creation will also log new user in as the current user.

    :param request: used to retrieve user inputs from html form
    :type request: HTTPRequest object
    :param source: description of page source where call for user creation was made allowing return
        of user to the same page after successful new user creation
    :type source: str

    :raises IntegrityError: Non-unique username was supplied

    :return: Success - site home page. Error - Create new user page
    :rtype: HTTPResponse
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
        return HttpResponseRedirect(reverse('user_management:create_user',
                                            args=(source, error_message,)))

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
        return HttpResponseRedirect(reverse('user_management:create_user',
                                            args=(source, error_message,)))

    # at this point the new user was successfully created. Log user in
    login(request, user)

    # return user to original page of call where 'sign_up' was selected
    return HttpResponseRedirect(reverse(f'product_site:{source}'))
