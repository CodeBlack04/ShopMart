from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import NewProductForm,  EditProductForm

# Create your views here.
def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    related_products = Product.objects.filter(is_sold=False).filter(is_reserved=False).filter(category=product.category).exclude(pk=product_pk)

    if not product.is_sold:
        if product.is_reserved:
            if product.is_reservation_expired():
                print('Product in unreserved')
                product.unreserve()
                product.save()

    return render(request=request, template_name='product/detail.html', context={
        'product': product,
        'related_products': related_products
    })

@login_required
def new_product(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)

        if form.is_valid():
            product_new = form.save(commit=False)
            product_new.created_by = request.user
            product_new.save()

            return redirect('product:detail', product_new.id)
    
    else:
        form = NewProductForm()

    return render(request=request, template_name='product/product_form.html', context={
        'form': form,
        'title': 'List New Product'
    })

@login_required
def edit_product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            return redirect('product:detail', product.id)
        
    else:
        form = EditProductForm(instance=product)

    return render(request=request, template_name='product/product_form.html', context={
        'form': form,
        'title': 'Edit Your product'
    })
        
@login_required
def product_delete(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    product.delete()
    return redirect('core:dashboard')
