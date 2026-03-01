from django.contrib.auth import get_user_model # для импорта модели
from django.contrib.auth.forms import UserCreationForm # импорт стандартной формы создания пользователя

User = get_user_model()

class MyUserCreationForm (UserCreationForm):
    '''
    кастомная форма регистрации
    '''
    class Meta:
        model = User # Моя модель юзера
        fields = ('username', 'email', 'sex', 'birthday', ) # поля, которые будут отображаться в форме
        labels = { # для отображения полкей формы на русском
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'sex': 'Пол',
            'birthday': 'Дата рождения',
        }
