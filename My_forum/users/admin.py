from django.contrib import admin
from .models import User, PasswordResetToken, Notification
from posts.models import Post
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Базовая регистрация моделей, чтобы был к ним доступ в админке
admin.site.register(PasswordResetToken)
admin.site.register(Notification)

# Управление связями и вложенными объектами (Инлайны)
class PostInline(admin.TabularInline):
    model = Post
    extra = 0 # Убираем пустые формы для новых постов
    readonly_fields = ('text', 'created_at', 'is_blocked', 'block_reason', ) # Поля только для чтения
    show_change_link = True # Добавляем ссылку на пост в списке пользователей

# Инлайн для тех, на кого ПОДПИСАН пользователь
class FollowingInline(admin.TabularInline):
    model = User.follow.through # Обращаемся к промежуточной таблице
    fk_name = 'from_user' # Кто подписывается
    extra = 0
    verbose_name = 'Подписка'

# Инлайн для тех, кто ПОДПИСАН на пользователя
class FollowersInline(admin.TabularInline):
    model = User.follow.through # Обращаемся к промежуточной таблице
    fk_name = 'to_user' # На кого подписываются
    extra = 0
    verbose_name = 'Подписчик'

# Кастомные классы админки, чтобы превратить интерфейс Django в удобную панель управления
@admin.register(User) # декоратор для регистрации модели в админке 
class MyUserAdmin(BaseUserAdmin):
    # 1. Что отображать в списке (колонки)
    list_display = ('username', 'email', 'sex', 'blocked_status', )
    # 2. Фильтры в правой панели
    list_filter = ('blocked_status', 'sex', )
    # 3. Поля для поиска
    search_fields = ('username', 'email', )
    # 4. Редактирование поля (из списка)
    list_editable = ('blocked_status', )
    # 5. Кастомные действия
    # Регистрируем действия строкой (имя метода)
    actions = ['block_users', 'unblock_users', 'hidden_users', 'unhidden_users']
    # функции-экшен
    @admin.action(description='Заблокировать выбранных пользователей')
    def block_users(self, request, queryset):
        queryset.update(blocked_status='blocked')
    @admin.action(description='Разблокировать выбранных пользователей')
    def unblock_users(self, request, queryset):
        queryset.update(blocked_status='active')
    @admin.action(description='Скрыть выбранных пользователей и их контент')
    def hidden_users(self, request, queryset):
        queryset.update(blocked_status='hidden')
    @admin.action(description='Раскрыть выбранных пользователей')
    def unhidden_users(self, request, queryset):
        queryset.update(blocked_status='unhide')
    # 6. Инлайны (показывать связанные объекты прямо на странице пользователя)
    inlines = [PostInline, FollowingInline, FollowersInline]
