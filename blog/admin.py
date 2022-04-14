from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')  # Поля которые нужно показывать
    list_filter = ('status', 'created', 'publish', 'author')  # Фильтрация
    search_fields = ('title', 'body')  # Поиск
    # Автоматически заполнение слага
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')  # Метод сортировки
