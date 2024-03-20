from django.contrib import admin
from Videos.models import Video, Comment, Category


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date', 'likes', 'dislikes',
                    'watchers_count', 'comments_count', 'user')
    search_fields = ('name', '')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'user', 'comment', 'date')
    search_fields = ('videos', 'user', 'comment',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    filter_horizontal = ('videos',)


admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
