from django.shortcuts import render, HttpResponse

def logincheck(request):
    """Determine if a current user is authenticated

    Parameter:
    -----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render

    Return:
    -------
    True if user is authenticated, False if not
    """
    if request.user.is_authenticated:
        return True
    else: 
        return False

def site_home(request):

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
