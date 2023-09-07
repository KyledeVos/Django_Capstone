"""Views Module for Django App 'Polls'

Methods:
--------
home_page(request):
    render admin home app of app with SignUp, Login and Product Catalog

create_category(request, source):
    render html page allowing admin user to create a Category for Products to belong to.
    Pass in source argument determining page to return to after Category addition to database.

add_category(request, source):
    Retrieve Category Attributes from html form, create new Category instance and save to
    database. Use 'source' determining page to return to after new category is added.

create_label(request, source):
    render html page allowing admin user to create a new Label for Products.
    Pass in source argument determining page to return to after Label addition to database.

add_label(request, source):
    Retrieve Label Attributes from html form, create new Label instance and save to
    database. Use 'source' determining page to return to after new label is added.

create_product(request):
    Render html page allowing admin user to create a new product seeing number of allowed
    product options and passing allowed size options, current product Categories and Labels.

retrieve_size_pricing(request):
    Retrieve user-defined prices from html form input adding non-empty options
    to a list of tuples and return.

retrieve_product_options(request):
    Retrieve user-defined options for a product from html form, adding each to a list
    of tuples

add_product(request):
    Retrieve user-defined attributes from html from from 'create-product', create new
    product and save to database.
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse
from . import models
from datetime import date


def home_page(request):
    """render admin home app of app with SignUp, Login and Product Catalog"""
    return render(request, 'home_page.html')

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for New Product Creation

# max allowed desired options for a product
MAX_OPTIONS = 5

def create_category(request, source):
    """render html page allowing admin user to create a Category for Products to belong to.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new category is added
        to database.
    """
    return render(request, 'creation/create_category.html', {'source':source})


def add_category(request, source):
    """Retrieve Category Attributes from html form, create new Category instance and save to database
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new category is added
        to database
    """
    title = request.POST['title']
    category = models.Category.objects.create(title=title)
    category.save()
    # new category was created during product creation, return admin user to 'create_product' page
    if source == "new_product":
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
    # new category was created seperately, return admin user to main admin page
    else:
        return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))

def create_label(request, source):
    """render html page allowing admin user to create a new Label for Products.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new label is added
        to database
    """
    return render(request, 'creation/create_label.html', {'source': source})
        

def add_label(request, source):
    """Retrieve Label Attributes from html form, create new Label instance and save to
    database
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new label is added
        to database
    """
    title = request.POST['title']

    # if a discount was not set for this label, set to 0
    discount_percentage = request.POST.get('discount_percentage', 0)
    if discount_percentage=="":
        discount_percentage = 0

    creation_date = date.today()
    removal_days = request.POST.get('removal_days', '-1')
    if removal_days=="":
        removal_days = -1

    # colour retrieved from html 'color' input in hexadecimal format
    colour = request.POST.get('custom_colour', '')

    # create and save new label to database
    label = models.Label.objects.create(title=title,
                                        discount_percentage=discount_percentage,
                                        creation_date=creation_date,
                                        removal_days=removal_days,
                                        custom_colour=colour)
    label.save()
    # new label was created during product creation, return admin user to 'create_product' page
    if source == 'new_product':
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
    # new category was created seperately, return admin user to main admin page
    else:
        return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))

    
def create_product(request):
    """Render html page allowing admin user to create a new product seeing number of allowed
    product options and passing allowed size options, current product Categories and Labels

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    """
    # create list of option numbers (as strings) used by 'create_product.html' for
    # Product Options creation
    options_list = []
    for i in range(1, MAX_OPTIONS+1):
        options_list.append(str(i))

    # retrieve current product size options
    size_choices = []
    for tup in models.Product_Sizes.size_options:
        size_choices.append(tup[1])

    # retrieve all currently created product categories and labels
    categories = models.Category.objects.all()
    labels = models.Label.objects.all()

    context = {"size_choices": size_choices,
               "options_list": options_list,
               "categories": categories,
               "labels":labels,
               "source": 'new_product'}
    return render(request, 'creation/create_product.html', context)


# Helper Method
def retrieve_size_pricing(request):
    """Retrieve user-defined prices from html form input (using request) adding non-empty options
        to a list of tuples and return

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed to retrieve product sizes and products during
        new product creation

    Return:
    -------
    list of tuples each containing a product size and populated price value
    """
    size_info = []
    for tup in models.Product_Sizes.size_options:
        current_size = tup[1]
        #attempt to retrieve a possible user input price for current size but set to
        # None if user did not input an associated price
        size_info.append(
            (current_size,
                request.POST.get(f"{current_size} price" ,None),)
        )
    return size_info

# Helper Method

def retrieve_product_options(request):
    """Retrieve user-defined options for a product from html form, adding each to a list
    of tuples

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for additional options for a product
        from an html form
    Return:
    -------
    list of tuples each containing a product option title and description
    """
    product_options_list = []
    for i in range(1, MAX_OPTIONS + 1):
        # attempt to retrieve an option's title and description (optional)
        title = request.POST.get(f"Option{i} title", None)
        description = request.POST.get(f"Option{i} desc", None)
        if title != None :
            description = request.POST.get(f"Option{i} desc")
            product_options_list.append((title, description))

    return product_options_list
    

def add_product(request):
    """Retrieve user-defined attributes from html from from 'create-product', create new
    product and save to database

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for retrieval of attributes for a new product
    """
    # retrieve Product Category, title and description from request
    category = get_object_or_404(models.Category, pk= request.POST['category'])
    title = request.POST['title']
    description = request.POST['description']

    # using helper methods above, retrieve product size and associated prices and possible
    # additional product options as desired by admin user
    size_info_list = retrieve_size_pricing(request)
    product_options_list = retrieve_product_options(request)

    # retrieve unique id for each label that may have been added to a product in htmlm form
    labels_list = [ models.Label.objects.get(id = label_id) 
                    for label_id in request.POST.getlist('labels')]

    # create basic product with compulsory fields
    product = models.Product.objects.create(
                            category = category,
                            title = title,
                            description = description,
        )
    
    # add Each Label (if present) to the Product
    for label in labels_list:
        product.labels.add(label)
    product.save()

    # add (optional) unique size prices
    for product_info in size_info_list:
        if product_info[1] != '':
            product_info = models.Product_Sizes.objects.create(
                                product=product,
                                size = product_info[0],
                                price = product_info[1])
            product_info.save()

    # add (optional) product options
    for option in product_options_list:
        if option[0] != '' and option[1] !='':
            prod_option = models.Option.objects.create(
                product = product,
                title = option[0],
                description = option[1]
            )
            prod_option.save()

    return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))   

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Views for Data Display

def view_all_products(request):
    return HttpResponse("Viewing All Products")