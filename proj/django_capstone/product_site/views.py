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
    context = {
        'logged_in': logincheck(request),
        'username': request.user.username,
        'source' : 'site_home'
    }
    return render(request, 'site_home.html', context)
