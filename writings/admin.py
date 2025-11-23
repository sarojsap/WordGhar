from django.contrib import admin
from .models import Writing

@admin.register(Writing)
class WritingAdmin(admin.ModelAdmin):
    list_display=('title','author','category','created_at')
    list_filter=('category','author')
    search_fields=('title','content','author__username')
    readonly_fields=('slug',)
    ordering=('-created_at',)
