from django.urls import path
from .views import SignUpView # импорт вьюшки регистрации
from django.views.generic import TemplateView # Импорт встроенного в Django класса для простых страниц

urlpatterns = [
    path('register_login/', SignUpView.as_view(), name='register_login'), # путь для формы регистрации
    path('subscriptions/', TemplateView.as_view(template_name='users/subscriptions.html'), name='subscriptions'), # путь для страницы редиректа после регистрации
]
