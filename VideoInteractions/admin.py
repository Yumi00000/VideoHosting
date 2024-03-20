from django.contrib import admin
from VideoInteractions.models import History, Playlist


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    filter_horizontal = ('videos',)


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', '')
    filter_horizontal = ('videos',)


admin.site.register(History, HistoryAdmin)
admin.site.register(Playlist, PlaylistAdmin)
