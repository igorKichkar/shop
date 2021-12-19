from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import *
from .models import *

from .utils import get_model_from_slug, get_product_data_for_template, check_in_card


def main(request):
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
    }
    return render(request, 'mainapp/main.html', context=context)


def category(request, product_name_category):
    products = get_model_from_slug(product_name_category)
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'products': products.objects.all(),
    }
    return render(request, 'mainapp/category.html', context=context)


def detail_product(request, product_name_category, product_id):
    products = get_model_from_slug(product_name_category)
    product = products.objects.get(pk=product_id)
    if request.user.is_authenticated:
        in_card = check_in_card(Card.objects.filter(owner=request.user), product)
    else:
        in_card = False
    context = {
        'in_card': in_card,
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'model': product_name_category,
        'data_product': get_product_data_for_template(products, product),

    }
    return render(request, 'mainapp/detail_product.html', context=context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['subсategory'] = Subсategory.objects.all()
        context['products_name'] = Product_name.objects.all()
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['subсategory'] = Subсategory.objects.all()
        context['products_name'] = Product_name.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def add_to_card(request, name_category, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    products = get_model_from_slug(name_category)
    product = products.objects.get(pk=product_id)
    products_in_card = Card.objects.filter(owner=request.user)
    if not check_in_card(products_in_card, product):
        c = Card(owner=request.user, content_object=product)
        c.save()
    return redirect(request.META.get('HTTP_REFERER'))


def card_manager(request):
    if not request.user.is_authenticated:
        return redirect('login')

    def check_form_inputs(inputs):
        for i in inputs:
            form_input = int(request.POST.get(str(i.id)) or 0)
            if not form_input > 0:
                return False
        return True

    products_in_card = Card.objects.filter(owner=request.user)
    if request.method == "POST":
        if not check_form_inputs(products_in_card):
            messages.add_message(request, messages.INFO, 'Некоректное колличество товара')
            return redirect('card_manager')
        for i in products_in_card:
            form_input = request.POST.get(str(i.id))
            if i.total_products != int(form_input) and int(form_input) > 0:
                i.total_products = int((request.POST.get(str(i.id))))
                i.save()
    sum_in_catd = 0
    for i in products_in_card:
        sum_in_catd += i.content_object.price * i.total_products
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'products_in_card': products_in_card,
        'sum_in_catd': sum_in_catd,
    }
    return render(request, 'mainapp/card.html', context=context)


def delete_from_card(request, product_id):
    product_in_card = Card.objects.get(id=product_id)
    if not product_in_card.owner == request.user:
        return HttpResponse('Error handler content', status=403)
    product_in_card.delete()
    return redirect('card_manager')


def create_order(request):
    if not request.user.is_authenticated:
        return HttpResponse('Error handler content', status=403)
    products_in_card = Card.objects.filter(owner=request.user)
    order = TotalOrderForUser(owner=request.user)
    order.save()
    for i in products_in_card:
        product_registration_in_the_order = OrderProduct(content_object=i.content_object,
                                                         total_products=i.total_products,
                                                         final_price=i.content_object.price)
        product_registration_in_the_order.save()
        order.order.add(product_registration_in_the_order)
        i.delete()
    return redirect('index')


def user_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'user_orders': TotalOrderForUser.objects.filter(owner=request.user)
    }
    return render(request, 'mainapp/user_orders.html', context=context)


def detail_order(request, order_id):
    order = TotalOrderForUser.objects.get(id=order_id)
    if not order.owner == request.user:
        return HttpResponse('Error handler content', status=403)
    order_products = order.order.all()
    sum_price = 0
    for i in order_products:
        sum_price += i.final_price * i.total_products
    context = {
        'order': order,
        'order_products': order_products,
        'sum_price': sum_price,
    }
    return render(request, 'mainapp/detail_order.html', context=context)


def delete_order(request, order_id):
    order = TotalOrderForUser.objects.get(id=order_id)
    if not order.owner == request.user:
        return HttpResponse('Error handler content', status=403)
    order.delete()
    return redirect('user_orders')
