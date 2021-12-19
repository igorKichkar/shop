from django.contrib.auth.views import LogoutView
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', main, name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('category/<slug:product_name_category>/', category, name='category'),
    path('detail-product/<slug:product_name_category>/<int:product_id>/', detail_product, name='detail_product'),
    path('add-to-card/<slug:name_category>/<str:product_id>/', add_to_card, name='add_to_card'),
    path('card-manager/', card_manager, name='card_manager'),
    path('delete-from-card/<int:product_id>/', delete_from_card, name='delete_from_card'),
    path('dcreate-order/', create_order, name='create_order'),
    path('user-orders/', user_orders, name='user_orders'),
    path('detail-order/<int:order_id>/', detail_order, name='detail_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
