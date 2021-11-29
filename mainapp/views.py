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
        print(context)
        return context

    def get_queryset(self):
        return Smartphone.objects.all()

def index(request):
    print(request.user)
    return render(request, 'mainapp/main.html')


def login(request):
    return HttpResponse('ok')


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
