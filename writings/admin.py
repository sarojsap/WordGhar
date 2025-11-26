from django.contrib import admin
from .models import Writing, Like, Comment

@admin.register(Writing)
class WritingAdmin(admin.ModelAdmin):
    list_display=('title','author','category','created_at')
    list_filter=('category','author')
    search_fields=('title','content','author__username')
    readonly_fields=('slug',)
    ordering=('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=('user','writing','created_at')
    list_filter=('created_at',)
    search_fields=('user__username','writing__title')
    ordering=('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user','writing','created_at','content_preview')
    list_filter=('created_at',)
    search_fields=('user__username','writing__title','content')
    ordering=('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
