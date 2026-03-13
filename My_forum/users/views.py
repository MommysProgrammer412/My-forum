from django.shortcuts import render # для рендера шаблонов
from django.contrib.auth.views import LoginView, LogoutView # готовые классы джанго для входа и выхода
from django.views.generic.edit import CreateView # встроенный класс джанго для создания записей
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # встроенные формы джанго связанные с пользователями (вход, регистрация, смена пароля)
from django.contrib.auth import login # для автоматического входа после регистрации
from .forms import MyUserCreationForm # импортирую кастомную форму регистрации
from django.urls import reverse_lazy # для ссылки на страницу после входа/регистрации

class SignUpView(CreateView):
    '''
    вьюшка регистрации юзеров
    '''
    form_class = MyUserCreationForm # кастомная форма регистрации
    template_name = 'users/register_login.html' # путь к шаблону
    #success_url = reverse_lazy('subscriptions') перенаправление на страницу подписок
    redirect_authenticated_user = True # не давать уже авторизованным пользователям доступ к странице входа и регистрации
    def form_valid(self, form):
        '''
        Метод чтобы «подложить» сессию логина
        '''
        response = super().form_valid(form) # вызываем базовое сохранение формы
        user = form.instance # Извлекаем созданного пользователя из объекта формы
        login(self.request, user) # автоматический вход
        return response # Отправляем пользователя дальше (на success_url)
    def get_context_data(self, **kwargs):
        '''
        Этот метод докладывает доплнительную форму во view, которые отправляются в шаблон, чтобы была возможность выбора нужной формы
        '''
        context = super().get_context_data(**kwargs) # получаю от родительского класса встроенную gjango форму с настройками и сохраняю в переменную
        context['AuthenticationForm'] = AuthenticationForm() # добавляю в словарь ключ и значение, в виде экземпляра дополнительной формы 
        context['type'] = 'signup' # метка, по которой будет вывод формы в шаблоне
        return context # Возвращаю измененный словарь для отрисовки в шаблоне

class UserLoginView(LoginView): 
    '''
    вьюшка для входа юзера
    '''
    form_class = AuthenticationForm # встроенная форма регистрации
    template_name = 'users/register_login.html' # путь к шаблону
    #success_url = reverse_lazy('subscriptions')  перенаправление на страницу подписок
    redirect_authenticated_user = True # не давать уже авторизованным пользователям доступ к странице входа и регистрации
    def get_context_data(self, **kwargs):
        '''
        Этот метод докладывает доплнительную форму во view, которые отправляются в шаблон, чтобы была возможность выбора нужной формы
        '''
        context = super().get_context_data(**kwargs) # получаю от родительского класса встроенную gjango форму с настройками и сохраняю в переменную
        context['MyUserCreationForm'] = MyUserCreationForm() # добавляю в словарь ключ и значение, в виде экземпляра дополнительной формы 
        context['type'] = 'login' # метка, по которой будет вывод формы в шаблоне
        return context # Возвращаю измененный словарь для отрисовки в шаблоне

class UserLogoutView(LogoutView):
    '''вьюха выхода из аккаунта'''
    pass

class PasswordRecovery(CreateView):
    '''вьюха восстановления пароля'''
    pass
