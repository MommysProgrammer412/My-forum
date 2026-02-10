from django.db import models
from django.core.exceptions import ValidationError

class Post(models.Model):
    retweet_of = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=700, blank=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=5, choices=[('spam', 'Спам'), ('abuse', 'Оскорбление'), ('other', 'Другое')], blank = True, null = True)
    is_pinned = models.BooleanField(default=False)
    hashtag = models.ManyToManyField('Hashtag', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.ManyToManyField('File', blank=True, related_name='attached_posts')
    def clean(self):
        text_content = str(self.text or "").strip()
        if not text_content and not self.retweet_of:
            raise ValidationError('Пост должен либо содержать текст, либо быть ретвитом.')
    def __str__(self):
        return f"Пост от {self.author} - {self.text}"

class PostLike(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Лайк от {self.author} к посту {self.post}"

class CommentLike(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Лайк от {self.author} к комментарию {self.comment}"

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=5, choices=[('spam', 'Спам'), ('abuse', 'Оскорбление'), ('other', 'Другое')], blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Комментарий от {self.author} к посту {self.post} - {self.text}"

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=5, choices=[('spam', 'Спам'), ('abuse', 'Оскорбление'), ('other', 'Другое')], blank = True, null = True)
    def __str__(self):
        return f"#{self.name}"

class PostReport(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reason = models.CharField(max_length=5, choices=[('spam', 'Спам'), ('abuse', 'Оскорбление'), ('other', 'Другое')], blank = True, null = True)
    report_status = models.CharField(default='pending', max_length=8, choices=[('pending', 'В ожидании'), ('reviewed', 'Просмотрено'), ('resolved', 'Решено')])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Жалоба от {self.user} на пост {self.post} - {self.reason}"

class CommentReport(models.Model):
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reason = models.CharField(max_length=5, choices=[('spam', 'Спам'), ('abuse', 'Оскорбление'), ('other', 'Другое')], blank = True, null = True)
    report_status = models.CharField(default='pending', max_length=8, choices=[('pending', 'В ожидании'), ('reviewed', 'Просмотрено'), ('resolved', 'Решено')])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Жалоба от {self.user} на комментарий {self.comment} - {self.reason}"

class File(models.Model):
    file_hash = models.CharField(max_length=128)
    file_path = models.FileField(upload_to='media/uploads/')
    size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=8, choices=[('image', 'Изображение'), ('video', 'Видео'), ('document', 'Документ'), ('other', 'Другое')])
    original_name = models.CharField(max_length=255)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Файл: {self.original_name}'