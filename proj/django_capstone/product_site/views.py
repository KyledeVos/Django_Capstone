"""Views Module for Django App 'product_site'. App serves as central site
for web application.

Methods:
--------
logincheck(request):
    Determine if a current user is authenticated

site_home(request):
    Render main site home page, checking if currently logged-in user is a staff
        member allowing access to admin control functionality
"""
from django.shortcuts import render, HttpResponse

def logincheck(request):
    """Determine if a current user is authenticated. """
    return True if request.user.is_authenticated else False


def site_home(request):
    """Render main site home page, checking if currently logged-in user is a staff
        member allowing access to admin control functionality.
         
    Parameter:
    ----------
    request: HTTPRequest object
        required for user authentication, status check and html page render
    """
    # Determine if the user has been logged in
    logged_in = logincheck(request)
    # if the user has been checked in, check if they are staff; giving access to admin control
    # of the site
    staff = False
    if logged_in:
        staff = True if request.user.is_staff else False
        
    context = {
        'logged_in': logged_in,
        'username': request.user.username,
        'source' : 'site_home',
        'staff' : staff
    }
    return render(request, 'site_home.html', context)
