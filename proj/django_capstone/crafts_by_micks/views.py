from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse
from . import models
from datetime import date


def home_page(request):
    return render(request, 'home_page.html')

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Views for New Product Creation

# max allowed desired options for a product
MAX_OPTIONS = 5

def create_category(request, source):
    
    return render(request, 'create_category.html', {'source':source})


def add_category(request, source):

    title = request.POST['title']
    category = models.Category.objects.create(title=title)
    category.save()
    if source == "new_product":
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
    else:
        return HttpResponse('admin page for New Category under construction')

def create_label(request, source):
    return render(request, 'create_label.html', {'source': source})
        

def add_label(request, source):
    title = request.POST['title']

    discount_percentage = request.POST.get('discount_percentage', 0)
    if discount_percentage=="":
        discount_percentage = 0

    creation_date = date.today()
    removal_days = request.POST.get('removal_days', '-1')
    if removal_days=="":
        removal_days = -1
    colour = request.POST.get('custom_colour', '')

    label = models.Label.objects.create(title=title,
                                        discount_percentage=discount_percentage,
                                        creation_date=creation_date,
                                        removal_days=removal_days,
                                        custom_colour=colour)
    label.save()
    if source == 'new_product':
        return HttpResponseRedirect(reverse('crafts_by_micks:create_product'))
    else:
        return HttpResponse('admin page for New Category under construction')

    
def create_product(request):
    options_list = []
    for i in range(1, MAX_OPTIONS+1):
        options_list.append(str(i))

    size_choices = []
    for tup in models.Product_Sizes.size_options:
        size_choices.append(tup[1])

    categories = models.Category.objects.all()
    labels = models.Label.objects.all()

    context = {"size_choices": size_choices,
               "options_list": options_list,
               "categories": categories,
               "labels":labels,
               "source": 'new_product'}
    return render(request, 'create_product.html', context)

# Helper Method
def retrieve_size_pricing(request):
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
    category = get_object_or_404(models.Category, pk= request.POST['category'])
    title = request.POST['title']
    description = request.POST['description']

    size_info_list = retrieve_size_pricing(request)
    product_options_list = retrieve_product_options(request)
    labels_list = [ models.Label.objects.get(id = label_id) for label_id in request.POST.getlist('labels')]

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

    # retrieve newly created product id
    product_id = product.id

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

    return HttpResponse(f"{title}, {description}, Pricing: {size_info_list} "
                        f"Options: {product_options_list}, Category: {category}")

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
