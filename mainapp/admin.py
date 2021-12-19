from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class SubсategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class Product_nameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class NotebookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class SmartphoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class HeadphonesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subсategory, SubсategoryAdmin)
admin.site.register(Product_name, Product_nameAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Headphones, HeadphonesAdmin)
admin.site.register(Card)
admin.site.register(OrderProduct)
admin.site.register(TotalOrderForUser)
admin.site.register(User)
