from django.contrib import admin
from Users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'first_name', 'last_name', 'email',
                    'birthday', 'gender', 'phone_number', 'followers_count', 'followings_count',
                    )


admin.site.register(CustomUser, UserAdmin)
