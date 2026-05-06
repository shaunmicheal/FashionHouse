from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category

def home(request):
    products = Product.objects.filter(available=True)[:8]
    return render(request, 'shop/home.html', {'products': products})

def product_listing(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'shop/product_listing.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)
    request.session['cart'] = cart
    return redirect('cart')
# Create your views here.
