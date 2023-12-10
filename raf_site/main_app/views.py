from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.forms import AuthUserForm, AddUserForm
from .mixins import GroupRequiredMixin
from .models import User


class RedirectView(LoginRequiredMixin, View):
    login_url = "/login"
    def get(self, request, *args, **kwargs):
        user = request.user

        # Проверяем принадлежность пользователя к группам
        if user.groups.filter(name='Guards').exists():
            return redirect('kpp')  # Замените 'group1_home' на URL-маршрут для группы 1
        elif user.groups.filter(name='HR').exists():
            return redirect('')  # Замените 'group2_home' на URL-маршрут для группы 2
        elif user.groups.filter(name='Worker').exists():
            return redirect('')  # Замените 'group2_home' на URL-маршрут для группы 2
        else:
            return redirect('unknown')  # Замените 'default_home' на URL-маршрут по умолчанию


class UnknownView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "unknown.html"


class GuardView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = 'Guards'
    login_url = "/login"
    template_name = "guard.html"



class WatcherView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = 'Guards'
    login_url = "/login"
    template_name = "watcher.html"


class LoginView(LoginView):
    """
    Отображение для входа пользователя в аккаунт
    """
    form_class = AuthUserForm
    redirect_authenticated_user = 'redirect'
    template_name = 'login.html'
    next_page = 'redirect'
    success_url = reverse_lazy('redirect')

    def get_success_url(self):
        return self.success_url


class LogoutView(LogoutView):
    """
    Выход пользователя из аккаунта
    """
    next_page = reverse_lazy('login')


class UsersListView(ListView):
    model = User
    template_name = 'hr_main.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'hr_detail.html'
    context_object_name = 'selected_user'


class AddUserView(CreateView):
    model = User
    form_class = AddUserForm
    template_name = 'hr_add_user.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data["first_name"][0]+form.cleaned_data["last_name"]
        self.object.save()
        return super().form_valid(form)


class UpdateUserView(UpdateView):
    model = User
    form_class = AddUserForm
    template_name = 'hr_upd_user.html'
    success_url = reverse_lazy('user_list')
    context_object_name = 'selected_user'

def webcam_stream(request):
    return render(request, 'webcam_stream.html')