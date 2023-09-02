from django.shortcuts import render, HttpResponse


def home_page(request):
    return render(request, 'home_page.html')
    

def create_product(request):
    return render(request, 'create_product.html')



def add_product(request):
    pass
