from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birthday = models.DateField()
    status = models.CharField(max_length=150, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=[('М', 'Мужчина'), ('Ж', 'Женщина')])
    email = models.EmailField(unique=True, blank=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    blocked_status = models.CharField(default='active', choices=[('active', 'Активный'), ('blocked', 'Заблокированный'), ('hidden', 'Скрытый')], max_length=7)
    follow = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    block = models.ManyToManyField('self', symmetrical=False)
    def __str__(self):
        return f'{self.username}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    def __str__(self):
        return f"{self.token_hash}"

class Notification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    verb = models.CharField(max_length=8, choices=[('like', 'Лайк'), ('comment', 'Комментарий'), ('follow', 'Подписка'), ('birthday', 'День Рождения')])
    target = models.CharField(max_length=7, null=True, blank=True, choices=[('post', 'Пост'), ('comment', 'Комментарий'), ('user', 'Пользователь')])
    is_read = models.BooleanField(default=False)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Уведомление для {self.user} - {self.verb}"