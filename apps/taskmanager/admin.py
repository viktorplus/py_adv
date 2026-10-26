from django.contrib import admin
from apps.taskmanager.models import (Task, SubTask, Category)
# Register your models here.
# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    filter_horizontal = ('categories',)
    inlines = (SubTaskInline,)

    @admin.display(description='Title', ordering='title')
    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title

@admin.action(description='Mark selected subtasks as Done')
def mark_as_done(modeladmin, request, queryset):
    updated = queryset.update(status='Done')
    modeladmin.message_user(request, f'{updated} Mark selected subtask(s) as Done')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    actions = [mark_as_done]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

