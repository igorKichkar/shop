from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib import messages
from .forms import *
from .models import *
from .utils import get_model_from_slug, get_product_data_for_template, check_in_card


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


def logout_user(request):
    logout(request)
    return redirect('login')


def add_to_card(request, name_category, product_id):
    products = get_model_from_slug(name_category)
    product = products.objects.get(pk=product_id)
    products_in_card = Card.objects.filter(owner=request.user)
    if check_in_card(products_in_card, product):
        print('Exist!!!!!!!!!!!!!')
    else:
        c = Card(owner=request.user, content_object=product)
        c.save()
        print('save')
    return redirect(request.META.get('HTTP_REFERER'))


def card_manager(request):
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
            else:
                print(i.total_products, int((request.POST.get(str(i.id)))), '    NO Change')
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
    Card.objects.filter(id=product_id).delete()
    return redirect('card_manager')
    # return redirect(request.META.get('HTTP_REFERER'))


def create_order(request):
    products_in_card = Card.objects.filter(owner=request.user)
    order1 = TotalOrderForUser(owner=request.user)
    order1.save()
    for i in products_in_card:
        product_registration_in_the_order = OrderProduct(content_object=i.content_object,
                                                         total_products=i.total_products,
                                                         final_price=i.content_object.price)
        print('iteration_________________')
        product_registration_in_the_order.save()
        order1.order.add(product_registration_in_the_order)
        print(order1.order.all())
        i.delete()
    return redirect('index')
