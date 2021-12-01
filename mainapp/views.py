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
        context['notebook'] = Notebook.objects.all()
        context['category'] = Category.objects.all()
        subсategory = {}
        for i in Subсategory.objects.all():
            subсategory[i.category_id] = [i.name, i.slug]


        context['subсategory'] = subсategory
        return context

    def get_queryset(self):
        return Smartphone.objects.all()

def category(request, name_category):
    # if name_category == 'smartphones':
    #     products = Smartphone.objects.all()
    # elif name_category == 'notebooks':
    #     products = Notebook.objects.all()
    context = {
        'subсategory': Subсategory.objects.all(),
        'category': Category.objects.all()
    }

    return render(request, 'mainapp/category.html', context=context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')
    print(Subсategory.objects.first().category_id)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')
