"""Views Module for Django App 'crafts_by_micks' serving as project admin site and control

Methods:
--------
home_page(request):
    render admin home app of app with SignUp, Login and Product Catalog

create_category(request, source, error):
    render html page allowing admin user to create a Category for Products to belong to.
    Pass in source argument determining page to return to after Category addition to database.

add_category(request, source):
    Retrieve Category Attributes from html form, create new Category instance and save to
    database. Use 'source' determining page to return to after new category is added.

create_label(request, source, error):
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

retrieve_additional_images(request):
    Retrieve possible additional product images uploaded by admin user and append
    image title and image file to a list

add_product(request):
    Retrieve user-defined attributes from html from from 'create-product', create new
    product and save to database.

view_all_labels(request):
    Retrieve all labels from database for render to html page

view_all_products(request):
    retrieve and sort all products alphabetically in order of category and then product title
    passing list to html page for rendering

view_all_categories(request, error):
    Provide all categories for html page render and pass on possible error message to display during
    category update or deletion

update_delete_category(request, category_id):
    Use 'request' to determine action (update or delete) to perform on category specified by
    category_id. Handle possible errors and return error message when reloading update/deletion page

update_label(request, label_id, error):
    Retrieve current label for update and render html page showing current set label attributes.
        Form in page allows user to change label attributes and pass on for save to database.

update_product(request, product_id, error):
    Retrieve current attributes for a Product and Display to new page allowing
    user to perform updates to these attributes to update product information

save_update(request, product_id):
    Retrieve old/new attributes for a current product from html form for product update
        and perform applicable updates to Product and associated model instances.

delete_label(request, label_id):
    Retrieve current label and perform deletion from database

initial_product_deletion(request, product_id):
    Retrieve current product selected by user for deletion and return confirmation
    page to confirm if deletion is correct

confirmed_product_deletion(request, product_id):
    Retrieve deletion confirmation from html form used to determine if application is
    to go ahead with deletion or not. If so, retrieve product and perform deletion

all_customers(request):
    Retrieve All saved customers and their associated orders. Determine order status
        for 'action_required' notification to admin user

customer_orders(request, customer_id):
    Retrieve and sort customer orders into not paid, processing and completed

view_order(request, order_id, customer_id, type):
    Retrieve an format an individual customer order for render

change_order_status(request, order_id, customer_id, new_status):
    Allow admin user to change order status after payment received and then after
        product has been delivered

"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from datetime import date
from . import models

def home_page(request):
    """render admin home app of app with SignUp, Login and Product Catalog"""
    return render(request, 'home_page.html')

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for New Product Creation

# max allowed desired options for a product
MAX_OPTIONS = 5
# max allowed additional images for a product
MAX_IMAGES = 10

def create_category(request, source, error):
    """render html page allowing admin user to create a Category for Products to belong to.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new category is added
        to database.
    error: str
        message to display to user if duplicated category title is received
    """
    return render(request, 'creation/create_category.html', {'source':source, 'error':error})


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
    # attempt to create and save new title unless duplicate title was supplied
    try:
        title = request.POST['title']
        category = models.Category.objects.create(title=title)
        category.save()
        # new category was created during product creation, return admin user to 'create_product' page
        if source == "new_product":
            return HttpResponseRedirect(reverse('crafts_by_micks:create_product', args=("None",)))
        # new category was created seperately, return admin user to main admin page
        else:
            return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))

    # duplicate category title 
    except IntegrityError:
        return HttpResponseRedirect(reverse('crafts_by_micks:create_category', args=(source, "Duplicate Name",)))

def create_label(request, source, error):
    """render html page allowing admin user to create a new Label for Products.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    source: str
        Specify name of original view call determing page to return to after new label is added
        to database
    error: str
        message to display to user if duplicated label title is received
    """
    return render(request, 'creation/create_label.html',  {'source':source, 'error':error})
        

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
    try:
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
            return HttpResponseRedirect(reverse('crafts_by_micks:create_product', args=("None",)))
        # new category was created seperately, return admin user to main admin page
        else:
            return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))
    
    # duplicate category title
    except IntegrityError:
        return HttpResponseRedirect(reverse('crafts_by_micks:create_label', args=(source, "Duplicate Name",)))

    
def create_product(request, error):
    """Render html page allowing admin user to create a new product seeing number of allowed
    product options and passing allowed size options, current product Categories and Labels

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata about the request needed for html page render
    error: str
        message to display to user if duplicated Product title is received
    """
    # create list of option numbers (as strings) used by 'create_product.html' for
    # Product Options creation
    options_list = []
    for i in range(1, MAX_OPTIONS + 1):
        options_list.append(str(i))

    # create list to specify an additional image number that can be added
    # to a product
    images_list = []
    for i in range(1, MAX_IMAGES + 1):
        images_list.append(str(i))

    # retrieve current product size options
    size_choices = []
    for tup in models.Product_Sizes.size_options:
        size_choices.append(tup[1])

    # retrieve all currently created product categories and labels
    categories = models.Category.objects.all()
    labels = models.Label.objects.all()

    context = {"size_choices": size_choices,
               "options_list": options_list,
               "images_list": images_list,
               "categories": categories,
               "labels":labels,
               "source": 'new_product',
               'error': error}
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

def retrieve_additional_images(request):
    """Retrieve possible additional product images uploaded by admin user and append
        image file to a list.
    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for retrieval of additional image's
         image file from an html form
    Return:
    -------
    list containing image files
    """
    additional_images = []
    for i in range(1, MAX_IMAGES + 1):
            try:
                # attempt to retrieve image
                new_image = request.FILES[f"Image{i} image"]
                additional_images.append(new_image)
            except:
                # If no image has been given, do nothing
                pass
    return additional_images


def add_product(request):
    """Retrieve user-defined attributes from html from from 'create-product',
        create new product and save to database

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for retrieval of attributes for a new product
    """
    try:
        # retrieve Product Category, title and description from request
        category = get_object_or_404(models.Category, pk= request.POST['category'])
        title = request.POST['title']
        description = request.POST['description']

        # retrieve product main image
        product_image = request.FILES['main_image']

        # using helper methods above, retrieve product size and associated prices, possible
        # additional product options and images as desired and provided by admin user
        size_info_list = retrieve_size_pricing(request)
        product_options_list = retrieve_product_options(request)
        additional_images = retrieve_additional_images(request)

        # retrieve unique id for each label that may have been added to a product in html form
        labels_list = [ models.Label.objects.get(id = label_id) 
                        for label_id in request.POST.getlist('labels')]

        # create basic product with compulsory fields
        product = models.Product.objects.create(
                                category = category,
                                title = title,
                                description = description,
                                product_image = product_image
            )
        
        # add possible labels to product
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

        # add optional product additional images and save
        for current_image in additional_images:
            if current_image != '':
                models.Product_Images.objects.create(
                    product = product,
                    image = current_image
                ).save()
                
    # duplicate Product title - Return User to Create Product
    except IntegrityError:
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product', args=("Duplicate Name",)))

    # return to admin home page
    return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))   

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for Data Display

def view_all_labels(request):
    """Retrieve all labels from database for render to html page.

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for html page render
    """
    labels = models.Label.objects.all()
    return render(request, 'display/view_all_labels.html', {'labels': labels})

def view_all_products(request):
    """retrieve and sort all products alphabetically in order of category and then product title
    passing list to html page for rendering

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for html page render

    NOTE:
    -----
    current implementation will sort categories and products into alphabetical order
    """
    # retrieve all products, ordering alphabetically by category title and then by product title
    products = models.Product.objects.order_by('category__title', 'title')
    # list to hold lists category name [0] and associated products as remaining elements
    prod_categories = []

    # check if there are any saved products
    if products.exists():
        # first iteration will have no tracking title
        current_title = 'none'
        # track current category to which products are being added
        category_count = 0
        for product in products:

            # first iteration with no category title tracking. Add first category name and product
            if current_title == "none":
                prod_categories.append([product.category.title, product])
                current_title = product.category.title
            # add current product that belongs to current category
            elif current_title == product.category.title:
                prod_categories[category_count].append(product)
            # new category - increment category count and create new list with new category
            # name and product
            else:
                category_count+=1
                prod_categories.append([product.category.title, product])
                current_title = product.category.title

    # call html page to display all products to admin
    return render(request, 'display/view_all_products.html', {'prod_categories': prod_categories})

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for Data Update and Possible Deletion

def view_all_categories(request, error):
    """Provide all categories for html page render and pass on possible error message to display during
    category update or deletion

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for html page render
    error: string
        description of possible error that may occur that during category update or deletion
    """
    categories = models.Category.objects.all()
    return render(request, 'Update/view_all_categories.html', {'categories': categories, 'error':error})

def update_delete_category(request, category_id):
    """Use 'request' to determine action (update or delete) to perform on category specified by
    category_id. Handle possible errors and return error message when reloading update/deletion page

    Parameter:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed to determine action to undertake (update or delete) and
        retrieve attributes from html form to perform action
    category_id: int
        primary key id of category to be updated or deleted
    """
    # retrieve the current category
    category = get_object_or_404(models.Category, pk = category_id)

    # 1) if user has selected to update the category title
    try:
        if 'Update' in request.POST:
            new_title = request.POST['title']
            # if a new title was given, change category title to new title and save
            if new_title != '':
                category.title = new_title
                category.save()
            return HttpResponseRedirect(reverse('crafts_by_micks:view_all_categories', args=("none",)))
    except IntegrityError:
            # user has entered a title that is not unique
            return HttpResponseRedirect(reverse('crafts_by_micks:view_all_categories', args=("Update Error",)))
            
    # 2) if user has selected to delete the category
    # NOTE - Deletion of a Category cannot be done if any products have been assigned to it
    if 'Delete' in request.POST:
        # retrieve count of all possible products that may assigned to current category
        product_count = len(models.Product.objects.filter(category = category))
        print(f"Products:  {product_count}")
    
        if product_count == 0:
            # if there are no products assigned to the category, deletion may be performed
            category.delete()
            return HttpResponseRedirect(reverse('crafts_by_micks:view_all_categories', args=("none",)))
        else:
            # category has assigned products, display error to user that deletion may not be performed
            return HttpResponseRedirect(reverse('crafts_by_micks:view_all_categories', args=("Delete Error",)))
        

def update_label(request, label_id, error):
    """Retrieve current label for update and render html page showing current set label attributes.
        Form in page allows user to change label attributes and pass on for save to database.

    Parameters:
    ----------
    request: HTTPRequest object
        pass current label to page to display attributes
    label_id: int
        primary key id for current label selected by user for update
    error: string
        Description of error message to display for user
        Current Implementation is only for updated Label title that is not unique
        
        """
    label = get_object_or_404(models.Label, pk=label_id)
    return render(request, 'Update/update_label.html', {'label': label, 'error': error})


def save_label_update(request, label_id):
    """Retrieve possible new label attributes from an html form (passed through request) and attempt
    to perform updates to current label and save to database

    Parameters:
    ----------
    request: HTTPRequest object
        retrieve possible updated label attributes from html form
    label_id: int
        primary key id for current label selected by user for update
    """
    # retrieve the current label
    label = get_object_or_404(models.Label, pk=label_id)
    # retrieve possible new title
    new_title = request.POST['title']
    # if user has provided a new title, update label title (duplicate checked during attempted save)
    if new_title != '':
        label.title = new_title

    # retrieve possible new discount percentage
    new_discount = request.POST.get('discount_percentage', 'none')
    if new_discount!= "" and new_discount != '0':
        label.discount_percentage = new_discount

    # retrieve possible new days until label is to be removed
    new_removal = request.POST['removal_days']
    if new_removal != '':
        label.removal_days = new_removal
    else:
        label.removal_days = -1

    # retrieve possible new custom_colour for label:
    custom_colour = request.POST['custom_colour']
    if custom_colour != label.custom_colour:
        print("Different Colour")
        label.custom_colour = custom_colour
    
    try:
        # attempt to save changes to label
        label.save()
        # return user to page of all labels
        return HttpResponseRedirect(reverse('crafts_by_micks:view_all_labels'))
    except IntegrityError:
        # user has attempted to save with duplicated label title, provide error and return user
        # to update label page
        return HttpResponseRedirect(reverse('crafts_by_micks:update_label', args=(label.id, "Duplicated Name",)))       

def update_product(request, product_id, error):
    """Retrieve current attributes for a Product and Display to new page allowing
    user to perform updates to these attributes to update product information
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for html page render with
        current product attributes
    product_id: int
        primary key id for current product selected by user for update
    error: string
        Description of error message to display for user
        Current Implementation is only for updated Product title that is not unique
    """
    # retrieve current product for update
    product = get_object_or_404(models.Product, pk = product_id)
    # retrieve currently set sizes and associated prices for object
    sizes_prices = models.Product_Sizes.objects.filter(product=product)
    # retrieve names all allowed size options
    all_sizes = [size[1] for size in models.Product_Sizes.size_options]
    # retrieve all product options
    options = models.Option.objects.filter(product=product)
    # retrieve all additional product images that may have been added
    current_images = models.Product_Images.objects.filter(product = product)
    
    # if the current number of options for a product is less than the max allowed,
    # determine number of options that can still be added and add each option number
    # to a list
    more_options = []
    if len(options) < MAX_OPTIONS:
        for new_option in range(1, MAX_OPTIONS -len(options) + 1):
            more_options.append(new_option)

    # determine if there are still extra images that may be added on to a product
    extra_images = []
    if len(current_images) < MAX_IMAGES:
        for new_image in range(len(current_images) + 1, MAX_IMAGES + 1):
            extra_images.append(new_image)

    # create a new prices_sizes list
    new_size_list = []
    # variable to track for populated size price for Product
    match = False

    # loop through all sizes checking for a populated size for the product, if
    # one is match - add its price. If not, set price to 0
    for size in all_sizes:
        match = False
        for current in sizes_prices:
            if size == current.size:
                new_size_list.append([size, current.price])
                match = True
                break
        if not match:
            new_size_list.append([size, 0.0])

    # retrieve product currrent category name
    current_category = product.category.title
    # rerieve all categories
    all_categories = models.Category.objects.all()

    # retrieve labels associated with product
    current_labels = product.labels.all()
    # retrieve all labels stored in database
    all_labels = models.Label.objects.all()
    # list to store labels not assigned to the current product
    not_assigned = []
    
    # iterate through all labels in database, checking and adding those not assigned
    # to the current product to 'not_assigned' list
    for label in all_labels:
        match = False
        for assigned in current_labels:
            # label match found, do not add to list
            if label.title == assigned.title:
                match = True
                break
        if not match:
            # label has not been assigned to product
            not_assigned.append(label)
        # reset match for next iteration
        match = False

    context = {
        'product': product,
        'sizes_prices': sizes_prices,
        'all_sizes' : new_size_list,
        'options':options,
        'more_options': more_options,
        'current_images': current_images,
        'extra_images': extra_images,
        'current_category': current_category,
        'all_categories': all_categories,
        'current_labels': current_labels,
        'not_assigned': not_assigned,
        'error': error
    }

    return render(request, 'Update/update_product.html', context)


def save_update(request, product_id):
    """Retrieve old/new attributes for a current product from html form for product update
        and perform applicable updates to Product and associated model instances.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for retrieval of product attributes from
        html form
    product_id: int
        primary key id for current product select by user for update
    """
    # retrieve current product to be updated
    product = get_object_or_404(models.Product, pk = product_id)

    # ---- Category Update ----
    category = get_object_or_404(models.Category, pk= request.POST['category'])
    product.category = category

    # ---- Labels Update ----
    # retrieve unique id for each label that may have been added to a product in html form
    labels_list = [ models.Label.objects.get(id = label_id) 
                    for label_id in request.POST.getlist('labels')]
    
    # clear all labels assigned to product
    product.labels.clear()
    # add Each Label (if present) to the Product
    for label in labels_list:
        product.labels.add(label)

    # ---- Title and Description Update ----
    title = request.POST['title']
    product.title = title
    description = request.POST['description']
    product.description = description

    # ---- Main Image Update ----
    # attempt to retrieve possible new image, but set to None if image was not changed
    new_main_image = request.FILES.get("new_main_image" , None)
    if new_main_image != None:
        product.product_image.delete(save=False)
        product.product_image = new_main_image

    # ---- Size Pricing ----
    # retrieve all updated and possible new sizes from html form
    price_list = retrieve_size_pricing(request)
    # retrieve all prices currently assigned to product
    product_pricing = models.Product_Sizes.objects.filter(product = product)

    # track if match for existing price was found against new/updated price
    match = False
    # compare each updated/new price from form against current prices assigned to product
    # checking for first match on size
    for new_price in price_list:
        for current_price in product_pricing:
            # if a matching size was found
            if current_price.size == new_price[0]:
                match = True
                # check if price was set to 0, delete product_price:
                if int(float(new_price[1])) == 0:
                    current_price.delete()
                    break
                # check if there is a difference on the price, if so 
                # update the price
                elif current_price.price != new_price[1]:
                    current_price.price = new_price [1]
                    current_price.save()
                    break
        # at this point, no match for a set price was found indicating it is a new price
        # for the product
        if not match and int(float(new_price[1])) != 0:
            # create new product_price with size and associated price and save
            product_size = models.Product_Sizes.objects.create(
                                    product=product,
                                    size = new_price[0],
                                    price = new_price[1])
            product_size.save()
        # reset match for next iteration
        match = False

    # ---- Product Options - Current ----
    # retrieve all options currently assigned to product
    assigned_options = models.Option.objects.filter(product = product)
    # determine original number of options assigned to product to determine
    # number of additional options user was allowed to add
    additonal_options_count = MAX_OPTIONS - len(assigned_options)

    for option in assigned_options:
        # determine if admin has selected option to be removed
        option_delete = request.POST.get(f"Option{option.id} delete", "none")
        if option_delete == 'delete':
            # delete option and move to next iteration for next option
            option.delete()
            continue

        # attempt to retrieve option from html page with matching title id
        # to a current option
        retrieved_option_title = request.POST[f'Option{option.id} title'] 
        retrieved_option_description = request.POST[f'Option{option.id} desc']

        # check the possible new title is not empty nor contains only spaces
        if retrieved_option_title != "" and not retrieved_option_title.isspace():
            # determine if the title has been changed, if so update title
            if option.title != retrieved_option_title:
                option.title = retrieved_option_title
                option.save()

        # check the possible new description is not empty nor contains only spaces
        if retrieved_option_description != "" and not retrieved_option_description.isspace():
            # determine if the descripttion has been changed, if so update description
            if option.description != retrieved_option_description:
                option.description = retrieved_option_description
                option.save()

    # ---- Product Options - New ----
    for count in range(1, additonal_options_count + 1):
        # attempt to retrieve a posssible new option title and description
        new_option_title = request.POST.get(f"Option{count} title", 'none')
        new_option_desc = request.POST.get(f"Option{count} desc", 'none')
        # check if new title and description was recieved and non_empty
        if new_option_title != '' and not new_option_title.isspace():
            if new_option_desc != '' and not new_option_desc.isspace():
                # valid Title and Description gives, create new product option
                prod_option = models.Option.objects.create(
                    product = product,
                    title = new_option_title,
                    description = new_option_desc
                )
                prod_option.save()
        
    # ---- Additional Product Images ----
    # retrieve list of product_images that were marked for deletion
    deletion_images_list = request.POST.getlist('deletion_images')
    for image_delete in deletion_images_list:
        # using id's of images recieved from form, find matching
        # product_image, delete image file seperately and then delete the instance
        image_object = models.Product_Images.objects.filter(pk = image_delete)
        image_object[0].image.delete(save=False)
        image_object.delete()

    # retrieve all images currently assigned to product (after deletion above are completed)
    assigned_images = models.Product_Images.objects.filter(product = product)
        
    # if the product has assigned images that could have been changed
    if len(assigned_images) > 0:
        # check each image (id) against any possible image that may been provided
        # as a replacement
        for current_image in assigned_images:
            try:
                new_image = request.FILES.get(f"{current_image.id} new" , None)
                if new_image != None:
                    # a new image has been found with a match the current assigned image id
                    # delete the current image, assign the new image and save the change    
                    current_image.image.delete(save=False)
                    current_image.image = new_image
                    current_image.save()
            except:
                # a new image was not found, do nothing - user did not want to change image
                pass
    
    # determine number of allowed new images starting from 1 more than those assigned
    # attempt to retrieve any newly added images
    for count in range(len(assigned_images)+1, MAX_IMAGES + 1):
        try:
            new_image = request.FILES.get(f"{count} new_image" , None)
            if new_image != None:
                # a new image has been found with a match the current assigned image id
                # delete the current image, assign the new image and save the change    
                models.Product_Images.objects.create(
                    product = product,
                    image = new_image
                ).save()
        except:
            # new image was not added, do nothing
            pass
    
    # attempt to save product changes
    try:
        product.save()
    except IntegrityError:
        # non-unique Product Title was set
        return HttpResponseRedirect(reverse('crafts_by_micks:update_product', args=(product.id, "Duplicate Name",)))

    # no errors occured in updating product, return user to display of all products
    return HttpResponseRedirect(reverse('crafts_by_micks:view_all_products'))


# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for Data Deletion (only)

def delete_label(request, label_id):
    """Retrieve current label and perform deletion from database.
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed to render all labels page after label deletion
    label_id: int
        primary key id for current label selected by user for deletion"""
    # retrieve label for deletion
    label = get_object_or_404(models.Label, pk = label_id)
    # perform deletion
    label.delete()
    # return user to view all labels
    return HttpResponseRedirect(reverse('crafts_by_micks:view_all_labels'))


def initial_product_deletion(request, product_id):
    """Retrieve current product selected by user for deletion and return confirmation
    page to confirm if deletion is correct.

    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request to display deletion confirmation page
    product_id: int
        primary key id for current product selected by user for deletion
    """
    # retrieve current product up for deletion
    product = get_object_or_404(models.Product, pk=product_id)
    return render(request, 'Deletion/product_initial_deletion.html', {'product':product})


def confirmed_product_deletion(request, product_id):
    """Retrieve deletion confirmation from html form used to determine if application is
    to go ahead with deletion or not. If so, retrieve product and perform deletion
    
    NOTE:
    Deletion of Product will cascade to deletion of product associated Sizes_Prices and Product Options
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request to retrieve user confirmation for deletion or not
    product_id: int
        primary key id for current product selected by user for deletion
    """
    # check if deletion of product is correct
    if 'Delete' in request.POST:
        # retrieve current product for deletion and perform deletion
        product = get_object_or_404(models.Product, pk = product_id)
        # delete product main image seperately
        product.product_image.delete(save=False)

        # retrieve each additional Product Image
        additional_images = models.Product_Images.objects.filter(product = product)
        for current_image in additional_images:
            # delete image file seperately
            current_image.image.delete(save=False)
            # delete product_image instance
            current_image.delete()

        # delete product
        product.delete()

    # return user to all products page
    return HttpResponseRedirect(reverse('crafts_by_micks:view_all_products'))

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for Customer and Order Details

def all_customers(request):
    """Retrieve All saved customers and their associated orders. Determine order status
        for 'action_required' notification to admin user.
         
    Parameter:
    ----------
    request: HTTPRequest object
        used to render page displaying all customer orders and their status
    """
    # retrieve all customers
    customers = models.User.objects.filter(is_staff=False)
    # list to store customer and 'action_required' boolean
    customer_status = []
    # track action required for a customer
    action_required = False
    
    # for each customer, determine if an order is not yet completed and still requires attention
    for customer in customers:
        # retrieve all orders assigned to customer
        customer_orders = models.Order.objects.filter(customer = customer)
        for order in customer_orders:
            # determine if order recieved but no payment yet
            if order.status == 'r':
                action_required = True
                customer_status.append([customer, "Awaiting Payment"])
                break
            # payment recieved - order being processed
            elif order.status == 'p':
                customer_status.append([customer, "Payment Received - Processing"])
                # order submitted
                action_required = True
                break
        if action_required == False:
            # order has either not been submitted yet or has been completed
            customer_status.append([customer, False])
        else:
            # reset for next customer loop
            action_required == False

    return render(request, 'Display/all_customers.html', {'customer_status': customer_status})

def customer_orders(request, customer_id):
    """Retrieve and sort customer orders into not paid, processing and completed.
    
    Parameters:
    ----------
    request: HTTPRequest object
        used to render page displaying seperated customer orders
    customer_id: int
        Customer primary key
    """
    #Lists to sort customer orders:
    awaiting_payment_orders = []
    processing_orders = []
    completed_orders = []

    # retrieve current customer
    customer = get_object_or_404(models.User, pk=customer_id )
    # retrieve all orders associated with customer
    all_orders = models.Order.objects.filter(customer = customer)

    # sort orders into above lists  
    for order in all_orders:
        # ordered received and awaiting payment
        if order.status == 'r':
            awaiting_payment_orders.append(order)
        # order paid and being processed
        elif order.status == 'p':
            processing_orders.append(order)
        # order delivered and completed
        elif order.status == 'c':
            completed_orders.append(order)

    context = {
        'customer': customer,
        "awaiting_payment_orders": awaiting_payment_orders,
        'processing_orders': processing_orders, 
        'completed_orders': completed_orders,
        'customer_id': customer_id
    }

    return render(request, 'display/customer_orders.html', context)


def view_order(request, order_id, customer_id, type):
    """Retrieve an format an individual customer order for render.

    Parameters:
    ----------
    request: HTTPRequest object
        used to render page displaying order details
    order_id: int
        primary key to retrieve specific order
    customer_id: int
        primary key for customer to whom order is assigned
    type: str
        description of order type (not_paid, processing or completed)
    """
    # retrieve the current order
    order = get_object_or_404(models.Order, pk=order_id)
    # retrieve all items associated with this order
    order_items = models.Order_Item.objects.filter(order = order)
    # retrieve and format order total:
    total_value = f"{(round(order.total_value, 2)):.2f}"

    
    for item in order_items:
        # correct decimals in product price
        item.price = f"{(round(item.price, 2)):.2f}"
        # retrieve any product options and seperate each option
        item.options = [split_option for split_option in item.options.split(";")]
    
    context = {
        'order_items': order_items,
        'order_id': order_id,
        'order' : order,
        'customer_id': customer_id,
        'type': type,
        'total_value': total_value
    }

    return render(request, 'Display/view_order.html', context)


def change_order_status(request, order_id, customer_id, new_status):
    """Allow admin user to change order status after payment received and then after
        product has been delivered
        
    Parameters:
    -----------
    request: HTTPRequest object
        used to return customer to view_order page
    order_id: int
        primary key for order whose status is to changed
    customer_id: int
        primary key of current customer needed for return to view_order page
    new_status: str
        description of new status to be applied to order
    """
    #Retrieve the current order
    order = get_object_or_404(models.Order, pk = order_id)

    # payment recieved - order status must be changed to paid
    if new_status == "paid":
        order.status = 'p'
        order.payment_received_date = date.today()
        order.save()
        return HttpResponseRedirect(reverse('crafts_by_micks:view_order', args=(order_id, customer_id, 'processing')))
        
    # order has been processed and delivered to customer
    else:
        order.status = 'c'
        order.delivered_date = date.today()
        order.save()
        return HttpResponseRedirect(reverse('crafts_by_micks:view_order', args=(order_id, customer_id, 'completed')))

    