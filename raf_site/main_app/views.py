import base64
import os
import shutil
import tempfile
import time
import threading

import cv2
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.forms import AuthUserForm, AddUserForm, UpdUserForm, SupportRequestForm
from .mixins import GroupRequiredMixin
from .models import User
from .face_rec import register_faces_by_web


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


class GuardView(TemplateView):
    group_required = 'Guards'
    login_url = "/login"
    template_name = "guard.html"

    def dispatch(self, request, *args, **kwargs):
        print(request.user.groups.all())  # Отладочный вывод
        return super().dispatch(request, *args, **kwargs)


class WatcherView(TemplateView):
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
        self.object.username = form.cleaned_data["first_name"][0] + form.cleaned_data["last_name"]
        self.object.save()
        return super().form_valid(form)


class UpdateUserView(UpdateView):
    model = User
    form_class = UpdUserForm
    template_name = 'hr_upd_user.html'
    success_url = reverse_lazy('user_list')
    context_object_name = 'selected_user'


class AccountantPageView(TemplateView):
    template_name = 'accountant.html'


class DownloadFileView(View):
    def post(self, request, *args, **kwargs):
        # Генерация файла (ваш код создания файла)
        content = "Hello, this is a dynamically generated file."

        # Создание временного каталога
        temp_dir = tempfile.mkdtemp()

        # Создание временного файла
        temp_file_path = os.path.join(temp_dir, 'generated_file.txt')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(content)

        # Подготовка ответа для скачивания
        with open(temp_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=generated_file.txt'

        # Очистка временных файлов и каталога
        shutil.rmtree(temp_dir)

        return response


class SupportRequestView(FormView):
    template_name = 'support_request_form.html'
    form_class = SupportRequestForm
    success_url = reverse_lazy('login')  # Подставьте свой URL для успешной отправки
    success_message = "Support request submitted successfully."

    def form_valid(self, form):
        # Сохранение формы и установка пользователя
        form.instance.request_from = self.request.user
        form.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User  # Замените "User" на вашу модель пользователя
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


def webcam_stream(request):
    return render(request, 'webcam_stream.html')


def webcam_stream2(request):
    return render(request, 'webcam_stream2.html')


def webcam_stream_add_face(request):
    if request.method == 'POST':
        print('post')
        register_faces_by_web()
        return JsonResponse({'status': 'success'})
    return render(request, 'watcher_add_face.html')


class UsersAddFaceListView(ListView):
    model = User
    template_name = 'guard_add_face_user_view.html'
    context_object_name = 'users'


class UserAddFaceDetailView(DetailView):
    model = User
    template_name = 'watcher_add_face.html'
    context_object_name = 'selected_user'

    def post(self, request, pk, *args, **kwargs):
        print('post')
        register_faces_by_web(pk)
        return JsonResponse({'status': 'success'})
