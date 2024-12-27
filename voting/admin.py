from django.contrib import admin
from .models import User, Poll, Option, Vote, Category, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin', 'created_at']
    search_fields = ['username', 'email']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'start_time', 'end_time', 'is_public']
    list_filter = ['is_public', 'category']
    search_fields = ['title', 'description']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll']
    search_fields = ['text']

admin.site.register(Vote)
admin.site.register(Comment)
