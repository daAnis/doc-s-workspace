from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserKind
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'full_name', 'kind', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('full_name', 'kind')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('full_name', 'kind')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('username', 'full_name', 'kind')
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.register(UserKind)
admin.site.register(User, UserAdmin)