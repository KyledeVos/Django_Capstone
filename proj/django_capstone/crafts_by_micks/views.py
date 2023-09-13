"""Views Module for Django App 'Polls'

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

add_product(request):
    Retrieve user-defined attributes from html from from 'create-product', create new
    product and save to database.

view_all_products(request):
    retrieve and sort all products alphabetically in order of category and then product title
    passing list to html page for rendering

view_all_categories(request, error):
    Provide all categories for html page render and pass on possible error message to display during
    category update or deletion

update_delete_category(request, category_id):
    Use 'request' to determine action (update or delete) to perform on category specified by
    category_id. Handle possible errors and return error message when reloading update/deletion page

update_product(request, product_id, error):
    Retrieve current attributes for a Product and Display to new page allowing
    user to perform updates to these attributes to update product information

save_update(request, product_id):
    Retrieve old/new attributes for a current product from html form for product update
        and perform applicable updates to Product and associated model instances.
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from . import models
from datetime import date
import copy


def home_page(request):
    """render admin home app of app with SignUp, Login and Product Catalog"""
    return render(request, 'home_page.html')

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for New Product Creation

# max allowed desired options for a product
MAX_OPTIONS = 5

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
            return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
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
            return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
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
    

def add_product(request):
    """Retrieve user-defined attributes from html from from 'create-product', create new
    product and save to database

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

        # using helper methods above, retrieve product size and associated prices and possible
        # additional product options as desired by admin user
        size_info_list = retrieve_size_pricing(request)
        product_options_list = retrieve_product_options(request)

        # retrieve unique id for each label that may have been added to a product in html form
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

    # duplicate Product title - Return User to Create Product
    except IntegrityError:
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product', args=("Duplicate Name",)))

    # return to admin home page
    return HttpResponseRedirect(reverse('crafts_by_micks:home_page'))   

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for Data Display

def view_all_labels(request):

    # retrieve all product labels
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
    if not products.exists():
            prod_categories['empty'] = 'empty'
    else:
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
# Views for Data Update

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
    label = get_object_or_404(models.Label, pk=label_id)
    return render(request, 'Update/update_label.html', {'label': label, 'error': error})


def save_label_update(request, label_id):

    # retrieve the current label
    label = get_object_or_404(models.Label, pk=label_id)
    # retrieve possible new title
    new_title = request.POST['title']
    if new_title != '':
        label.title = new_title
    
    try:
        label.save()
        return HttpResponseRedirect(reverse('crafts_by_micks:view_all_labels'))
    except IntegrityError:
        return HttpResponseRedirect(reverse('crafts_by_micks:update_label', args=(label.id, "Duplicated Name",)))

 
    return HttpResponse("Saving")
       

def update_product(request, product_id, error):
    """Retrieve current attributes for a Product and Display to new page allowing
    user to perform updates to these attributes to update product information
    
    Parameters:
    ----------
    request: HTTPRequest object
        contains metadata from a request needed for html page render with
        current product attributes
    product_id: int
        primary key id for current product select by user for update
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
    
    # if the current number of options for a product is less than the max allowed,
    # determine number of options that can still be added and add each option number
    # to a list
    if len(options) < MAX_OPTIONS:
        more_options = []
        for new_option in range(len(options) + 1, MAX_OPTIONS + 1):
            more_options.append(new_option)

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

    # ---- Product Options ----
    # retrieve possible options from html form
    request_options = retrieve_product_options(request)
    # retrieve all options currently assigned to product
    assigned_options = models.Option.objects.filter(product = product)
    # retrieve all current option Titles - will be used later to determine assigned
    # options that need to be deleted
    options_delete = [option.title for option in assigned_options]
    
    # track if an object exists in database matching those recieved from html form
    match = False
    for request_option in request_options:
        for assigned_option in assigned_options:
            # option with matching title found
            if assigned_option.title == request_option[0]:
                match = True
                # remove this option from assigned options to be deleted
                options_delete.remove(assigned_option.title)
                # check if the description has changed
                if assigned_option.description != request_option[1]:
                    # change and save new description
                    assigned_option.description = request_option[1]
                    assigned_option.save()
                    print(f"Deleting : {options_delete}")
                    # move to new retrieved option from html form
                    break

        # existing option was not found to match any retrieved
        if not match:
            # 1) user has added a new option, ensure description was added for the title
            if request_option[0] != "":
                # create and save new product option
                prod_option = models.Option.objects.create(
                        product = product,
                        title = request_option[0],
                        description = request_option[1]
                    )
                prod_option.save()
            # reset match for next iteration
        match = False

    # check if there are any titles left in those assigned to products, if so they 
    # are to be deleted (user removed or changed title)
    if len(options_delete)> 0:
        for deletion_option in options_delete:
            current_option = models.Option.objects.filter(title = deletion_option)
            current_option.delete()

    # attempt to save product with possible newly updated title, description, category and/or labels
    try:
        product.save()
    except IntegrityError:
        # duplicated product name was given for update, return user to update page and pass error message
        # for display
        print("Duplicate Name")
        return HttpResponseRedirect(reverse('crafts_by_micks:update_product', args=(product.id, "Duplicate Name",))) 
    
    # no errors occured in updating product, return user to display of all products
    return HttpResponseRedirect(reverse('crafts_by_micks:view_all_products'))


