from django.urls import path
from .views import SignUpView, UserLoginView # импорт вьюшек связанных с пользователями
from django.views.generic import TemplateView # Импорт встроенного в Django класса для простых страниц

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), # путь для регистрации
    path('subscriptions/', TemplateView.as_view(template_name='users/subscriptions.html'), name='subscriptions'), # путь для страницы редиректа после регистрации/входа
    path('login/', UserLoginView.as_view(), name='login'), # путь для входа
]
