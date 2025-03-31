from django.contrib import admin
from .models import Category, Product, Contact, Newsletter, Order
from .models import *
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    readonly_fields = ('rating', 'reviews')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'text')
    search_fields = ('text',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'url', 'alt_text')
    search_fields = ('url', 'alt_text')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'platform', 'total_amount', 'created_at', 'status')
    list_filter = ('platform', 'status')
    search_fields = ('customer_name', 'customer_email')
    readonly_fields = ('created_at',) 