from django.contrib import admin
from .models import CustomUser, Task
from django.contrib.auth.admin import UserAdmin

# Register CustomUser with UserAdmin to manage it in the admin interface
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

# Register Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'hours_spent', 'status')
    list_filter = ('status', 'date', 'user')
    search_fields = ('title', 'description', 'tags')