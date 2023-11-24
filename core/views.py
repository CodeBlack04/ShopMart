from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from product.models import Product, Category
from .forms import ContactForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        products_list = Product.objects.filter(is_sold=False).exclude(created_by=request.user).order_by('-created_at')
    else:
        products_list = Product.objects.filter(is_sold=False).order_by('-created_at')

    categories = Category.objects.all()

    paginator = Paginator(products_list, 5)

    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    return render(request=request, template_name='core/home/index.html', context={
        'title': 'Welcome',
        'products': products,
        'categories': categories,
    })

@login_required
def dashboard(request):
    products = Product.objects.filter(created_by = request.user)
    
    return render(request=request, template_name='core/home/dashboard.html', context={
        'products': products,
        'title': 'Dashboard'
    })

def about(request):
    return render(request=request, template_name='core/home/about.html', context={
        'title': 'About'
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')
        
    else:
        form = ContactForm()
        
    return render(request=request, template_name='core/home/contact.html', context={
        'form': form,
        'title': 'Contact'
    })

def policy(request):
    return render(request=request, template_name='core/home/policy.html', context={
        'title': 'Policy'
    })

def terms(request):
    return render(request=request, template_name='core/home/terms.html', context={
        'title': 'Terms'
    })

