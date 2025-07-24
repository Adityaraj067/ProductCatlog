from django.contrib import admin
from .models import Product, Seller, UserProfile, Cart, Wishlist, OrderedItem, Order, Review, Payment, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pr_id', 'pr_name', 'pr_cate', 'pr_price', 'pr_stk_quant', 'pr_brand', 'pr_season')
    search_fields = ('pr_name', 'pr_brand', 'pr_cate')
    list_filter = ('pr_cate', 'pr_season', 'pr_brand')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'contact')
    search_fields = ('shop_name', 'user__username')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'wallet_balance')
    search_fields = ('user__username', 'phone')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')
    search_fields = ('product__pr_name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'id')
    list_filter = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__pr_name')
    list_filter = ('rating',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'payment_method', 'status', 'payment_date')
    search_fields = ('user__username', 'order__id', 'payment_method')
    list_filter = ('status', 'payment_method')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__pr_name')
