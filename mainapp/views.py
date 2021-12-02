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
from .utils import get_model_from_slug, get_product_data_for_template
from pprint import pprint


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
        context['product_name'] = Product_name.objects.all()
        return context

    def get_queryset(self):
        return Smartphone.objects.all()


def category(request, product_name_category):
    model = get_model_from_slug(product_name_category)
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'product_name': Product_name.objects.all(),
        'products': model.objects.all(),
    }
    return render(request, 'mainapp/category.html', context=context)


def detail_product(request, product_name_category, product_id):
    model_product = get_model_from_slug(product_name_category)
    product = model_product.objects.get(pk=product_id)
    data_product = get_product_data_for_template(model_product, product)
    context = {
        'category': Category.objects.all(),
        'subсategory': Subсategory.objects.all(),
        'product_name': Product_name.objects.all(),
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


def add_to_basket(request, name_category, product_id):
    # request.session['my_car'] = {'model': 'id++'}
    # print(request.session['my_car'])
    a = get_model_from_slug(name_category)
    print(a.objects.get(pk=product_id))
    print(product_id)
    return redirect(request.META.get('HTTP_REFERER'))


def logout_user(request):
    logout(request)
    return redirect('login')
