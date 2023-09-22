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
from crafts_by_micks.models import Category, Product, Product_Sizes, Product_Images, Option, Order_Item

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
        current_product['display_price'] = f"{product_pricing[0].price:.2f}"

        # track if there are multiple sizes available for a product
        current_product['multiple_sizes'] = True if len(product_pricing) > 1 else False

        # add current product to list
        product_list.append(current_product)
    return product_list


# Helper Function
def create_product_list():
    # retrieve all product categories - in alphabetical order
    all_categories = Category.objects.order_by('title')
    # list to hold all categories and their associated, valid products for main site display
    category_list = []

    # confirm there are categories loaded, if not there cannot be any products
    # and product to category association is not needed
    if len(all_categories) > 0: 
        for category in all_categories:
            # retrieve all products  for each category:
            all_products = Product.objects.filter(category=category).order_by('title')    
            # refine product list and validate products that may be put on website display
            current_category_products = populate_display_products(all_products)
            # check for no products - if none do not add current category
            if len(current_category_products) == 0:
                continue
            # add found products to category list for display on main page
            category_list.append([category.title, current_category_products])

    return category_list


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

    # retrieve list of product categories and associated products
    category_products_list = create_product_list()
        
    context = {
        'logged_in': logged_in,
        'username': request.user.username,
        'source' : 'site_home',
        'staff' : staff,
        'products': category_products_list
    }
    return render(request, 'site_home.html', context)


def product_view(request, product_id):

    # Determine if the user has been logged in
    logged_in = logincheck(request)
    # if the user has been checked in, check if they are staff; giving access to admin control
    # of the site
    staff = False
    if logged_in:
        staff = True if request.user.is_staff else False

    # Retrieve product
    product = Product.objects.get(pk = product_id)
    # Retrieve all labels associated with the product
    labels = product.labels.all()
    # Retrieve all associated sizes and prices for the product
    product_pricing = Product_Sizes.objects.filter(product = product)

    # labels can apply discounts to a product price
    highest_discount = 0
    # determine highest discount from labels
    for label in labels:
        if label.discount_percentage > 0 and label.discount_percentage > highest_discount:
            highest_discount = label.discount_percentage
    # track if a discount has been applied for notification on project page
    discount_bool = True if highest_discount > 0 else False
    # if there is a discount to apply, modify all product prices to show discount
    if highest_discount > 0:
        for price_option in product_pricing:
            price_option.price *= (highest_discount/100)
            # correct decimals for price
            price_option.price = f"{(round(price_option.price, 2)):.2f}"

    # retrive all possible product additonal images
    product_images = Product_Images.objects.filter(product = product)

    # retrieve all additional product options
    product_options = Option.objects.filter(product = product)
    print(product_options)

    context = {
        'product': product,
        'labels': labels,
        'discount_bool': discount_bool,
        'price_list': product_pricing,
        'product_images': product_images,
        'options': product_options,
        'logged_in': logged_in,
        'username': request.user.username,
        'source' : 'site_home',
        'staff' : staff,
    }
    return render(request, 'product_view.html', context)


def create_order_item(request, product_id):

    # retrieve current user (customer)
    current_user = request.user

    # list of tuples holding a size, price and quantity
    pricing_list = []
    # retrieve list of selected sizes from html form and use to retrieve
    # Product_Size instance
    selected_sizes = [Product_Sizes.objects.filter(pk = id) for id in request.POST.getlist('selected_sizes')]

    # for each selected price, retrieve the quantity ordered
    for size_choice in selected_sizes:
        # attempt to retrieve a set quantity - html default set to 1
        quantity = request.POST[f'{size_choice[0].size} quantity']
        # create tuple of size, price and quantity and add to list
        pricing_list.append((size_choice[0].size, size_choice[0].price, quantity))

    # string to store chosen options as text
    product_options = ""
    # retrieve each option id from request that was selected by user
    for id in request.POST.getlist('product_options'):
        # retrieve the mathcing option from datase
        current_option = Option.objects.filter(pk = id)
        # append each option title and description
        product_options += current_option[0].title + ":"
        product_options += current_option[0].description + ";"

    # Create Order item - Each unique size and price set as individual item
    # All items get the same product_options
    for size_option in pricing_list:
            
        Order_Item.objects.create(
            customer = current_user,
            product_id = product_id,
            product_title = Product.objects.filter(pk=product_id)[0].title,
            chosen_size = size_option[0],
            price = size_option[1],
            quantity = size_option[2],
            options = product_options
        )
    
    return HttpResponse(f'Create Order Item for product {product_id}')

