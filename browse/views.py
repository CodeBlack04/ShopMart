from django.shortcuts import render
from django.core.paginator import Paginator

from django.db.models import Q, Min, Max

from product.models import Product, Category
from browse.forms import CategoryForm

# Create your views here.

def get_products(request):
    products_list = Product.objects.filter(is_sold=False).order_by('price')
    categories = Category.objects.all().order_by('name',)
    form = CategoryForm(request.GET)

    min_max_price = products_list.aggregate(Min('price'), Max('price'))

    query = request.GET.get('query', '')
    max_price = request.GET.get('max-price', None)

    if query:
        products_list = products_list.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    if form.is_valid():
        categories = form.cleaned_data['categories']

        if categories:
            category_based_products = []
            for category in categories:
                category_based_products += products_list.filter(category=category)
            products_list = category_based_products

    paginator = Paginator(products_list, 4)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request=request, template_name='browse/index.html', context={
        'products': products,
        'categories': categories,
        'category_form': form,

        'min_max_price': min_max_price,

        'max_price': max_price,

        'query': query,
        'title': 'Browse'
    })