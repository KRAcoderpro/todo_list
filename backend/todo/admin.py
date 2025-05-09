from django.contrib import admin
from .models import Task, Category, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'due_date', 'finished']
    list_filter = ['finished', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
