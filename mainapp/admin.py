from django.forms import ModelChoiceField, ValidationError, ModelForm
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

from PIL import Image


# class ProductAdminForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = mark_safe(
#             '<span style="color:red">Загружайте изображения с минимальным разрешением {}*{}</span>'.format(
#                 *Product.MIN_RESOLUTION))
#
#     def clean_image(self):
#         image = self.cleaned_data['image']
#         img = Image.open(image)
#         min_height, min_width = Product.MIN_RESOLUTION
#         max_height, max_width = Product.MAX_RESOLUTION
#         if image.size > Product.MAX_IMAGE_SIZE:
#             raise ValidationError('Размер изображения превышает 3MB')
#         if img.height < min_height or img.width < min_width:
#             raise ValidationError('Разрешение изображения меньше минимального!')
#         if img.height > max_height or img.width > max_width:
#             raise ValidationError('Разрешение изображения больше максимального!')
#         return image


class NotebookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Order)
admin.site.register(User)
