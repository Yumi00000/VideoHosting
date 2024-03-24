from django.contrib import admin
from .models import Video, Comment, Category


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date',
                    'watchers_count', 'comments_count', 'user', 'category')
    search_fields = ('name',)

    def comments_count(self, obj):
        return obj.comment_set.count()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'user', 'comment', 'date')
    search_fields = ('comment',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
