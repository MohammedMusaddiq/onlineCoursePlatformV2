from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(AuthAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_student', 'is_teacher', 'is_active',)
    list_filter = ('email', 'is_student', 'is_teacher', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'otp')}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_active', 'is_student', 'is_teacher', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_student', 'is_teacher',
                       'is_verified')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
