from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, UserProfile, Cart, Wishlist, Order, CartItem
from .forms import UserProfileForm
from django.db.models import Sum
from django.core.exceptions import ValidationError

# Helper to get cart item count
def get_cart_item_count(user):
    if not user.is_authenticated:
        return 0
    cart, _ = Cart.objects.get_or_create(user=user)
    return CartItem.objects.filter(cart=cart).aggregate(total=Sum('quantity'))['total'] or 0


def home(request):
    """Home/Landing page"""
    products = Product.objects.all()[:8]  # Show first 8 products
    # Add image URLs for each category (relative to MEDIA_URL)
    home_categories = [
        ("Men", "Men", f"{request.build_absolute_uri('/media/category_images/men.jpg')}",),
        ("Women", "Women", f"{request.build_absolute_uri('/media/category_images/women.jpg')}",),
        ("Boys", "Boys", f"{request.build_absolute_uri('/media/category_images/boys.jpg')}",),
        ("Girls", "Girls", f"{request.build_absolute_uri('/media/category_images/girls.jpg')}",),
        ("Kids", "Kids", f"{request.build_absolute_uri('/media/category_images/kids.jpg')}",),
    ]
    context = {
        'products': products,
        'cart_item_count': get_cart_item_count(request.user),
        'home_categories': home_categories,
    }
    return render(request, 'catalog/home.html', context)


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            Cart.objects.create(user=user)
            Wishlist.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'catalog/signup.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'catalog/login.html')


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile page"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'catalog/profile.html', context)


def product_list(request):
    """Product catalog with filtering"""
    products = Product.objects.all()
    category = request.GET.get('category')
    season = request.GET.get('season')
    fabric = request.GET.get('fabric')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    brand = request.GET.get('brand')

    if category:
        products = products.filter(pr_cate=category)
    if season:
        products = products.filter(pr_season=season)
    if fabric:
        products = products.filter(pr_fabric__icontains=fabric)
    if price_min:
        products = products.filter(pr_price__gte=price_min)
    if price_max:
        products = products.filter(pr_price__lte=price_max)
    if brand:
        products = products.filter(pr_brand__icontains=brand)
    
    context = {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,
        'seasons': Product.SEASON_CHOICES,
        'cart_item_count': get_cart_item_count(request.user),
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, pr_id=product_id)
    reviews = product.review_set.all().order_by('-created_at')
    
    context = {
        'product': product,
        'reviews': reviews,
        'cart_item_count': get_cart_item_count(request.user),
    }
    return render(request, 'catalog/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart with error handling for stock and duplicates."""
    product = get_object_or_404(Product, pr_id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if not product.is_in_stock():
        messages.error(request, f'Sorry, {product.pr_name} is out of stock!')
        return redirect('product_detail', product_id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if product.pr_stk_quant < cart_item.quantity + quantity:
            messages.error(request, f'Cannot add more than available stock for {product.pr_name}.')
            return redirect('cart')
        cart_item.quantity += quantity
    else:
        if product.pr_stk_quant < quantity:
            messages.error(request, f'Cannot add more than available stock for {product.pr_name}.')
            return redirect('cart')
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f'{product.pr_name} added to cart!')
    return redirect('cart')


@login_required
def cart(request):
    """View and update cart with stock validation."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    total = cart.total_price() if hasattr(cart, 'total_price') else sum(item.product.pr_price * item.quantity for item in cart_items)
    if request.method == 'POST':
        for item in cart_items:
            qty = int(request.POST.get(f'quantity_{item.id}', item.quantity))
            if qty > 0:
                if item.product.pr_stk_quant < qty:
                    messages.error(request, f'Not enough stock for {item.product.pr_name}.')
                    continue
                item.quantity = qty
                item.save()
            else:
                item.delete()
        messages.success(request, 'Cart updated!')
        return redirect('cart')
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_item_count': get_cart_item_count(request.user),
    }
    return render(request, 'catalog/cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def wishlist(request):
    """User wishlist"""
    wishlist = get_object_or_404(Wishlist, user=request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'catalog/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist with duplicate check."""
    product = get_object_or_404(Product, pr_id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    if wishlist.products.filter(pk=product.pk).exists():
        messages.info(request, f'{product.pr_name} is already in your wishlist!')
    else:
        wishlist.products.add(product)
        messages.success(request, f'{product.pr_name} added to wishlist!')
    return redirect('product_detail', product_id=product_id)
