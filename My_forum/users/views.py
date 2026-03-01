from django.shortcuts import render # для рендера шаблонов
from django.contrib.auth.views import LoginView, LogoutView # готовые классы джанго для входа и выхода
from django.views.generic.edit import CreateView # встроенный класс джанго для создания записей
from django.contrib.auth.forms import UserCreationForm # встроенная форма джанго для регистрации
from django.contrib.auth import login # для автоматического входа после регистрации
from .forms import MyUserCreationForm # импортирую кастомную форму регистрации
from django.urls import reverse_lazy # для ссылки на страницу после входа/регистрации

class SignUpView(CreateView):
    '''
    вьюшка регистрации юзеров
    '''
    form_class = MyUserCreationForm # кастомная форма регистрации
    template_name = 'users/register_login.html' # путь к шаблону
    success_url = reverse_lazy('subscriptions') # перенаправление на страницу подписок
    def form_valid(self, form):
        '''
        Метод чтобы «подложить» сессию логина
        '''
        response = super().form_valid(form) # вызываем базовое сохранение формы
        user = form.instance # Извлекаем созданного пользователя из объекта формы
        login(self.request, user) # автоматический вход
        return response # Отправляем пользователя дальше (на success_url)
















class UserLoginView(LoginView): 
    pass

class UserLogoutView(LogoutView):
    pass
