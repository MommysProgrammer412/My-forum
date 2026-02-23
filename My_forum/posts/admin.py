from django.contrib import admin
from .models import Post, Comment, Hashtag, PostReport, CommentReport, File, PostLike, CommentLike
from django.utils.html import format_html # для отображения превью изображений в админке

# Базовая регистрация моделей, чтобы был к ним доступ в админке
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(PostReport)
admin.site.register(CommentReport)
admin.site.register(File)
admin.site.register(PostLike)
admin.site.register(CommentLike)

# Кастомные классы админки, чтобы превратить интерфейс Django в удобную панель управления
class PostAdmin(admin.ModelAdmin):
    # 1. Что отображать в списке (колонки)
    list_display = ('author', 'text', 'created_at', 'is_blocked', )
    # 2. Фильтры
    list_filter = ('is_blocked', 'block_reason', )
    # 3. Поля для поиска
    search_fields = ('author__username', 'text', )
    # 4. Редактирование поля (из списка)
    list_editable = ('is_blocked', 'block_reason', )
    # 5. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['hide_posts', 'unhide_posts']
    # функции-экшен
    @admin.action(description='Скрыть выбранные посты')
    def hide_posts(self, request, queryset):
        queryset.update(is_blocked=True)
    @admin.action(description='Разблокировать выбранные посты')
    def unhide_posts(self, request, queryset):
        queryset.update(is_blocked=False)
    # 6. Инлайны (показывать связанные объекты прямо на странице поста)
    inlines = ['CommentInline', 'PostLikeInline']

class CommentAdmin(admin.ModelAdmin):
    # 1. Что отображать в списке (колонки)
    list_display = ('author', 'text', 'created_at', 'is_blocked', )
    # 2. Фильтры
    list_filter = ('is_blocked', 'block_reason', )
    # 3. Поля для поиска
    search_fields = ('author__username', 'text', )
    # 4. Редактирование поля (из списка)
    list_editable = ('is_blocked', 'block_reason', )
    # 5. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['hide_comments', 'unhide_comments']
    # функции-экшен
    @admin.action(description='Скрыть выбранные комментарии')
    def hide_comments(self, request, queryset):
        queryset.update(is_blocked=True)
    @admin.action(description='Разблокировать выбранные комментарии')
    def unhide_comments(self, request, queryset):
        queryset.update(is_blocked=False)

class HashtagAdmin(admin.ModelAdmin):
    # 1. Что отображается в списке
    list_display = ('name', 'is_blocked', )
    # 2. Фильтры
    list_filter = ('is_blocked', 'block_reason', )
    # 3. Редактирование поля (из списка)
    list_editable = ('is_blocked', 'block_reason', )
    # 4. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['hide_hashtags', 'unhide_hashtags']
    # функции-экшен
    @admin.action(description='Скрыть выбранные хэштеги')
    def hide_hashtags(self, request, queryset):
        queryset.update(is_blocked=True)
    @admin.action(description='Разблокировать выбранные хэштеги')
    def unhide_hashtags(self, request, queryset):
        queryset.update(is_blocked=False)

class PostReportAdmin(admin.ModelAdmin):
    # 1. Что отображается в списке
    list_display = ('post', 'user', 'reason', 'report_status', )
    # 2. Фильтры
    list_filter = ('report_status', )
    # 3. Редактирование поля (из списка)
    list_editable = ('report_status', )
    # 4. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['hide_posts', 'unhide_posts', 'mark_as_reviewed', 'mark_as_resolved']
    # функции-экшен
    @admin.action(description='Скрыть выбранные посты')
    def hide_posts(self, request, queryset):
        queryset.update(post__is_blocked=True)
    @admin.action(description='Разблокировать выбранные посты')
    def unhide_posts(self, request, queryset):
        queryset.update(post__is_blocked=False)
    @admin.action(description='Пометить жалобы как просмотренные')
    def mark_as_reviewed(self, request, queryset):
        queryset.update(report_status='reviewed')
    @admin.action(description='Пометить жалобы как решенные')
    def mark_as_resolved(self, request, queryset):
        queryset.update(report_status='resolved')

class CommentReportAdmin(admin.ModelAdmin):
    # 1. Что отображается в списке
    list_display = ('comment', 'user', 'reason', 'report_status', )
    # 2. Фильтры
    list_filter = ('report_status', )
    # 3. Редактирование поля (из списка)
    list_editable = ('report_status', )
    # 4. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['hide_comments', 'unhide_comments', 'mark_as_reviewed', 'mark_as_resolved']
    # функции-экшен
    @admin.action(description='Скрыть выбранные комментарии')
    def hide_comments(self, request, queryset):
        queryset.update(comment__is_blocked=True)
    @admin.action(description='Разблокировать выбранные комментарии')
    def unhide_comments(self, request, queryset):
        queryset.update(comment__is_blocked=False)
    @admin.action(description='Пометить жалобы как просмотренные')
    def mark_as_reviewed(self, request, queryset):
        queryset.update(report_status='reviewed')
    @admin.action(description='Пометить жалобы как решенные')
    def mark_as_resolved(self, request, queryset):
        queryset.update(report_status='resolved')

class FileAdmin(admin.ModelAdmin):
    # 1. Что отображается в списке
    list_display = ('author', 'file_type', 'uploaded_at', 'get_preview', )
    # 2. Фильтры
    list_filter = ('file_type', )
    # 3. Просмотр файла
    #Создание метода-поля, который принимает текущий объект
    @admin.display(description='Превью')
    def get_preview(self, obj):
        # Если это изображение - возвращаем HTML с тегом <img>
        if obj.file_type == 'image':
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 5px;"/>', obj.file_path.url)
        # Для других типов файлов можно возвращать иконки или просто текст
        elif obj.file_type == 'video':
            return format_html('<span style="color: blue;">Видео файл</span>')
        elif obj.file_type == 'document':
            return format_html('<span style="color: green;">Документ</span>')
        return 'Нет файла'

# Управление связями и вложенными объектами (Инлайны)
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 # Убираем пустые формы для новых комментариев
    readonly_fields = ('author', 'text', 'created_at', 'is_blocked', 'block_reason', ) # Поля только для чтения

class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0 # Убираем пустые формы для новых комментариев
    readonly_fields = ('user', 'created_at', ) # Поля только для чтения
