from django.contrib import admin
from . models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'status', 'trending']

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)



admin.site.register(Category)
admin.site.register(Product)
