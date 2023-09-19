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
from crafts_by_micks.models import Product, Product_Sizes

# Helper Function
def logincheck(request):
    """Determine if a current user is authenticated. """
    return True if request.user.is_authenticated else False

# Business Logic - Define and Sort Product Attributes
def populate_display_products(all_products):

    # list to hold each product
    product_list = []

    for product in all_products:
        # Retrieve All associated prices for the current product. Products
        # without prices are allowed in system (in creation process by admin),
        # but may not be displayed on the product site
        product_pricing = Product_Sizes.objects.filter(product = product)

        # no associated prices, move to next product
        if len(product_pricing) == 0:
            continue

        # product attributes stored in a dictionary
        current_product = {}
        print(f"Pricing: {product_pricing}")
        # retrieve compulsory fields for product with pricing options
        current_product['id'] = product.id
        current_product['category'] = product.category.title
        current_product['title'] = product.title
        current_product['main_image'] = product.product_image
        current_product['review_value'] = product.review_value

        # -- PRICING --
        # Product will have at least one price assigned to it (various sizes).
        # Logic - use 'no' size or smallest product size price as default
        # 1) Check if price of no-size was set, acts as default:
        current_product['display_price'] = product_pricing[0].price

        # track if there are multiple sizes available for a product
        current_product['multiple_sizes'] = True if len(product_pricing) > 1 else False

        # add current product to list
        product_list.append(current_product)
    return product_list


def site_home(request):
    """Render main site home page, checking
     if currently logged-in user is a staff
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

    # retrieve all products
    all_products = Product.objects.all()
    # refine product list and validate products that may be put on website display
    valid_products = populate_display_products(all_products)
    print(valid_products)
        
    context = {
        'logged_in': logged_in,
        'username': request.user.username,
        'source' : 'site_home',
        'staff' : staff,
        'products': valid_products,
    }
    return render(request, 'site_home.html', context)
