from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from django.contrib.auth.forms import UserChangeForm


class UserAdminForm(UserChangeForm):
    class Meta:
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = UserAdminForm
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'mobile')

    fieldsets = (
        ('General info', {'fields': ('username', 'password'), }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile')}) ,
        (None, {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        (None, {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
