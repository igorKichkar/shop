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

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         return ModelChoiceField(Category.objects.filter(slug='notebooks'))
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class HeadphonesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         return ModelChoiceField(Category.objects.filter(slug='smartphones'))
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subсategory, SubсategoryAdmin)
admin.site.register(Product_name, Product_nameAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Headphones, HeadphonesAdmin)
admin.site.register(Card)
admin.site.register(Order)
admin.site.register(User)
