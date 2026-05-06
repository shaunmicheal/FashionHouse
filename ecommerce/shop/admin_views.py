from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Product, Category

@staff_member_required(login_url='/accounts/login/')
def admin_dashboard(request):
    products = Product.objects.all().order_by('-id')
    total = products.count()
    out_of_stock = products.filter(stock=0).count()
    available = products.filter(available=True).count()
    categories = Category.objects.all()
    return render(request, 'admin_panel/dashboard.html', {
        'products': products,
        'total': total,
        'out_of_stock': out_of_stock,
        'available': available,
        'categories': categories,
    })

@staff_member_required(login_url='/accounts/login/')
def admin_add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        stock = request.POST.get('stock')
        available = request.POST.get('available') == 'on'
        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name, slug=slug, category=category,
            description=description, price=price,
            image_url=image_url, stock=stock, available=available
        )
        messages.success(request, f'Product "{name}" added successfully.')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/add_product.html', {'categories': categories})

@staff_member_required(login_url='/accounts/login/')
def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.slug = request.POST.get('slug')
        product.category = get_object_or_404(
            Category, id=request.POST.get('category')
        )
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.image_url = request.POST.get('image_url')
        product.stock = request.POST.get('stock')
        product.available = request.POST.get('available') == 'on'
        product.save()
        messages.success(request, f'Product "{product.name}" updated.')
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/edit_product.html', {
        'product': product,
        'categories': categories,
    })

@staff_member_required(login_url='/accounts/login/')
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
    return redirect('admin_dashboard')

@staff_member_required(login_url='/accounts/login/')
def admin_toggle_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.available = not product.available
    product.save()
    return redirect('admin_dashboard')