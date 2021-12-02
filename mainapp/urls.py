from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', StoreHome.as_view(), name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('category/<slug:product_name_category>/', category, name='category'),
    path('detail-product/<slug:product_name_category>/<int:product_id>/', detail_product, name='detail_product'),
    path('add_to_basket/<slug:name_category>/<str:product_id>/', add_to_basket, name='add_to_basket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
