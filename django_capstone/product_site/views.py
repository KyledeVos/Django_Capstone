"""Views Module for Django App 'product_site'. App serves as central site
for web application.

Methods:
--------
:meth:`logincheck(request)`
    Determine if a current user is authenticated

:meth:`populate_display_products(all_products)`
    validate and sort a list of products for website display - checking at least one price
    has been set

:meth:`create_product_list()`
    Retrieve all Categories and Products from database, Sort Products into their
    categories - sorting Products and Categories in Alphabetical order according to title.
    Performs product validation for website display

:meth:`site_home(request)`
    Render main site home page, checking if currently logged-in user is a staff
        member allowing access to admin control functionality

:meth:`determine_discount_percentage(labels)`
    Using QuerySet of associated Labels for a Product, determine highest
    assigned label percentage discount to apply a Product

:meth:`product_view(request, product_id, error)`
    Retrieve Attributes and Selected Pricing for rendering of Individual Product Webpage
    showing Product Details, Pricing and validation of customer login for addition of Product
    to an Order.

:meth:`create_retrieve_order(request)`
    Determine Order for currently logged in user to add selected Product_Item.
        If no open order is present, create a new open order for user.

:meth:`create_order_item(request, product_id)`
    Retrieve Product Attributes and user selected Attributes for a Selected Product.
        Validate against chosen price(s) and size(s) and add Product to open Order
        for User.

:meth:`main_image_control(order_items)`
    Retrieve main image and matching id for products and return as list

:meth:`customer_orders(request, message)`
    Retrieve current logged in customer info and matching Orders information
        for display to client

:meth:`remove_item(request, item_id, order_id)`
    Delete an Order_Item from an order. Delete order if all Order Items have been removed.

:meth:`view_order(request, order_id, message)`
    Retrieve current order (processing or completed status) details for
        display to customer.

:meth:`submit_order(request, order_id)`
    Retrieve an order submitted for processing and change order status
        to received

:meth:`product_review(request, order_item_id, order_id)`
    Allow logged-in user to submit a review for a product that has been paid for
        and delivered

:meth:`review_rating_update(applied_rating, product)`
    Calculate New Average Review rating for a product after a new review
        has been added for the product

:meth:`save_review(request, product_id, order_id)`
    Retrieve customer review attributes and preferences to create new product
        review and assign to the Product
"""
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import date
from crafts_by_micks.models import Category, Label, Product, Product_Sizes, Product_Images, Option, Order_Item, Order, Review

# Helper Function
def logincheck(request):
    """Determine if a current user is authenticated.

    :param request: needed to authenticate current user
    :type request: HTTPRequest object

    :return: True for authenticated user, False if not
    :rtype: boolean
    """
    return True if request.user.is_authenticated else False


