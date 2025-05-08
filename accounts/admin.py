from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import EmailActivation

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'email', 'admin', 'staff', 'is_active', 'score')
    list_filter = ('admin', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'score')}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'activated', 'forced_expire')
    search_fields = ('email', 'user__email', 'user__username')
    raw_id_fields = ('user',)


admin.site.register(EmailActivation, EmailActivationAdmin) 