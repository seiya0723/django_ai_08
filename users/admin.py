from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

#https://github.com/django/django/blob/main/django/contrib/auth/admin.py#L40
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    #管理サイトから追加するときのフォーム
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','first_name', 'last_name' ),
        }),
    )


    list_display = ('username', 'email',  'first_name', 'last_name', 'is_staff')
    search_fields = ('username',   'first_name', 'last_name', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