# Business Logic - Product Site Validity for Display based on price presence
def populate_display_products(all_products):
    """validate and sort a list of products for website display - checking at least one price
    has been set.

    :param all_products: list containing unvalidated Products
    :type all_products: list

    :return: validated list of Products
    :rtype: list

    NOTE:
     Products without prices are allowed in system (in creation process by admin),
    but may not be displayed on the product site
    """
    # list to hold each product
    product_list = []

    for product in all_products:
        # Retrieve All associated prices for the current product.
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

        # retrieve all labels associated with a product
        labels = Label.objects.filter(product = product)
        current_product['labels'] = labels

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
    """Retrieve all Categories and Products from database, Sort Products into their
    categories - sorting Products and Categories in Alphabetical order according to title.
    Performs product validation for website display.

    :return: list containing tuples as: (category_name, list of valid Products)
    :rtype: list
    """
    # retrieve all product categories - in alphabetical order
    all_categories = Category.objects.order_by('title')
    # list to hold all categories and their associated, valid products for main site display
    category_list = []

    # confirm there are categories loaded, if not there cannot be any products
    # and product to category association is not needed
    if len(all_categories) > 0: 
        for category in all_categories:
            # retrieve all products for each category:
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
    """Render main site home page, checking if currently logged-in user is a staff
        member allowing access to admin control functionality. Retrieves validated
        and sorted list of Categories and associated Products for home page display.

    :param request: required for user authentication, status check and html page render
    :type request: HTTPRequest object

    :return: site home page
    :rtype: HTTPResponse
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


def determine_discount_percentage(labels):
    """Using QuerySet of associated Labels for a Product, determine highest
    assigned label percentage discount to apply a Product.

    :param labels: QuerySet containing Labels that have been assigned to a Product.
    :type labels: QuerySet `Label`

    :return: Highest Percentage Discount applicable to Product Prices
    :rtype: int
    """
    # track highest percentage discount applied
    highest_discount = 0

    # iterate through all labels checking for a new, highest discount to apply
    for label in labels:
        if label.discount_percentage > 0 and label.discount_percentage > highest_discount:
            highest_discount = label.discount_percentage

    return highest_discount


def product_view(request, product_id, error):
    """Retrieve Attributes and Selected Pricing for rendering of Individual Product Webpage
    showing Product Details, Pricing and validation of customer login for addition of Product
    to an Order.

    :param request: required for user authentication, status check and html page render
    :type request: HTTPRequest object
    :param product_id: unique Primary Key value for selected Product
    :type product_id: int
    :param error: description of error to display to user on page - current implementation
        accounts for addition of Product to Order without selection of Size and
        Associated Price
    :type error: str

    :return: page displaying selected Product Attributes for addition to an order or view
            of Product details by user
    :rtype: HTTPResponse
    """
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
    highest_discount = determine_discount_percentage(labels)

    # track if a discount has been applied for notification on project page
    discount_bool = True if highest_discount > 0 else False
    # if there is a discount to apply, modify all product prices to show discount

    for price_option in product_pricing:
        if highest_discount > 0:
            price_option.price *= (highest_discount/100)
        # correct decimals for price
        price_option.price = f"{(round(price_option.price, 2)):.2f}"

    # retrive all possible product additonal images
    product_images = Product_Images.objects.filter(product = product)

    # retrieve all additional product options
    product_options = Option.objects.filter(product = product)

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
        'error': error
    }
    return render(request, 'product_view.html', context)


def create_retrieve_order(request):
    """Determine Order for currently logged in user to add selected Product_Item.
        If no open order is present, create a new open order for user.

    :param request: needed to determine current logged-in user
    :type request: HTTPRequest object

    :return: open order to add a Product Item to or new open Order
    :rtype: Class `Order` instance    
    """
    # retrieve current user (customer)
    customer = request.user

    # attempt to retrieve all orders assigned to customer
    current_orders = Order.objects.filter(customer = customer)
    # no assigned orders- create a new order
    if len(current_orders) == 0:
        new_order = Order.objects.create(
            customer = customer,
            status = 'ns'
        )
        return new_order
    # existing orders do exist
    else:
        # check for current, non-submitted order
        for order in current_orders:
            if order.status == 'ns':
                # open order exists
                return order

        # no open orders for customer, create and return a new order
        new_order = Order.objects.create(
            customer = customer,
            status = 'ns'
        )
        return new_order


def create_order_item(request, product_id):
    """Retrieve Product Attributes and user selected Attributes for a Selected Product.
        Validate against chosen price(s) and size(s) and add Product to open Order
        for User.

    :param request: used to retrieve Product and Selected Attributes from Product_Page
    :type request: HTTPRequest object
    :param product_id: unique Primary Key value for selected Product
    :type product_id: int

    :return: user to site home page
    :rtype: HTTPResponse
    """
    # list of tuples holding a size, price and quantity
    pricing_list = []
    # retrieve list of selected sizes from html form and use to retrieve
    # Product_Size instance
    selected_sizes = [Product_Sizes.objects.filter(pk = id) for id in request.POST.getlist('selected_sizes')]

    # check if user selected at least one price:
    if len(selected_sizes) == 0:
        # a price was not selected - order item invalid
        return HttpResponseRedirect(reverse('product_site:product_view', args=(product_id, "No Price",)))

    # Retrieve all labels associated with the product
    labels = Product.objects.filter(pk = product_id)[0].labels.all()
    # determine highest discount percentage that may be applied to a product
    highest_discount = determine_discount_percentage(labels)

    # for each selected price, retrieve the quantity ordered
    for size_choice in selected_sizes:
        # determine if a discount has been applied
        if highest_discount > 0:
            price = size_choice[0].price * (highest_discount/100)
        else:
            price = size_choice[0].price

        # attempt to retrieve a set quantity
        quantity = request.POST.get(f'{size_choice[0].size} quantity', "1")

        # if quantity was not entered, set default to '1'
        if quantity == "":
            quantity = "1"
        # create tuple of size, price and quantity and add to list
        pricing_list.append((size_choice[0].size, price, quantity))

    # string to store chosen options as text
    product_options = ""
    # retrieve each option id from request that was selected by user
    for id in request.POST.getlist('product_options'):
        # retrieve the matching option from database
        current_option = Option.objects.filter(pk = id)
        # append each option title and description
        product_options += current_option[0].title + ":"
        product_options += current_option[0].description + ";"

    # Create Order item - Each unique size and price set as individual item
    # All items get the same product_options
    for size_option in pricing_list:
        Order_Item.objects.create(
            # retrieve an existing open order or create new order
            order = create_retrieve_order(request),
            product_id = product_id,
            product_title = Product.objects.filter(pk=product_id)[0].title,
            chosen_size = size_option[0],
            price = size_option[1],
            quantity = size_option[2],
            options = product_options
        )

    # Return User to All Products Page
    return HttpResponseRedirect(reverse('product_site:site_home'))

# Helper Function - Construct list of all product main images
def main_image_control(order_items):
    """Retrieve main image and matching id for products and return as list.

    :param order_items: list containg selected Order_Items to retrieve product id and main image from
    :type order_items: list

    :return: list containing product id's and matching main images
    :rtype: list
    """
    # list to hold product_id and its matching image
    product_image_list = []

    # make order_items list contain unique values based on product id
    unique_items = set([item.product_id for item in set(order_items)])
    
    for product_id in unique_items:
        # Retrieve matching product main image
        product_image = get_object_or_404(Product, pk=product_id).product_image
        product_image_list.append([product_id, product_image])

    return product_image_list


def customer_orders(request, message):
    """Retrieve current logged in customer info and matching Orders information
        for display to client

    :param request: Retrieved current logged-in customer and render html page showing order info
    :type request: HTTPRequest object
    :param message: Message to display to user for successful submission of an order for processing
    :type message: str

    :return: user to view customer orders page
    :rtype: HTTPResponse
    """
    # retrieve current logged in customer (user)
    customer = request.user
    #retrieve all orders assigned to a customer
    all_orders = Order.objects.filter(customer = customer)
    # lists to store each order type
    open_orders = []
    processing = []
    completed = []
    # list to store product images for orders not submitted
    product_image_list = []

    # seperate orders
    for order in all_orders:
        # order not yet submitted
        if order.status == 'ns':
            open_orders.append(order)
        # order completed and delivered
        elif order.status == 'c':
            completed.append(order)
        # order awaiting payment, manufacture or delivery
        else:
            processing.append(order)

    # if there is an open order, retrieve all order items
    open_order_items = []
    # track order total value
    order_total = 0
    if len(open_orders) > 0:
        for item in Order_Item.objects.filter(order = order):
            # add item total value to order total value
            order_total += item.price * item.quantity
            # retrieve current item and correct price decimals
            item.price = f"{(round(item.price, 2)):.2f}"
            # retrieve any product options and seperate each option
            item.options = [split_option for split_option in item.options.split(";")]
            open_order_items.append(item)

        # format order total value to two decimal places
        order_total = f"{(round(order_total, 2)):.2f}"
        # retrieve list of product_id and matching main image
        product_image_list = main_image_control(open_order_items)

    context = {
        'customer': customer,
        'open_orders': open_orders,
        'open_order_items': open_order_items,
        'order_total': order_total,
        'processing_orders': processing,
        'completed_orders': completed,
        'product_image_list': product_image_list,
        'message': message
    }

    return render(request, 'customer_orders.html', context)


def remove_item(request, item_id, order_id):
    """Delete an Order_Item from an order. Delete order if all Order Items have been removed.

    :param request: render Orders Display page
    :type request: HTTPRequest object
    :param item_id: primary key field for Order_Time to be deleted
    :type item_id: int
    :param order_id: primary key field for Order holding selecting Order Item
    :type order_id: int

    :return: customer to view orders page
    :rtype: HTTPResponse
    """
    # Retrieve Order_Item for deletion and assigned Order
    order_item = get_object_or_404(Order_Item, pk=item_id)
    order = get_object_or_404(Order, pk = order_id)
    # Delete Order_Item
    order_item.delete()

    # Determine if a non-submitted order has all order_items removed,
    # if so, delete this order
    remaining_items = Order_Item.objects.filter(order = order)
    if len(remaining_items) == 0:
        order.delete()

    # Return customer to Order Display Page
    return HttpResponseRedirect(reverse('product_site:customer_orders', args=("Item Successfully Removed",)))


def view_order(request, order_id, message):
    """Retrieve current order (processing or completed status) details for
        display to customer.

    :param request: render html page displaying order info
    :type request: HTTPRequest object
    :param order_id: primary key for order details being requested
    :type order_id: int
    :param message: informative message to display to customer
    :type message: str

    :return: user to view order page
    :rtype: HTTPResponse
    """
    # retrieve order, status and order_items
    order = get_object_or_404(Order, pk=order_id)
    status = order.status
    order_items = Order_Item.objects.filter(order = order)
    # list to store product_id and associated main image
    product_image_list = main_image_control(order_items)


    # Date Checks and Format
    # 1) Payment Date
    if order.payment_received_date == None:
        payment_date = "Not Recieved / Processing"
    else:
        payment_date = f'Received on: {order.payment_received_date}'

    # Correct Total Value Decimals
    order.total_value = f"{(round(order.total_value, 2)):.2f}"

    for item in order_items:
        # retrieve current item and correct price decimals
        item.price = f"{(round(item.price, 2)):.2f}"
        # retrieve any product options and seperate each option
        item.options = [split_option for split_option in item.options.split(";")]

    context = {
        'order': order,
        'status': status,
        'payment_date': payment_date,
        'order_items': order_items,
        'product_image_list': product_image_list,
        'message': message
    }
    return render(request, 'view_order.html', context)


def submit_order(request, order_id):
    """Retrieve an order submitted for processing and change order status
        to received.

    :param request: Used to return customer to view orders page
    :type request: HTTPRequest object
    :param order_id: primary key of order being submitted for processing
    :type order_id: int

    :return: user to view orders page
    :rtype: HTTPResponse
    """
    # retrieve current order
    order = get_object_or_404(Order, pk = order_id)

    # retrieve order_items for order
    order_items = Order_Item.objects.filter(order = order)
    total_value = 0

    for item in order_items:
        total_value += float(item.price) * int(item.quantity)

    # change status to recieved (displayed as processing on webpage) and save
    order.status = 'r'
    # update submission date
    order.submitted_date = date.today()
    # update order total_value
    order.total_value = total_value
    order.save()

    # return user to orders pages
    return HttpResponseRedirect(reverse('product_site:customer_orders', args=('Order Received', )))


def product_review(request, order_item_id, order_id):
    """Allow logged-in user to submit a review for a product that has been paid for
        and delivered.

        :param request: used to render product review page
        :type request: HTTPRequest object
        :param order_item_id: primary key for product item to be reviewed
        :type order_item_id: int
        :param order_id: primary key of current order needed to return user to order view after
            review of product is submitted
        :type order_id: int

        :return: user to product review page
        :rtype: HTTPResponse
    """
    # retrieve order_item for review
    order_item = get_object_or_404(Order_Item, pk = order_item_id)
    # retrieve product main image
    product_image = get_object_or_404(Product, pk=order_item.product_id).product_image

    context = {
        'order_item': order_item,
        'order_id': order_id,
        'product_image': product_image,
        'max_rating': [str(count) for count in range(1, 6)],
    }
    return render(request, 'product_review.html', context)


# Helper Function - Update Overall Review Rating of Product
def review_rating_update(applied_rating, product):
    """Calculate New Average Review rating for a product after a new review
        has been added for the product

    :param applied_rating: value of review_rating added to a product
    :type applied_rating: int
    :param product: product whose review rating needs to be re-calculated
    :type product: class `Product` instance

    :return: no return        
    """
    # track number of reviews for a product and sum of all ratings
    count = 0
    sum = 0
    # iterate through all product reviews
    for review in Review.objects.filter(product = product):
        count += 1
        sum += review.rating

    # calculate review average rating and update product
    product.review_value = round(sum/count, 1)
    product.save()


def save_review(request, product_id, order_id):
    """Retrieve customer review attributes and preferences to create new product
        review and assign to the Product.
    
    :param request: used to render product review page
    :type request: HTTPRequest object
    :param product_id: primary key of product to which review is to be added
    :type product_id: int
    :param order_id: primary key of current order with product being reviewed
    :type order_id: int

    :return: user to view order page
    :rtype: HTTPResponse
    """
    # determine if customer wants anonymous review
    anonymous = request.POST.get('anonymous_review', 'Anonymous')
    # customer chose to revew with name
    if anonymous != 'checked':
        # retrieve current logged_in user - only logged in user would be able to review
        user = request.user
        author = f"{user.first_name} {user.last_name}"
    # customer wants review to be anonymous
    else:
        author = anonymous

    # Retrieve Review Rating
    rating = int(request.POST['review_value'])
    # Retrieve Review Description - No description provided will have value of 'Optional'
    description = request.POST['review_description']

    # retrieve current product
    product = get_object_or_404(Product, pk=product_id)

    # Create New Review
    review = Review.objects.create(
        product = product,
        author = author,
        description = description,
        rating = rating
    )

    # updating product review rating
    review_rating_update(rating, product)

    return HttpResponseRedirect(reverse('product_site:view_order', args=(order_id, 'Review Submitted' )))
