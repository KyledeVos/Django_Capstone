from django.shortcuts import render, HttpResponse


def home_page(request):
    return render(request, 'home_page.html')
    

def create_product(request):
    return HttpResponse("Create Product")



def add_product(request):
    pass
