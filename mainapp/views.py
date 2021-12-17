import instance as instance
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .forms import *
from django.apps import apps
from .models import *
from .utils import get_model_from_slug, get_product_data_for_template, check_in_card
from pprint import pprint
from django.contrib.contenttypes.models import ContentType, ContentTypeManager


class StoreHome(ListView):
    model = Smartphone
    template_name = 'mainapp/main.html'
    context_object_name = 'smartphones'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Главная страница")
    #     context = dict(list(context.items()) + list(c_def.items()))
    #     return context
    #
    #     return dict(list(context.items()) + list(c_def.items()))
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['subсategory'] = Subсategory.objects.all()
        context['products_name'] = Product_name.objects.all()
        return context

    def get_queryset(self):
        return Smartphone.objects.all()


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
    data_product = get_product_data_for_template(products, product)
    products_in_card = Card.objects.filter(owner=request.user)
    context = {
        'in_card': check_in_card(products_in_card, product),
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'model': product_name_category,
        'data_product': data_product,
    }
    return render(request, 'mainapp/detail_product.html', context=context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def add_to_card(request, name_category, product_id):
    products = get_model_from_slug(name_category)
    product = products.objects.get(pk=product_id)
    products_in_card = Card.objects.filter(owner=request.user)
    if check_in_card(products_in_card, product):
        print('Exist!!!!!!!!!!!!!')
    else:
        c = Card(owner=request.user, content_object=product, final_price=product.price)
        c.save()
        print('save')
    return redirect(request.META.get('HTTP_REFERER'))


def card_manager(request):
    products_in_card = Card.objects.filter(owner=request.user)
    if request.method == "POST":
        form = CardAmmount(request.POST)
        if form.is_valid():
            print(form.cleaned_data['ammount'])
            return redirect('card_manager')
    else:
        form = CardAmmount()
    context = {
        'form': form,
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'products_name': Product_name.objects.all(),
        'products_in_card': products_in_card,
    }
    return render(request, 'mainapp/card.html', context=context)


def update_card(request):
    if request.method == "POST":
        form = CardAmmount(request.POST)
        print(form.cleaned_data['ammount'])

    form = CardAmmount()
    return redirect(request.META.get('HTTP_REFERER'))


def logout_user(request):
    logout(request)
    return redirect('login')
